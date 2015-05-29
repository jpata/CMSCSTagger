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
    ntrees=10,
    spectators=spectators,
)

#Select a subregion of the full training data
cls2 = TMVABDTClassifier(
    name="cls2",
    variables=["bd_csv1", "bd_csv2", "bd_jp", "bd_sel", "bd_smu"],
    ntrees=10,
    spectators=spectators,
)

#Select a subregion of the full training data
cls3 = TMVABDTClassifier(
    name="cls3",
    variables=["bd_csv1", "bd_csv2", "bd_jp", "bd_sel", "bd_smu"],
    ntrees=10,
    spectators=spectators,
    weight="w1"
)


#path = "/Users/joosep/Documents/btv/data/"
path = "./data/"

ds = {}

for dt in ["qcd", "ttjets"]:
    for typ, kind in [
        ("testing", ROOT.TMVA.Types.kTesting),
        ("training", ROOT.TMVA.Types.kTraining)
    ]:
        for label, lt in [("b", "b"), ("c", "l"), ("l", "l")]:
            ds[(dt, typ, label)] = ROOTData(
                label=lt,
                filename=path+"{0}_{1}_{2}.root".format(dt, label, typ),
                treename="tree_{0}".format(label),
                kind=kind
            )

for dt in ["ttjets"]:
    for typ, kind in [
        ("testing", ROOT.TMVA.Types.kTesting),
        ("training", ROOT.TMVA.Types.kTraining)
    ]:
        for label, lt in [("b", "b"), ("c", "l"), ("l", "l")]:
            d = ds[(dt, typ, label)]
            cls1.add_data(d)
            cls2.add_data(d)
            cls3.add_data(d)

for d in ds.values():
    d.load()

cls1.prepare()
cls1.train()

cls2.prepare()
cls2.train()

cls3.prepare()
cls3.train()

ds_eval = {}
for ((dt, typ, label), d) in ds.items():
    print d.tree, [x.tree for x in cls1.data], [x.tree for x in cls2.data]
    x = np.hstack((cls1.evaluate(d), cls2.evaluate(d), cls3.evaluate(d)))

    fn = "{0}_{1}_{2}.root".format(dt, label, typ)
    array2root(x, fn, "tree", ["cls1", "cls2", "cls3"])

for ((dt, typ, label), d) in ds.items():
    fn = "{0}_{1}_{2}.root".format(dt, label, typ)
    d2 = ROOTData(
        filename=fn, treename="tree", label=label
    )
    d2.load()
    d.tree.AddFriend(d2.tree)
    ds_eval[(dt, typ, label)] = d2

validation_of = ROOT.TFile("out.root", "RECREATE")
validation_of.cd()

for ((dt, typ, label), d) in ds.items():
    fn = "{0}_{1}_{2}".format(dt, label, typ)
    rdir = validation_of.mkdir(fn)
    for cl, lims in [
        ("bd_csv1", (100, 0, 1)),
        ("bd_csv2", (100, 0, 1)),
        ("bd_jp", (100, 0, 2)),
        ("bd_sel", (100, 0, 1)),
        ("bd_smu", (100, 0, 1)),
        ("cls1", (100, -1, 1)),
        ("cls2", (100, -1, 1)),
        ("cls3", (100, -1, 1))
        ]:
        print dt, typ, label, cl
        #discriminator distribution
        h = d.hist(cl, lims, "1")
        rdir.cd()
        h = h.Clone("h_{0}".format(cl))
        h.Write()

        #cumulative
        hc = h.GetCumulative()
        hc = hc.Clone(h.GetName() + "_c")
        hc.Write()

validation_of.Close()
