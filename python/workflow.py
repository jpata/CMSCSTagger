from supertagger_train import ROOTData, TMVAClassifier, array2root
import numpy as np
from copy import deepcopy
import ROOT
from multiprocessing import Pool

steps = ["project", "train", "evaluate"]
#steps = ["train", "evaluate"]
#steps = ["evaluate"]

input_file = "jets.root"
output_file = "out.root"

spectators = ["pt_bin", "eta_bin"]
cls = [
    TMVAClassifier(
        name="cls1",
        variables=["csv1", "csv2"],
        data_classes=["l", "c", "b", "g"],
        ntrees=400,
        spectators=spectators
    ),

    # TMVAClassifier(
    #     name="cls2",
    #     variables=["csv1", "csv2"],
    #     data_classes=["l", "c", "b", "g"],
    #     ntrees=600,
    #     spectators=spectators
    # ),
    # 
    # TMVAClassifier(
    #     name="cls3",
    #     variables=["csv1", "csv2"],
    #     data_classes=["l", "c", "b", "g"],
    #     ntrees=800,
    #     spectators=spectators
    # ),
    # 
    # TMVAClassifier(
    #     name="cls4",
    #     variables=["csv1", "csv2"],
    #     data_classes=["l", "c", "b", "g"],
    #     ntrees=1000,
    #     spectators=spectators
    # ),
    # 
    # TMVAClassifier(
    #     name="cls5",
    #     variables=["csv1", "csv2"],
    #     data_classes=["l", "c", "b", "g"],
    #     ntrees=1200,
    #     spectators=spectators
    # )
]

data = ROOTData(filename="jets.root", treename="tree")
print "full data", len(data)

#Create a temporary file to avoid creating root ttrees in memory
temp = ROOT.TFile("tempfile.root", "RECREATE")
temp.cd()

if "project" in steps:
    #Select a subregion of the full training data
    # subdata = data.selection(
    #     partition=[0, 100000]
    # )
    subdata = data.selection()
    subdata.tfile = temp
    subdata.tree.SetName("subdata")
    subdata.tree.SetDirectory(temp)
    subdata.tree.Write("", ROOT.TObject.kOverwrite)
    
    #create datasets based on classes
    print "creating training classes"
    datas_cls = {
        "b": subdata.selection(
            selection="abs(flavour)==5"
        ),
        "c": subdata.selection(
            selection="abs(flavour)==4"
        ),
        "l": subdata.selection(
            selection="abs(flavour)<4"
        ),
        "g": subdata.selection(
            selection="abs(flavour)==21"
        ),
    }
    for k, d in datas_cls.items():
        print k, d.tree.GetEntries()
        d.tree.SetName("subdata_cls_{0}".format(k))
        d.tree.SetDirectory(temp)
        d.tree.Write("", ROOT.TObject.kOverwrite)

if "train" in steps:    
    print "creating classifier"

    def train(kwargs):
        c = kwargs.get("classifier")
        #data_dict = kwargs.get("data")
        c.prepare()
        c.add_class("l", datas_cls["l"])
        c.add_class("c", datas_cls["c"])
        c.add_class("b", datas_cls["b"])
        c.add_class("g", datas_cls["g"])
        c.train()
        return c
        
    pool = Pool(4)
    cls = map(train, [
        {"classifier":cls[i]} for i in range(len(cls))
    ])


if "evaluate" in steps:
    for c in cls:
        dtest = ROOTData(filename=c.out_file, treename="TestTree")
        dtrain = ROOTData(filename=c.out_file, treename="TrainTree")
        
        for dn, d in [("test", dtest), ("train", dtrain)]:
            ev = c.evaluate(d)
            array2root(
                ev,
                "outputs/TMVAMulticlass_" + c.name + "_" + dn + ".root",
                "tree",
                colnames=["prob_b", "prob_c", "prob_l"]
            )
temp.Write()
temp.Close()
