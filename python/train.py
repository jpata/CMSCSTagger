import sys
import cPickle as pickle

#remove problematic cmssw python packages
newpath = []
for x in sys.path:
    if "/cvmfs/cms.cern.ch/" and "pandas" in x:
        continue
    newpath += [x]
sys.path = newpath

from collections import OrderedDict

location = "jpata-macbook"

if location=="jpata-macbook":
    sys.path.append("/Users/joosep/Documents/btv/CMSSW_7_4_5/src/RecoBTag/CombinedMVA/python/")
    sys.path.append("/Users/joosep/Documents/ROOTDataHelpers/")
elif location=="phys":
    sys.path.append("/home/joosep/btv/CMSSW_7_4_5/src/RecoBTag/CombinedMVA/python/")
    sys.path.append("/home/joosep/btv/CMSSW_7_4_5/src/RecoBTag/ROOTDataHelpers/python/")

import numpy as np
import root_numpy as rnpy
import matplotlib.pyplot as plt
import pandas
import sklearn
import sklearn_cls
from sklearn_cls import SKLearnClassifier
from xglearn import XGBoostClassifier
from matplotlib.colors import LogNorm
import rootpy
import rootpy.plotting
from sklearn import metrics
import ROOT


ptbins = np.linspace(20,620, 41)
ptbins2 = np.array([20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 200, 240, 280, 320, 360])

etabins = np.linspace(0, 2.5, 41)
etabins2 = np.linspace(0, 2.5, 11)

def load_dataset(fn, treename, i):
    arr = rnpy.root2rec(
        fn,
        selection="Jet_pt>20",
        #branches=["Jet_pt", "Jet_eta", "Jet_flavour"],
        branches=[
            "Jet_pt", "Jet_eta", "Jet_flavour", "Jet_CSV", "Jet_CSVIVF",
            "Jet_CombMVA", "Jet_CombMVANEW", "Jet_CombMVAETH", "Jet_SoftMu",
            "Jet_SoftEl", "Jet_JP", "Jet_JBP", "TagVarCSV_vertexCategory"
        ],
        treename=treename,
        #start=0,
        #stop=50000
    )
    df = pandas.DataFrame(arr)
    df["id"] = i
    df[np.isnan(df)] = 0.0
    df[np.isinf(df)] = 0.0
    for c in ["Jet_CSV", "Jet_CSVIVF", "Jet_SoftEl", "Jet_SoftMu"]:
        df.loc[df[c]<=0, c] = 0
        df.loc[df[c]>=1, c] = 1
    df["abs_eta"] = df["Jet_eta"].abs()
    df["training"] = 0
    
    perminds = np.random.permutation(df.index)
    df.loc[perminds[:len(perminds)/2], "training"] = 1
    df["ptbin"] = map(lambda x: ptbins.searchsorted(x), df["Jet_pt"])
    df["ptbin2"] = map(lambda x: ptbins2.searchsorted(x), df["Jet_pt"])
    df["etabin"] = map(lambda x: etabins.searchsorted(x), df["abs_eta"])
    df["etabin2"] = map(lambda x: etabins2.searchsorted(x), df["abs_eta"])
    df["w"] = 1.0
    return df

def calc_roc(h1, h2):
    h1 = h1.Clone()
    h2 = h2.Clone()
    h1.Scale(1.0 / h1.Integral())
    h2.Scale(1.0 / h2.Integral())
    roc = np.zeros((h1.GetNbinsX()+2, 2))
    err = np.zeros((h1.GetNbinsX()+2, 2))
    e1 = ROOT.Double(0)
    e2 = ROOT.Double(0)
    for i in range(0, h1.GetNbinsX()+2):
        I1 = h1.Integral(0, h1.GetNbinsX())
        I2 = h2.Integral(0, h2.GetNbinsX())
        if I1>0 and I2>0:
            roc[i, 0] = float(h1.IntegralAndError(i, h1.GetNbinsX()+2, e1)) / I1
            roc[i, 1] = float(h2.IntegralAndError(i, h1.GetNbinsX()+2, e2)) / I2
            err[i, 0] = e1
            err[i, 1] = e2
    return roc, err
    
def draw_rocs(pairs, **kwargs):
    rebin = kwargs.get("rebin", 1) 
    rs = []
    es = []
    for pair in pairs:
        h1, h2, label, pl_args = pair
        h1.rebin(rebin)
        h2.rebin(rebin)
        r, e = calc_roc(h1, h2)
        rs += [r]
        es += [e]

    ret = []
    for (r, e, pair) in zip(rs, es, pairs):
        h1, h2, label, pl_args = pair
        c1 = rootpy.asrootpy(h1.GetCumulative())
        c2 = rootpy.asrootpy(h2.GetCumulative())
        c1.Scale(1.0 / h1.Integral())
        c2.Scale(1.0 / h2.Integral())
        bx = list(c1.y())
        by = list(c2.y())
        a = 1.0 - sklearn.metrics.auc(bx, by)
        #plt.errorbar(r[:, 0], r[:, 1], e[:, 0], e[:, 1], label=label)
        r = plt.plot(r[:, 0], r[:, 1], label=label, **pl_args)
        ret += [r]
    return ret
    plt.legend(loc=2)
    
def plot_overtraining(clf, fname):
    X_test = d_testing[clf.variables]
    y_test = d_testing["id"]

    X_train = d_training[clf.variables]
    y_train = d_training["id"]
    
    test_score = np.zeros((clf.cls.n_estimators, ), dtype=np.float64)
    train_score = np.zeros((clf.cls.n_estimators, ), dtype=np.float64)

    for i, y_pred in enumerate(clf.cls.staged_decision_function(X_test)):
        test_score[i] = clf.cls.loss_(y_test, y_pred)

    for i, y_pred in enumerate(clf.cls.staged_decision_function(X_train)):
        train_score[i] = clf.cls.loss_(y_train, y_pred)
    
    plt.figure()
    plt.plot(test_score - train_score)
    plt.ylabel("$L_{test} - L_{train}$", fontsize=16)
    plt.xlabel("boosting step", fontsize=16)
    plt.grid()
    plt.savefig("overtrain.pdf")


def plot_test_training(h_ts, h_tr, fname):
    plt.figure(figsize=(6,6))
    plt.grid()
    r = draw_rocs([
        (h_ts["b"], h_ts["l"], "testing", {"color":"red"}),
        (h_tr["b"], h_tr["l"], "training", {"color":"green"}),
    ])

    plt.legend(loc=4)
    r = draw_rocs([
        (h_ts["b"], h_ts["c"], "testing", {"color":"red"}),
        (h_tr["b"], h_tr["c"], "training", {"color":"green"}),
    ])

    plt.yscale("log")

    a = np.linspace(0.1, 1.0, 5)
    a = [0.001] + list(a)
    plt.yticks(a, a)
    plt.xlim(0.3,1.0)
    plt.ylim(0.001,1.0)
    plt.xticks(np.linspace(0.3,1.0,8))
    plt.ylabel("udsg(c)-jet efficiency", fontsize=16)
    plt.xlabel("b jet efficiency", fontsize=16)
    plt.title(u"cMVA performance in $t\\bar{t}$+jets", fontsize=14)
    plt.savefig(fname)

def load_from_mmap(fn_metadata, fn_mmap):
    md = open(fn_metadata, "r")
    (shape, columns, dtypes) = pickle.load(md)
    md.close()
    mp = np.memmap(fn_mmap, dtype='float32', mode='r', shape=shape)
    d = pandas.DataFrame(mp, columns=columns, dtype=dtypes)
    return d
def save_to_mmap(fn_metadata, fn_mmap):
    mp = np.memmap(fn_mmap, dtype='float32', mode='w+', shape=d.shape)
    mp[:] = d.as_matrix().astype("float32")[:]
    md = open(fn_metadata, "w")
    pickle.dump((d.shape, d.columns, d.dtypes), md)
    md.close()


def cum(arr, nb=100000):
    h = np.histogram(
        arr,
        bins=np.linspace(-1, 1, nb)
    )
    h = h[0]
    h = h / float(np.sum(h))
    h = np.cumsum(h)
    return h

def get_eff_at(a, b, x):
    idx = a.searchsorted(x)
    return b[idx]
    
def cls_ds_metrics(clss, d1, d2):
    hists = {}
    for cls in clss:
        ca = cum(cls.evaluate(d1))
        cb = cum(cls.evaluate(d2))
        hists[cls.name] = (ca, cb)

    for v in ["Jet_CSVIVF", "Jet_CombMVANEW", "Jet_CombMVAETH"]:
        ca = cum(d1[v])
        cb = cum(d2[v])
        hists[v] = (ca, cb)
    ret = {}
    for v in hists.keys():
        ret[v] = {}
        ret[v]["AUC"] = 1.0 - metrics.auc(hists[v][0], hists[v][1])
        ret[v]["e50"] = 1.0 - get_eff_at(hists[v][0], hists[v][1], 1.0 - 0.5)
        ret[v]["e90"] = 1.0 - get_eff_at(hists[v][0], hists[v][1], 1.0 - 0.9)

        ret[v]["f0.01"] = 1.0 - get_eff_at(hists[v][1], hists[v][0], 1.0 - 0.01)
        ret[v]["f0.1"] = 1.0 - get_eff_at(hists[v][1], hists[v][0], 1.0 - 0.1)
        ret[v]["f0.3"] = 1.0 - get_eff_at(hists[v][1], hists[v][0], 1.0 - 0.3)

    return ret


def draw_comparison(xs1, bins, xlabel, ylabel, v, fname):
    plt.figure(figsize=(6,6))

    ax = plt.axes([0,0.52,1.0,0.5])
    ax.grid()
    
    for clf in classifiers:
        ax.plot(bins[xs1.keys()-1], [x[clf.name][v] for x in xs1], label=clf.name, ms=0, marker="x", lw=1, color=clf.color)
        
    ax.plot(bins[xs1.keys()-1], [x["Jet_CSVIVF"][v] for x in xs1], label="IVF", ms=0, marker="^", lw=2, color="black")
    ax.plot(bins[xs1.keys()-1], [x["Jet_CombMVANEW"][v] for x in xs1], label="cMVA", ms=0, marker="^", lw=1, color="orange")
    ax.plot(bins[xs1.keys()-1], [x["Jet_CombMVAETH"][v] for x in xs1], label="cMVA v2", ms=0, marker="^", lw=2, color="darkred", ls="--")
    ax.legend(loc="best")

    ax.set_ylabel(ylabel, fontsize=16)

    ax = plt.axes([0,0.0,1.0,0.48], sharex=ax)
    ax.grid()

    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel("classifier wrt. cMVA", fontsize=16)

    for clf in classifiers:
        ax.plot(bins[xs1.keys()-1], [x[clf.name][v]/ x["Jet_CombMVANEW"][v] for x in xs1], ms=0, marker="^", lw=1, color=clf.color)
        
    ax.plot(bins[xs1.keys()-1], [x["Jet_CSVIVF"][v]/ x["Jet_CombMVANEW"][v] for x in xs1], ms=0, marker="^", lw=2, color="black")
    ax.plot(bins[xs1.keys()-1], [x["Jet_CombMVAETH"][v]/ x["Jet_CombMVANEW"][v] for x in xs1], ms=0, marker="^", lw=2, color="darkred", ls="--")

    #ax.plot(bins[xs1.keys()-1], [x["c1"][v]/ x["Jet_CombMVANEW"][v] for x in xs1], ms=0, marker="^", lw=1, color="gray")
    #ax.plot(bins[xs1.keys()-1], [x["c2"][v]/ x["Jet_CombMVANEW"][v] for x in xs1], ms=0, marker="^", lw=1, color="purple")
    #ax.plot(bins[xs1.keys()-1], [x["c3"][v]/ x["Jet_CombMVANEW"][v] for x in xs1], ms=0, marker="^", lw=1, color="blue")
    #ax.plot(bins[xs1.keys()-1], [x["c4"][v]/ x["Jet_CombMVANEW"][v] for x in xs1], ms=0, marker="^", lw=1, color="cyan")
    ax.axhline(1.0, color="orange", lw=2)
    #ax.set_ylim(top=1.2)
    plt.savefig(fname, bbox_inches='tight')
    
    
if __name__ == "__main__":
    if location == "jpata-macbook":
        path = "/Users/joosep/Documents/btv/data/aug10/"
    elif location == "phys":
        path = "/home/joosep/btv/CMSSW_7_4_5/src/RecoBTag/CombinedMVA/"

    memmap_fn = "data.mmap"
    load_mmap = True
        
    if not load_mmap:
        print "loading data..."
        d1 = load_dataset(path + "ttjets_b_10M.root", "tree_b", 2)
        d2 = load_dataset(path + "ttjets_c_10M.root", "tree_c", 1)
        d3 = load_dataset(path + "ttjets_l_10M.root", "tree_l", 0)
        d = pandas.concat((d1, d2, d3))
        print "saving memmap..."
        save_to_mmap("metadata.pkl", "data.mmap")
    else:
        print "loading memmap..."
        d = load_from_mmap("metadata.pkl", "data.mmap")

    print "reweighting..."
    #d["w2"] = d["w"]
    #d.loc[d["id"] == 0, "w2"] *= 0.5
    #d.loc[d["id"] == 1, "w2"] *= 0.5
    d["l1"] = (d["id"]==2).astype("float32")
    
    print "splitting test/train"
    d_training = d[d["training"]==1]
    d_testing = d[d["training"]==0]
    
    print "shuffling..."
    d_training_shuf = d_training.iloc[np.random.permutation(len(d_training))]

    classifiers = []
    print "training clf1"
    clf1 = SKLearnClassifier(
        name="clf1",
        variables=["Jet_pt", "Jet_eta", "Jet_CSV", "Jet_CSVIVF", "Jet_JP", "Jet_JBP", "Jet_SoftMu", "Jet_SoftEl"],
        ntrees=200,
        weight="w",
        shrinkage=0.2,
        label="l1"
    )
    clf1.add_data(d_training_shuf[d_training_shuf["id"] == 2], "b")
    clf1.add_data(d_training_shuf[d_training_shuf["id"] == 0], "udsg")
    clf1.add_data(d_training_shuf[d_training_shuf["id"] == 1], "c")
    clf1.prepare()
    clf1.train()
    classifiers += [clf1]
    
    # clf2 = SKLearnClassifier(
    #     name="clf2",
    #     variables=["Jet_pt", "Jet_eta", "Jet_CSV", "Jet_CSVIVF", "Jet_JP", "Jet_JBP", "Jet_SoftMu", "Jet_SoftEl"],
    #     weight="w2",
    #     shrinkage=0.1,
    #     ntrees=200,
    #     label="l1"
    # 
    # )
    # clf2.add_data(d_training_shuf[d_training_shuf["id"] == 2], "b")
    # clf2.add_data(d_training_shuf[d_training_shuf["id"] == 0], "udsg")
    # clf2.add_data(d_training_shuf[d_training_shuf["id"] == 1], "c")
    # clf2.prepare()
    # clf2.train()
    # classifiers += [clf2]

    print "training clf3"
    clf3 = XGBoostClassifier(
        name="clf3",
        variables=["Jet_pt", "Jet_eta", "Jet_CSV", "Jet_CSVIVF", "Jet_JP", "Jet_JBP", "Jet_SoftMu", "Jet_SoftEl"],
        weight="w",
        shrinkage=0.2,
        ntrees=200,
        gamma=1.0,
        label="l1"

    )
    clf3.add_data(d_training_shuf[d_training_shuf["id"] == 2], "b")
    clf3.add_data(d_training_shuf[d_training_shuf["id"] == 0], "udsg")
    clf3.add_data(d_training_shuf[d_training_shuf["id"] == 1], "c")
    
    clf3.add_data(d_testing[d_testing["id"] == 2], "b", "testing")
    clf3.add_data(d_testing[d_testing["id"] == 0], "udsg", "testing")
    clf3.add_data(d_testing[d_testing["id"] == 1], "c", "testing")
    clf3.prepare()
    clf3.train()
    classifiers += [clf3]

    md = {
        "b": d_testing[d_testing["id"] == 2],
        "l": d_testing[d_testing["id"] == 0],
        "c": d_testing[d_testing["id"] == 1]
    }

    md_tr = {
        "b": d_training[d_training["id"] == 2],
        "l": d_training[d_training["id"] == 0],
        "c": d_training[d_training["id"] == 1]
    }


    hists = []
    for clf in classifiers:
        h_ts = clf.hists_cls((1000,-1,1), md)
        h_tr = clf.hists_cls((1000,-1,1), md_tr)
        hists += [(clf, h_ts, h_tr)]
        plot_test_training(h_ts, h_tr, "plots/{0}/overtrain2.pdf".format(clf.name))

    
    clf = classifiers[0]
    h01 = clf.hists((1000,0,1), md, lambda d: d["Jet_CombMVANEW"].as_matrix(), lambda d: d["w"].as_matrix())
    h02 = clf.hists((1000,-1,1), md, lambda d: d["Jet_CombMVAETH"].as_matrix(), lambda d: d["w"].as_matrix())
    h03 = clf.hists((1000,0,1), md, lambda d: d["Jet_CSVIVF"].as_matrix(), lambda d: d["w"].as_matrix())

###
### ROCs
###
    plt.figure(figsize=(10,10))
    plt.grid()
    
    cls_plots_l = []
    cls_plots_c = []
    colors = ["darkblue", "darkgreen", "violet"]
    for (icl, (clf, h_ts, h_tr)) in enumerate(hists):
        cls_plots_l += [
            (h_ts["b"], h_ts["l"], clf.name, {"color": colors[icl], "lw":1})
        ]
        cls_plots_c += [
            (h_ts["b"], h_ts["c"], clf.name, {"color": colors[icl], "lw":1})
        ]
        clf.color = colors[icl]
        
    r = draw_rocs([
        (h03["b"], h03["l"], "IVF", {"color":"black", "lw":1}),
        (h01["b"], h01["l"], "cMVA", {"color":"orange"}),
        (h02["b"], h02["l"], "cMVA v2", {"color":"darkred", "lw":2, "ls":"--"}),
    ] + cls_plots_l)

    plt.legend(loc="best")
    r = draw_rocs([
        (h03["b"], h03["c"], "IVF", {"color":"black", "lw":1}),
        (h01["b"], h01["c"], "cMVA", {"color":"orange"}),
        (h02["b"], h02["c"], "cMVA v2", {"color":"darkred", "lw":2, "ls":"--"}),
    ] + cls_plots_c)

    plt.yscale("log")

    a = np.linspace(0.1, 1.0, 5)
    a = [0.001] + list(a)
    plt.yticks(a, a)
    plt.xlim(0.3,1.0)
    plt.ylim(0.001,1.0)
    plt.axhline(0.01, color="black", ls="--")
    plt.axhline(0.1, color="black", ls="--")

    plt.xticks(np.linspace(0.3,1.0,8))
    plt.ylabel("udsg(c)-jet efficiency", fontsize=16)
    plt.xlabel("b jet efficiency", fontsize=16)
    plt.title(u"cMVA performance in $t\\bar{t}$+jets", fontsize=14)
    plt.savefig("plots/mva.pdf")

    gpt1 = d_testing.groupby("ptbin2")
    gpt2 = d_testing.groupby("etabin2")
    
    xs_l = gpt1.apply(lambda d: cls_ds_metrics(classifiers, d[d["id"]==2], d[d["id"]==0]))
    xs_c = gpt1.apply(lambda d: cls_ds_metrics(classifiers, d[d["id"]==2], d[d["id"]==1]))
        
    draw_comparison(xs_l, ptbins2,
        "jet $p_T$ [GeV]",
        "AUC udsg",
        "AUC",
        "plots/auc_l_pt.pdf"
    )

    draw_comparison(xs_c, ptbins2,
        "jet $p_T$ [GeV]",
        "AUC c",
        "AUC",
        "plots/auc_c_pt.pdf"
    )

    draw_comparison(xs_l, ptbins2,
        "jet $p_T$ [GeV]",
        "b eff at 10% udsg mistag",
        "f0.1",
        "plots/eff_b_udsg_M.pdf"
    )

    draw_comparison(xs_l, ptbins2,
        "jet $p_T$ [GeV]",
        "b eff at 1% udsg mistag",
        "f0.01",
        "plots/eff_b_udsg_T.pdf"
    )

    draw_comparison(xs_c, ptbins2,
        "jet $p_T$ [GeV]",
        "b eff at 30% c mistag",
        "f0.3",
        "plots/eff_b_c_M.pdf"
    )
