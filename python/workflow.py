from supertagger_train import ROOTData, TMVAClassifier, array2root
import numpy as np
from copy import deepcopy
import ROOT
from multiprocessing import Pool
import glob

#steps = ["project", "train", "evaluate"]
steps = ["train", "evaluate"]
#steps = ["evaluate"]

input_file = "jets.root"
output_file = "out.root"

spectators = ["pt_bin", "eta_bin"]

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

datas = [
    ROOTData(
        filename=fn, treename="tree", name="f_{0}".format(fn.split(".")[0])
    ) for ifn, fn in enumerate(glob.glob("tree_*.root"))
]

#Create a temporary file to avoid creating root ttrees in memory
temp = ROOT.TFile("tempfile.root", "RECREATE")
temp.cd()

cls = {}
datas_cls = {}

if "train" in steps:    
    print "creating classifier"
    
    #Select a subregion of the full training data
    for data in datas:
        _cls = [TMVAClassifier(
            name="cls1",
            data_name=data.name,
            variables=["csv1", "csv2"],
            data_classes=["l", "c", "b", "g"],
            ntrees=200,
            spectators=spectators
        )]
        
        #create datasets based on classes
        print "creating training classes", data.name
        _data = {
            "b": data.selection(
                selection="abs(flavour)==5"
            ),
            "c": data.selection(
                selection="abs(flavour)==4"
            ),
            "l": data.selection(
                selection="abs(flavour)<4"
            ),
            "g": data.selection(
                selection="abs(flavour)==21"
            ),
        }
        skip = False
        for k, d in _data.items():
            if d.tree.GetEntries() < 10:
                skip = True
                print "Skipping", data.name
            d.tree.SetName("subdata_cls_{0}".format(k))
            d.tree.SetDirectory(temp)
            d.tree.Write("", ROOT.TObject.kOverwrite)
        if not skip:
            datas_cls[data.name] = _data
            cls[data.name] = _cls
    def train(kwargs):
        c = kwargs.get("classifier")
        dname = c.data_name
        #data_dict = kwargs.get("data")
        c.prepare()
        c.add_class("l", datas_cls[dname]["l"])
        c.add_class("c", datas_cls[dname]["c"])
        c.add_class("b", datas_cls[dname]["b"])
        c.add_class("g", datas_cls[dname]["g"])
        c.train()
        return c
        
    pool = Pool(4)
    clss = []
    for c in cls.values():
        print c
        clss += c
    cls = pool.map(train, [
        {"classifier":clss[i]} for i in range(len(clss))
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
