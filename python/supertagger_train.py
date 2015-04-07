import ROOT
from ROOT import TMVA
from copy import deepcopy
import numpy as np
import ctypes 
import array

def array2root(arr,
    filename,
    treename,
    colnames=None,
    command="recreate"
    ):
    
    of = ROOT.TFile(filename, command)
    of.cd()
    tree = ROOT.TTree(treename, treename)
    if len(arr.shape)==1:
        nevs = len(arr)
        ncols = 1
        arr = arr.reshape((nevs, ncols))
    elif len(arr.shape)==2:
        nevs, ncols = arr.shape
    
    if not colnames:
        colnames = ["br"+str(i) for i in range(ncols)]
        
    branchvars = {}
    for col in range(ncols):
        brname = colnames[col]
        branchvars[col] = array.array("f", [0.0])
        tree.Branch(
            brname,
            branchvars[col],
            "{0}/F".format(brname)
        )
        
    nf = 0
    for i in range(nevs):
        for col in range(ncols):
            branchvars[col][0] = float(arr[i, col])
        nf += tree.Fill()
    
    tree.Write("", ROOT.TObject.kOverwrite)
    of.Close()
    
def root2array(
    filename,
    treename,
    colnames=None,
    ):
    
    of = ROOT.TFile(filename)
    tree = of.Get(treename)
    
    nevs = tree.GetEntries()
    ncols = len(colnames)
        
    branchvars = {}
    #tree.SetBranchStatus("*", False)
    
    arr = np.zeros((nevs, ncols), dtype="f")
    
    for col in range(ncols):
        brname = colnames[col]
        cn = tree.GetBranch(brname).GetListOfLeaves().At(0).GetTypeName()
        #print cn
        if cn == "Int_t":
            t = "i"
        elif cn == "Float_t":
            t = "f"
        branchvars[col] = array.array(t, [0])
        tree.SetBranchAddress(
            brname,
            branchvars[col],
        )
        #tree.SetBranchStatus(brname, True)
    
    nf = 0
    for i in range(nevs):
        nf += tree.GetEntry(i)
        #if i<10:
        #    print [branchvars[col][0] for col in range(ncols)]
        for col in range(ncols):
            arr[i, col] = branchvars[col][0]
    
    #print nf
    return arr
    
class Data(object):
    def __init__(self, **kwargs):
        self.classes = kwargs.get("classes", [])
        
    def selection(self, sel):
        """
        Applies selection on the data.
        """
        pass
        
    def get_category(self, category):
        """
        Returns the data in a category.
        Category is "test", "train".
        
        Arguments:
            category (string) - the category to get
            
        Returns (Data): selected data
        """
        pass
        
    def roc(self, class_a, class_b, classifier):
        pass

class ROOTData(Data):
    def __init__(self, **kwargs):
        Data.__init__(self, **kwargs)
        
        fname = kwargs.get("filename", None)
        treename = kwargs.get("treename", None)
        tree = kwargs.get("tree", None)
        
        if fname and treename:
            self.tfile = ROOT.TFile(fname)
            self.tree = self.tfile.Get(treename)
        elif tree != None:
            self.tree = tree
    
    def selection(self, **kwargs):
        
        selection = kwargs.get("selection", None)
        partition = kwargs.get("partition", None)
        
        c = deepcopy(self)
        
        if selection:
            tree = self.tree.CopyTree(selection)
        elif partition:
            low, high = min(partition), max(partition)
            tree = self.tree.CopyTree("", "", high-low, low)
        else:
            tree = self.tree.CloneTree()
        c.tree = tree
        return c
        
    def __len__(self):
        return self.tree.GetEntries()

class TrainingReport:
    pass
    
class Classifier:
    def __init__(self, **kwargs):
        pass
    
    def prepare(self):
        pass
    
    def add_class(self):
        pass
    
    def train(self, data):
        pass
    
    def evaluate(self, data):
        pass

class TMVAClassifier:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.mva_name = "bdt_" + self.name

        self.weights_file = "weights/{0}_{1}.weights.xml".format(
            self.name, self.mva_name
        )
        self.out_file = "outputs/TMVAMulticlass_{0}.root".format(self.name)
        
        self.variables = kwargs.get("variables")
        self.spectators = kwargs.get("spectators", [])
        
        self.ntrees = kwargs.get("ntrees", 1200)
        self.shrinkage = kwargs.get("shrinkage", 0.1)
        self.bag_fraction = kwargs.get("bag_fraction", 0.5)
        self.ncuts = kwargs.get("ncuts", 50)
        self.max_depth = kwargs.get("max_depth", 3)
        self.data_classes = kwargs.get("data_classes")
        self.data = []
        
    def prepare(self):
        self.out = ROOT.TFile(
            self.out_file,
            "RECREATE"
        )
        self.out.cd()
        self.factory = TMVA.Factory(
            self.name, self.out,
            "Transformations=I;N:"+
            "DrawProgressBar=False:"+
            "!V:"+
            "AnalysisType=Multiclass"
        )
        for var in self.variables:
            self.factory.AddVariable(var, "F")
        for var in self.spectators:
            self.factory.AddSpectator(var, "F")
    def add_class(self, class_name, data):
        self.data += [(data, class_name)]
        self.factory.AddTree(data.tree, class_name, 1.0)
        
    def train(self):
        print "training", self.name
        
        self.pt_eta_cat = self.factory.BookMethod(
            TMVA.Types.kCategory,
            "pteta_" + self.name,
            "VerbosityLevel=Debug", #options
        )
        
        self.mva_opts = ("!H:" +
            "!V:" +
            "NTrees={0}:".format(self.ntrees) +
            "BoostType=Grad:" +
            "Shrinkage={0}:".format(self.shrinkage) +
            "GradBaggingFraction={0}:".format(self.bag_fraction) +
            "nCuts={0}:".format(self.ncuts) + 
            "MaxDepth={0}".format(self.max_depth)
        )
        
        for data, cls in self.data:
            print cls, data.tree.GetEntries()
        
        skipped = []
        for ptbin in range(1, 82):
            for etabin in range(1, 22):
                cut_str = "pt_bin=={0} && eta_bin=={1}".format(ptbin, etabin)
                cut = ROOT.TCut(cut_str)
                min_n = min(
                    [data.tree.GetEntries(cut_str) for (data, cls) in self.data]
                )
                if min_n < 10:
                    print "skipping", ptbin, etabin
                    skipped += [(ptbin, etabin)]
                    continue
                    
                self.pt_eta_cat.AddMethod(
                    cut,
                    ":".join(self.variables),
                    TMVA.Types.kBDT,
                    self.mva_name + "_{0}_{1}".format(ptbin, etabin),
                    #"VerbosityLevel=Debug"
                    self.mva_opts
                )
        
        skipcut = []
        for (ptbin, etabin) in skipped:
            print "skipped", ptbin, etabin
            skipcut += [
                "((pt_bin - pt_bin%10)/10 == {0} && (eta_bin - eta_bin%10)/10 == {1})".format(ptbin, etabin)
            ]
        skipcut = "||".join(skipcut)
        skipcut = "!(" + skipcut + ")"
        
        self.factory.PrepareTrainingAndTestTree(
            ROOT.TCut(""),
            "SplitMode=Block:NormMode=NumEvents:!V"
        )
        
        self.factory.TrainAllMethods()
        #self.factory.TestAllMethods()
        #self.factory.EvaluateAllMethods()
        #self.factory.DeleteAllMethods()
        #del self.factory
        
        #Clean up factory
        #Necessary for serializing TMVAClassifier
        self.factory = None
        
        self.out.Write()
        self.out.Close()
        #del self.out
        #self.out = None
        return self
        
    def evaluate(self, data):
        reader = TMVA.Reader("!V:Silent")
        
        vardict = {}
        for var in self.variables:
            vardict[var] = array.array("f", [0])
            reader.AddVariable(var, vardict[var])
                
        reader.BookMVA(self.mva_name, self.weights_file)
    
        ret = np.zeros((len(data), len(self.data_classes)), dtype="f")
        
        data.tree.SetBranchStatus("*", False)
        for var in self.variables:
            data.tree.SetBranchStatus(var, True)
            data.tree.SetBranchAddress(var, vardict[var])
            
        for iev in range(len(data)):
            data.tree.GetEntry(iev)
            x = reader.EvaluateMulticlass(self.mva_name)
            for j in range(x.size()):
                ret[iev, j] = x.at(j)
        
        data.tree.SetBranchStatus("*", True)
        return ret
