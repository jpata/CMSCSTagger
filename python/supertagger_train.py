import ROOT
from ROOT import TMVA
from copy import deepcopy
import numpy as np
import ctypes
import array
import os
import math
from mvalib import Data, Classifier
from collections import OrderedDict

class ROOTData(Data):
    def __init__(self, **kwargs):
        Data.__init__(self, **kwargs)

        self.filename = kwargs.get("filename")
        self.treename = kwargs.get("treename")
        self.kind = kwargs.get("kind")
        self.label = kwargs.get("label")
        self.selection = "1"
        
        self.tree = None
        self.tfile = None
        self.is_loaded = False

    def load(self):
        self.tfile = ROOT.TFile(self.filename)
        self.tree = self.tfile.Get(self.treename)
        if not self.tree:
            raise Exception("Could not open {0}:{1}".format(
                self.filename, self.treename
            ))
        self.is_loaded = True
    
    def unload(self):
        self.tfile.Close()
        self.is_loaded = False
    
    
    def __len__(self):
        return self.tree.GetEntries()
        
    def hist(self, func, bins, cut):
        #ROOT.gROOT.cd()
        h = ROOT.TH1D("h", "h", *bins)
        n = self.tree.Draw("{0} >> h".format(func), cut)
        return h

def roc(h1, h2):
    h1 = h1.Clone()
    h2 = h2.Clone()
    h1.Scale(1.0 / h1.Integral())
    h2.Scale(1.0 / h2.Integral())
    c1 = h1.GetCumulative()
    c2 = h2.GetCumulative()
    nb = c1.GetNbinsX()
    ret = np.zeros((nb, 2))
    err = np.zeros((nb, 2))
    for i in range(nb):
        ret[i,0] = c1.GetBinContent(i+1) 
        ret[i,1] = c2.GetBinContent(i+1)
        err[i,0] = 0.0*c1.GetBinError(i+1) 
        err[i,1] = 0.0*c2.GetBinError(i+1)
    return ret, err
    
def check_data(data):
    brs = data.tree.GetListOfBranches()
    for br in brs:
        isnan = data.tree.GetEntries("{0} != {0}".format(br.GetName()))
        isinf = data.tree.GetEntries("{0} > 99999 || {0} < -99999".format(br.GetName()))
        print br.GetName(), isnan, isinf
        
    
class TMVABDTClassifier(Classifier):
    def __init__(self, **kwargs):
        Classifier.__init__(self, **kwargs)
        self.name = kwargs.get("name")
        
        self.mva_name = "bdt_" + self.name
        self.weights_file = "weights/tmva_{0}.weights.xml".format(
            self.mva_name
        )
        self.out_file = "outputs/TMVA_{0}.root".format(
            self.mva_name
        )

        self.variables = kwargs.get("variables")
        self.spectators = kwargs.get("spectators", [])

        self.ntrees = kwargs.get("ntrees", 1200)
        self.shrinkage = kwargs.get("shrinkage", 0.1)
        self.bag_fraction = kwargs.get("bag_fraction", 1.0)
        self.ncuts = kwargs.get("ncuts", 50)
        self.max_depth = kwargs.get("max_depth", 3)
        self.use_bootstrap = kwargs.get("use_bootstrap", False)
        self.data = []

    def prepare(self):
        self.out = ROOT.TFile(
            self.out_file,
            "RECREATE"
        )
        self.out.cd()
        self.factory = TMVA.Factory(
            "tmva", self.out,
            "Transformations=I;N:"+
            "DrawProgressBar=True:"+
            "!V:Silent=False:"+
            "AnalysisType=Classification"
        )
        for var in self.variables:
            self.factory.AddVariable(var, "F")
        for var in self.spectators:
            self.factory.AddSpectator(var, "F")
            
        for data in self.data:
            self.factory.AddTree(
                data.tree,
                data.label,
                1.0,
                ROOT.TCut(data.selection),
                data.kind
            )
    
    def load_data(self):
        for data in self.data:
            data.load()
            
    def add_data(self, data):
        self.data += [data]

    def train(self):
        print "training", self.mva_name

        self.mva_opts = ("!H:" +
            "!V:VerbosityLevel=Verbose:" +
            "NTrees={0}:".format(self.ntrees) +
            "BoostType=Grad:" +
            "Shrinkage={0}:".format(self.shrinkage) +
            #"GradBaggingFraction={0}:".format(self.bag_fraction) +
            "nCuts={0}:".format(self.ncuts) +
            "MaxDepth={0}:".format(self.max_depth)+
            "UseBaggedBoost={0}:".format(self.use_bootstrap)+
            "DoBoostMonitor=False"
        )

        self.factory.BookMethod(
            TMVA.Types.kBDT,
            self.mva_name,
            #"VerbosityLevel=Debug"
            self.mva_opts
        )

        # nevents_str = []
        # for icl, cl in enumerate(self.data_classes):
        #     nmax = min(self.max_events, self.data[cl].tree.GetEntries() / 2)
        #     nevents_str += ["nTrain_{0}={1}".format(cl, nmax)]
        #     nevents_str += ["nTest_{0}={1}".format(cl, nmax)]
        # nevents_str = ":".join(nevents_str)
        
        cutstrs = ["1"]
        #for var in self.variables:
        #    cutstrs += ["{0}=={0} && {0}>=-10 && {0}<100".format(var)]
        cutstr = "&&".join(cutstrs)
        print "cutstr", cutstr
        self.factory.PrepareTrainingAndTestTree(
            ROOT.TCut(cutstr),
            "SplitMode=Block:MixMode=Block:NormMode=NumEvents:V"# + nevents_str
        )

        self.factory.TrainAllMethods()
        self.factory.TestAllMethods()
        #self.factory.EvaluateAllMethods() #crashes?
        
        # * thread #1: tid = 0x11d781, 0x000000010d40a7c8 libTMVA.so`TMVA::DataSet::GetNEvtSigTest() + 50, queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=1, address=0x70)
        # frame #0: 0x000000010d40a7c8 libTMVA.so`TMVA::DataSet::GetNEvtSigTest() + 50
        # frame #1: 0x000000010d4302e7 libTMVA.so`TMVA::Factory::EvaluateAllMethods() + 11729
        # frame #2: 0x0000000102a019c7
    
        #print "done evaluate"
        self.factory.DeleteAllMethods()
        #del self.factory

        #Clean up factory
        #Necessary for serializing TMVAClassifier
        self.factory = None

        self.out.Write()
        self.out.Close()
        print "done training", self.mva_name
        #del self.out
        #self.out = None
        return self

    def evaluate(self, data):
        reader = TMVA.Reader("!V:Silent")

        vardict = {}
        vardict_d = {}
        for var in self.variables:
            vardict[var] = array.array("f", [0])
            vardict_d[var] = array.array("d", [0])
            reader.AddVariable(var, vardict[var])
        for var in self.spectators:
            vardict[var] = array.array("f", [0])
            vardict_d[var] = array.array("d", [0])
            reader.AddSpectator(var, vardict[var])
        reader.BookMVA(self.mva_name, self.weights_file)

        ret = np.zeros(
            (len(data), 1),
            #len(set([data.label for data in self.data]))),
            dtype="f"
        )

        data.tree.SetBranchStatus("*", False)
        for var in self.variables:
            data.tree.SetBranchStatus(var, True)
            data.tree.SetBranchAddress(var, vardict_d[var])
        
        for iev in range(len(data)):
            data.tree.GetEntry(iev)
            for k in vardict.keys():
                vardict[k][0] = float(vardict_d[k][0])
            x = reader.EvaluateMVA(self.mva_name)
            ret[iev,0] = x
            #for j in range(x.size()):
            #    ret[iev, j] = x.at(j)

        data.tree.SetBranchStatus("*", True)
        for var in self.variables:
            data.tree.SetBranchAddress(var, 0)
        return ret
