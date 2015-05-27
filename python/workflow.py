import ROOT
ROOT.gROOT.cd()
ROOT.gROOT.SetBatch(True)
from supertagger_train import ROOTData, TMVABDTClassifier
import supertagger_train
import numpy as np
from copy import deepcopy
import multiprocessing
from multiprocessing import Pool
import glob, sys, os
from roothelpers import array2root

#steps = ["project", "train", "evaluate"]
steps = ["train", "evaluate"]
#steps = ["evaluate"]

input_file = "jets.root"
output_file = "out.root"

spectators = ["flavour", "pt", "eta"]

#Select a subregion of the full training data
cls1 = TMVABDTClassifier(
    name="cls1",
    variables=["bd_csv1", "bd_csv2"],
    ntrees=50,
    spectators=spectators,
)

#Select a subregion of the full training data
cls2 = TMVABDTClassifier(
    name="cls2",
    variables=["bd_csv1", "bd_csv2", "bd_jp", "bd_sel", "bd_smu"],
    ntrees=50,
    spectators=spectators,
)


path = "/Users/joosep/Documents/btv/data/"

d1a = ROOTData(label="b", filename=path+"ttjets_b_training.root", treename="tree_b", kind=ROOT.TMVA.Types.kTraining)
d2a = ROOTData(label="l", filename=path+"ttjets_c_training.root", treename="tree_c", kind=ROOT.TMVA.Types.kTraining)
d3a = ROOTData(label="l", filename=path+"ttjets_l_training.root", treename="tree_l", kind=ROOT.TMVA.Types.kTraining)

d1b = ROOTData(label="b", filename=path+"ttjets_b_testing.root", treename="tree_b", kind=ROOT.TMVA.Types.kTesting)
d2b = ROOTData(label="l", filename=path+"ttjets_c_testing.root", treename="tree_c", kind=ROOT.TMVA.Types.kTesting)
d3b = ROOTData(label="l", filename=path+"ttjets_l_testing.root", treename="tree_l", kind=ROOT.TMVA.Types.kTesting)

for d in [d1a, d2a, d3a, d1b, d2b, d3b]:
    cls1.add_data(d)
    cls2.add_data(d)
cls1.load_data()
# 
# for d in [d1a, d2a, d3a, d1b, d2b, d3b]:
#     print d.filename
#     supertagger_train.check_data(d)
# 
# cls1.prepare()
# cls1.train()
# 
# cls2.prepare()
# cls2.train()
# 
# x = np.hstack((cls1.evaluate(d1b), cls2.evaluate(d1b)))
# y = np.hstack((cls1.evaluate(d2b), cls2.evaluate(d2b)))
# z = np.hstack((cls1.evaluate(d3b), cls2.evaluate(d3b)))
# array2root(x, "ttjets_b_testing.root", "tree", ["cls1", "cls2"])
# array2root(y, "ttjets_c_testing.root", "tree", ["cls1", "cls2"])
# array2root(z, "ttjets_l_testing.root", "tree", ["cls1", "cls2"])

d1_cls = supertagger_train.ROOTData(filename="ttjets_b_testing.root", treename="tree")
d2_cls = supertagger_train.ROOTData(filename="ttjets_c_testing.root", treename="tree")
d3_cls = supertagger_train.ROOTData(filename="ttjets_l_testing.root", treename="tree")

for d in [d1_cls, d2_cls, d3_cls]:
    d.load()

d1b.tree.AddFriend(d1_cls.tree)
d2b.tree.AddFriend(d2_cls.tree)
d3b.tree.AddFriend(d3_cls.tree)

validation_of = ROOT.TFile("out.root", "RECREATE")
validation_of.cd()

for fn, d in [("b", d1b), ("c", d2b), ("l", d3b)]:
    rdir = validation_of.mkdir(fn)
    for cl, lims in [
        ("bd_csv1", (100, 0, 1)),
        ("bd_csv2", (100, 0, 1)),
        ("bd_jp", (100, 0, 2)),
        ("bd_sel", (100, 0, 1)),
        ("bd_smu", (100, 0, 1)),
        ("cls1", (100, -1, 1)),
        ("cls2", (100, -1, 1))
        ]:
        h = d.hist(cl, lims, "1")
        rdir.cd()
        h = h.Clone("h_{0}".format(cl))
        h.Write()
        
        hc = h.GetCumulative()
        hc.SetName(h.GetName() + "_c")
        hc.Write()

validation_of.Close()
