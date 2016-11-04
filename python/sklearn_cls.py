from collections import OrderedDict
from sklearn.ensemble import GradientBoostingClassifier
import pandas
import numpy as np
import copy
import rootpy
from rootpy.plotting import Hist
import sys

import xgboost

import sklearn.datasets
import sklearn.ensemble
import sklearn.model_selection
from sklearn.model_selection import cross_val_score
import sklearn.metrics
from sklearn.metrics import roc_curve
from sklearn.model_selection import ShuffleSplit

import pandas
import root_numpy as rnpy

import json

ptbins = np.linspace(20, 620, 41)
ptbins2 = np.array([20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 200, 240, 280, 320, 360])

etabins = np.linspace(0, 2.5, 41)
etabins2 = np.linspace(0, 2.5, 11)

cols_replacevals = {
    "Jet_CSV": {"replaceval_bad": 0, "replaceval_low": 0, "replaceval_high": 1},
    "Jet_CSVIVF": {"replaceval_bad": 0, "replaceval_low": 0, "replaceval_high": 1},
    "Jet_cMVA": {"replaceval_bad": -1, "replaceval_low": -1, "replaceval_high": 1},
    "Jet_JP": {"replaceval_bad": 0, "replaceval_low": 0, "replaceval_high": 5},
    "Jet_JBP": {"replaceval_bad": 0, "replaceval_low": 0, "replaceval_high": 15},
    "Jet_SoftMu": {"replaceval_bad": 0, "replaceval_low": 0, "replaceval_high": 1},
    "Jet_SoftEl": {"replaceval_bad": 0, "replaceval_low": 0, "replaceval_high": 1},
}

def normalize_col_inplace(data, col, replaceval_bad=0, replaceval_low=0, replaceval_high=1):
    """
    vals (numpy array): input values
    replaceval_bad (float): replace NaN, Inf with this value
    replaceval_low (float): set anything below x to x
    replaceval_high (float): set anything above x to x
    return vals
    """
    vals = data[col]
    data.loc[np.isnan(vals), col] = replaceval_bad
    data.loc[np.isinf(vals), col] = replaceval_bad
    data.loc[vals<replaceval_low, col] = replaceval_low
    data.loc[vals>replaceval_high, col] = replaceval_high
    return data

def normalize_all_cols(data, cols_replacevals):
    for col in data.columns:
        if cols_replacevals.has_key(col):
            normalize_col_inplace(data, col, **cols_replacevals[col])
    return data

def load_data(filename, treename, **kwargs):
    return pandas.DataFrame(
        rnpy.root2array(
            filename,
            treename = treename,
            **kwargs
        )
    )

def preprocess(data, train_frac=0.8):
    #Here we categorize the data according to the jet pdgId into 4 main groups
    data["flavour_category"] = 0
    data.loc[data["Jet_flavour"].abs() <= 3, "flavour_category"] = 0
    data.loc[data["Jet_flavour"].abs() == 4, "flavour_category"] = 1
    data.loc[data["Jet_flavour"].abs() == 5, "flavour_category"] = 2
    data.loc[data["Jet_flavour"].abs() == 21, "flavour_category"] = 0

    data["is_training"] = data["index"] < 9
    data["weight"] = 1.0

    data["ptbin"] = map(lambda x: ptbins.searchsorted(x), data["Jet_pt"])
    data["ptbin2"] = map(lambda x: ptbins2.searchsorted(x), data["Jet_pt"])
    data["etabin"] = map(lambda x: etabins.searchsorted(x), data["Jet_eta"].abs())
    data["etabin2"] = map(lambda x: etabins2.searchsorted(x), data["Jet_eta"].abs())

    normalize_all_cols(data, cols_replacevals)

    return data

def filter_data(data, expr):
    return data[data.eval(expr)]

def calc_weight_binary(data, target):
    sig = data[target] == 1
    bkg = data[target] == 0
    data.loc[sig, "weight"] = 1.0 / np.sum(sig)
    data.loc[bkg, "weight"] = 1.0 / np.sum(bkg)
    return data

def classifier(cls, kwargs):
    return cls(**kwargs)

def fit_classifier(cls, data, variables, target):
    cls.fit(
        data[variables].as_matrix(),
        data[target].as_matrix(),
        sample_weight=data["weight"].ravel()
    )
    return cls

def roc(cls, X, y_true):
    y_pred = evaluate_sklearn_X(cls, X)
    return roc_curve(y_true, y_pred)

def fit_classifier_CV(cls, data, variables, target):
    rets = []
    kf = KFold(n_splits = 5)
    X = data[variables].as_matrix()
    y = data[target].as_matrix()
    for train, test in kf.split(X):
        fitted = cls.fit(
            X[train],
            y[train],
            sample_weight=data["weight"][train]
        )
        fpr, tpr, thresh = roc(fitted, X[test], y[test])
        rets += [(tpr, fpr)]
    return rets

def evaluate_cls(cls, data, variables):
    return evaluate_sklearn(cls, data, variables)

def make_tuple(*args):
    return tuple(args)

def get_weights(df, ptbins, etabins):
    """Given a data frame, calculate the pt-eta weights
    to make the kinematic distributions flat.
    
    Args:
        df (DataFrame): jets
        ptbins (array): Bins in pt
        etabins (array): Bins in eta
    
    Returns:
        2d array: weight distribution
    """
    vs, bx, by = np.histogram2d(
        df["Jet_pt"],
        df["Jet_eta"].abs(),
        bins=[ptbins, etabins]
    )
    #normalize
    vs = vs / float(np.sum(vs))
    #invert
    ws = 1.0/vs
    #get rid of bad values
    ws[np.isnan(ws)]=0.0
    ws[np.isinf(ws)]=1
    return ws

def train_crossvalidation(cls, data_tuple):
    rets = []
    models = []
    kf = ShuffleSplit(n_splits = 5)
    X = data_tuple[0].as_matrix()
    y = data_tuple[1].as_matrix()
    for train, test in kf.split(X):
        fitted = cls.fit(
            X[train],
            y[train],
        )
        models += [fitted]
        fpr, tpr, _ = sklearn.metrics.roc_curve(
            y[test],
            fitted.predict_proba(X[test])[:, 1]
        )
        rets += [(tpr, fpr)]
    return rets

def train_variable_remove(cls, data_tuple_train, data_tuple_test):
    cols = data_tuple_train[0].columns
    rets = []
    varsets = []
    for c in cols:
        new_cols = copy.deepcopy(list(cols))
        new_cols.pop(new_cols.index(c))
        print new_cols
        cls.fit(
            data_tuple_train[0][new_cols],
            data_tuple_train[1],
            verbose=False,
        )
        fpr, tpr, _ = sklearn.metrics.roc_curve(
            data_tuple_test[1],
            cls.predict_proba(data_tuple_test[0][new_cols])[:, 1]
        )
        rets += [(tpr, fpr)]
        varsets += [c]
    return rets, varsets

def save_set(eval_set, fn):
    i = 0
    data = {}
    for a, b in eval_set:
        #bcolz.carray(a, rootdir="{0}_{1}_a".format(fn, i))
        #bcolz.carray(b, rootdir="{0}_{1}_b".format(fn, i))
        fna = "{0}_{1}.svmbin".format(fn, i)
        fi = open(fna, "wb")
        sklearn.datasets.dump_svmlight_file(a, b, fi)
        fi.close()
        data[i] = fna
        i += 1
    fi = open(fn + ".json", "w")
    json.dump(data, fi)
    fi.close()

def load_set(fn):
    print "load_set"
    fi = open(fn + ".json")
    data = json.load(fi)
    fi.close()
    eval_set = []
    for k in sorted(data.keys()):
        eval_set += [
            xgboost.DMatrix(data[k]+"#cache{0}".format(k))
        ]
    return eval_set

# class SKLearnClassifier:
#     def __init__(self, **kwargs):
#         self.name = kwargs.get("name")
#         self.variables = kwargs.get("variables")
#         #self.spectators = kwargs.get("spectators", [])
#         self.ntrees = kwargs.get("ntrees", 1200)
#         self.shrinkage = kwargs.get("shrinkage", 0.1)
#         self.max_depth = kwargs.get("max_depth", 3)
#         self.subsample = kwargs.get("subsample", 1.0)
#         #self.max_events = kwargs.get("max_events", None)
#         self.min_samples_split = kwargs.get("min_samples_split", 100)
#         self.min_samples_leaf = kwargs.get("min_samples_leaf", 100)
        
#         self.weight = kwargs.get("weight", None)
#         self.label = kwargs.get("label")
        
#         self.data = OrderedDict()

#     def prepare(self):
#         self.cls = GradientBoostingClassifier(
#             n_estimators=self.ntrees, learning_rate=self.shrinkage,
#             max_depth=self.max_depth,
#             min_samples_split=self.min_samples_split,
#             min_samples_leaf=self.min_samples_leaf,
#             subsample=self.subsample,
#             verbose=True
#         )
    
#     def add_data(self, data, class_name):
#         self.data[class_name] = data
        
#     def train(self):
#         ks = self.data.keys()
#         tot = pandas.concat(
#             [self.data[k] for k in ks], ignore_index=True
#         )
#         if self.weight:
#             self.cls.fit(tot[self.variables], tot[self.label], tot[self.weight])
#         else:
#             self.cls.fit(tot[self.variables], tot[self.label])

#     def evaluate(self, data):
#         return evaluate_sklearn(self, data)
        
#     def hists(self, bins, data, func, weight):
#         ret = OrderedDict()
#         for dn, d in data.items():
#             ret[dn] = Hist(*bins)
#             ret[dn].FillN(int(d.shape[0]), func(d).astype("float64"), weight(d).astype("float64"), 1)
#         return ret
        
#     def hists_cls(self, bins, data=None, weight="w"):
#         if not data:
#             data = self.data
#         return self.hists(bins, data, lambda d: self.evaluate(d), lambda d: d[weight].as_matrix())
        
# def evaluate_tmva(cls, data, weightfile="test.xml"):
#     sklearn_to_tmva.gbr_to_tmva(cls.cls, data[cls.variables], weightfile)
#     from ROOT import TMVA
#     import array
#     reader = TMVA.Reader("!V")
#     vardict = {}
#     for fn in cls.variables:
#         vardict[fn] = array.array("f", [0])
#         reader.AddVariable(fn, vardict[fn])
#     reader.BookMVA("bdt", weightfile)
    
#     xs = []
#     arr = data[cls.variables].as_matrix()
#     for i in range(len(data)):
#         for ivar, var in enumerate(cls.variables):
#             vardict[var][0] = arr[i, ivar]
#         x = reader.EvaluateMVA("bdt")
#         xs += [x]
#     return np.array(xs, dtype="float64")
    
# def evaluate_sklearn(cls, data, variables):
#     return evaluate_sklearn_X(cls, data[variables])

# def evaluate_sklearn_X(cls, X):
#     ret = None
#     for t in cls.estimators_[:,0]:
#         s = t.tree_.predict(np.array(X, dtype="float32")) / cls.n_estimators * 10
#         if ret is None:
#             ret = s
#         else:
#             ret += s
#     return 2.0/(1.0+np.exp(-2.0*ret))-1
