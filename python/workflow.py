import ROOT
ROOT.gROOT.cd()
ROOT.gROOT.SetBatch(True)

from supertagger_train import ROOTData, TMVABDTClassifier
import supertagger_train
import numpy as np
import multiprocessing
from roothelpers import array2root
from collections import OrderedDict

#path = "/Users/joosep/Documents/btv/data/"
path = "./data/"
ncores = 4
spectators = ["bd_cmva1", "bd_cmva2", "pt", "eta", "flavour"]

def load_data(path):
    data = OrderedDict()

    for dt in ["qcd", "ttjets", "ttjets2"]:
        for typ, kind in [
            ("testing", ROOT.TMVA.Types.kTesting),
            ("training", ROOT.TMVA.Types.kTraining)
        ]:
            for label, lt in [("b", "b"), ("c", "l"), ("l", "l")]:
                data[(dt, typ, label)] = ROOTData(
                    label=lt,
                    filename=path+"{0}_{1}_{2}.root".format(dt, label, typ),
                    treename="tree_{0}".format(label),
                    kind=kind
                )
    return data

def create_classifiers(ds):

    ret = OrderedDict()
    #Select a subregion of the full training data
    cls1 = TMVABDTClassifier(
        name="cls1",
        variables=["bd_csv1", "bd_csv2"],
        ntrees=2000,
        spectators=spectators,
        label_signal="b",
        cut="bd_csv1==bd_csv1 && bd_csv2==bd_csv2 && bd_csv1>=0 && bd_csv1<1 && bd_csv2>=0 && bd_csv2<1"
    )
    ret["cls1"] = cls1

    #Select a subregion of the full training data
    cls2 = TMVABDTClassifier(
        name="cls2",
        variables=["bd_csv1", "bd_csv2", "bd_jp", "bd_sel", "bd_smu"],
        ntrees=2000,
        spectators=spectators,
        label_signal="b",
        cut="bd_csv1==bd_csv1 && bd_csv2==bd_csv2 && bd_csv1>=-10 && bd_csv1<1 && bd_csv2>=-10 && bd_csv2<1 && bd_jp>=0 && bd_jp<5 && bd_sel>=-9999 && bd_sel<1 && bd_smu>=-9999 && bd_smu<1"
    )
    ret["cls2"] = cls2

    #Select a subregion of the full training data
    cls3 = TMVABDTClassifier(
        name="cls3",
        variables=["bd_csv1", "bd_csv2", "bd_jp", "bd_sel", "bd_smu"],
        ntrees=2000,
        spectators=spectators,
        weight="w1",
        label_signal="b",
        cut="w1==w1 && w1>0 && w1<10000000 && bd_csv1==bd_csv1 && bd_csv2==bd_csv2 && bd_csv1>=-10 && bd_csv1<1 && bd_csv2>=-10 && bd_csv2<1 && bd_jp>=0 && bd_jp<5 && bd_sel>=-9999 && bd_sel<1 && bd_smu>=-9999 && bd_smu<1"
    )
    ret["cls3"] = cls3

    #Select a subregion of the full training data
    cls4 = TMVABDTClassifier(
        name="cls4",
        variables=["bd_csv1", "bd_csv2", "bd_jp", "bd_sel", "bd_smu", "pt", "eta"],
        ntrees=2000,
        spectators=spectators,
        weight="w1",
        label_signal="b",
        cut="w1==w1 && w1>0 && w1<10000000 && bd_csv1==bd_csv1 && bd_csv2==bd_csv2 && bd_csv1>=-10 && bd_csv1<1 && bd_csv2>=-10 && bd_csv2<1 && bd_jp>=0 && bd_jp<5 && bd_sel>=-9999 && bd_sel<1 && bd_smu>=-9999 && bd_smu<1"
    )
    ret["cls4"] = cls4

    for dt in ["ttjets2"]:
        for typ, kind in [
            ("testing", ROOT.TMVA.Types.kTesting),
            ("training", ROOT.TMVA.Types.kTraining)
        ]:
            for label, lt in [("b", "b"), ("c", "l"), ("l", "l")]:
                d = ds[(dt, typ, label)]
                for cl in ret.values():
                    cl.add_data(d)

    return ret

def train(args):
    data, classifier = args
    for d in data.values():
        d.load()

    print "training {0}".format(classifier.name)
    classifier.prepare()
    classifier.train()
    print "done {0}".format(classifier.name)
    return classifier

def evaluate_classifiers(classifiers, data):
    ds_eval = OrderedDict()
    for ((dt, typ, label), d) in data.items():
        if not d.is_loaded:
            d.load()
        evals = tuple([c.evaluate(d) for c in classifiers.values()])
        x = np.hstack(evals)

        fn = "{0}_{1}_{2}.root".format(dt, label, typ)
        array2root(x, fn, "tree", classifiers.keys())

    for ((dt, typ, label), d) in data.items():
        fn = "{0}_{1}_{2}.root".format(dt, label, typ)
        d2 = ROOTData(
            filename=fn, treename="tree", label=label
        )
        print fn
        d2.load()
        assert(d.tree.GetEntries() == d2.tree.GetEntries())
        d.tree.AddFriend(d2.tree, "t2")
        ds_eval[(dt, typ, label)] = d2
    return ds_eval

def validate_classifiers(data, ofname="out.root"):

    validation_of = ROOT.TFile(ofname, "RECREATE")
    validation_of.cd()

    for ((dt, typ, label), d) in data.items():
        fn = "{0}_{1}_{2}".format(dt, label, typ)
        rdir = validation_of.mkdir(fn)
        for cutname, cut in [
            ("inclusive", "1"),
            ("pt_30_50", "pt>=30 && pt<50"),
            ("pt_50_70", "pt>=50 && pt<70"),
            ("pt_70_90", "pt>=70 && pt<90"),
            ("pt_90_110", "pt>=90 && pt<110"),
            ("pt_110_130", "pt>=110 && pt<130"),
            ("pt_130_150", "pt>=140 && pt<150"),
        ]:
            cdir = rdir.mkdir(cutname)
            for cl, lims in [
                ("pt", (100, 30, 530)),
                ("eta", (100, -2.5, 2.5)),
                ("bd_csv1", (100, 0, 1)),
                ("bd_csv2", (100, 0, 1)),
                ("bd_jp", (100, 0, 2)),
                ("bd_sel", (100, 0, 1)),
                ("bd_smu", (100, 0, 1)),
                ("bd_cmva1", (100, 0, 1)),
                ("bd_cmva2", (100, 0, 1)),
                ("cls1", (100, -1, 1)),
                ("cls2", (100, -1, 1)),
                ("cls3", (100, -1, 1)),
                ("cls4", (100, -1, 1)),
                ]:
                print dt, typ, label, cl
                #discriminator distribution
                h = d.hist(cl, lims, cut)
                cdir.cd()
                h = h.Clone("h_{0}".format(cl))
                h.Write()

                #cumulative
                hc = h.GetCumulative()
                hc = hc.Clone(h.GetName() + "_c")
                hc.Write()

    validation_of.Close()

def main():

    data = load_data(path)

    classifiers = create_classifiers(data)

    args = [
        (data, classifiers["cls1"]),
        (data, classifiers["cls2"]),
        (data, classifiers["cls3"]),
        (data, classifiers["cls4"]),
    ]

    print "training classifiers"
    if ncores > 1:
        pool = multiprocessing.Pool(4)
        res = pool.map(train, args)
    else:
        res = map(train, args)

    resd = OrderedDict()
    for r in res:
        resd[r.name] = r

    print "evaluating classifiers"
    #careful, you must keep a reference to ds_eval, otherwise any operations with
    #an AddFriend tree fail
    ds_eval = evaluate_classifiers(classifiers, data)

    print "validating classifiers"
    validate_classifiers(data)

if __name__=="__main__":
    main()
