from collections import OrderedDict
import sklearn.ensemble
from sklearn.ensemble import GradientBoostingClassifier
import pandas
import numpy as np
import copy
import rootpy
from rootpy.plotting import Hist
import sys
#import sklearn_to_tmva
import sklearn.model_selection
from sklearn.model_selection import cross_val_score
import sklearn.metrics
from sklearn.metrics import roc_curve
from sklearn.model_selection import KFold

import pandas
import root_numpy as rnpy

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

def load_data(filename, treename, start, stop, branches, selection):
    return pandas.DataFrame(
        rnpy.root2array(
            filename,
            treename = treename,
            start = start,
            stop = stop,
            branches = branches,
            selection = selection
        )
    )

def preprocess(data):
    #Here we categorize the data according to the jet pdgId into 4 main groups
    data["Jet_flavour_abs"] = data["Jet_flavour"].abs().astype(np.int)
    data["flavour_category"] = ""
    data.loc[data["Jet_flavour_abs"] <= 3, "flavour_category"] = "light"
    data.loc[data["Jet_flavour_abs"] == 4, "flavour_category"] = "charm"
    data.loc[data["Jet_flavour_abs"] == 5, "flavour_category"] = "bhad"
    data.loc[data["Jet_flavour_abs"] == 21, "flavour_category"] = "gluon"
    data["is_b"] = data["flavour_category"] == "bhad"

    data["is_training"] = 1
    data["weight"] = 1.0


    data.loc[int(0.8*len(data)):, "is_training"] = 0

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

class SKLearnClassifier:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.variables = kwargs.get("variables")
        #self.spectators = kwargs.get("spectators", [])
        self.ntrees = kwargs.get("ntrees", 1200)
        self.shrinkage = kwargs.get("shrinkage", 0.1)
        self.max_depth = kwargs.get("max_depth", 3)
        self.subsample = kwargs.get("subsample", 1.0)
        #self.max_events = kwargs.get("max_events", None)
        self.min_samples_split = kwargs.get("min_samples_split", 100)
        self.min_samples_leaf = kwargs.get("min_samples_leaf", 100)
        
        self.weight = kwargs.get("weight", None)
        self.label = kwargs.get("label")
        
        self.data = OrderedDict()

    def prepare(self):
        self.cls = GradientBoostingClassifier(
            n_estimators=self.ntrees, learning_rate=self.shrinkage,
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            subsample=self.subsample,
            verbose=True
        )
    
    def add_data(self, data, class_name):
        self.data[class_name] = data
        
    def train(self):
        ks = self.data.keys()
        tot = pandas.concat(
            [self.data[k] for k in ks], ignore_index=True
        )
        if self.weight:
            self.cls.fit(tot[self.variables], tot[self.label], tot[self.weight])
        else:
            self.cls.fit(tot[self.variables], tot[self.label])

    def evaluate(self, data):
        return evaluate_sklearn(self, data)
        
    def hists(self, bins, data, func, weight):
        ret = OrderedDict()
        for dn, d in data.items():
            ret[dn] = Hist(*bins)
            ret[dn].FillN(int(d.shape[0]), func(d).astype("float64"), weight(d).astype("float64"), 1)
        return ret
        
    def hists_cls(self, bins, data=None, weight="w"):
        if not data:
            data = self.data
        return self.hists(bins, data, lambda d: self.evaluate(d), lambda d: d[weight].as_matrix())
        
def evaluate_tmva(cls, data, weightfile="test.xml"):
    sklearn_to_tmva.gbr_to_tmva(cls.cls, data[cls.variables], weightfile)
    from ROOT import TMVA
    import array
    reader = TMVA.Reader("!V")
    vardict = {}
    for fn in cls.variables:
        vardict[fn] = array.array("f", [0])
        reader.AddVariable(fn, vardict[fn])
    reader.BookMVA("bdt", weightfile)
    
    xs = []
    arr = data[cls.variables].as_matrix()
    for i in range(len(data)):
        for ivar, var in enumerate(cls.variables):
            vardict[var][0] = arr[i, ivar]
        x = reader.EvaluateMVA("bdt")
        xs += [x]
    return np.array(xs, dtype="float64")
    
def evaluate_sklearn(cls, data, variables):
    return evaluate_sklearn_X(cls, data[variables])

def evaluate_sklearn_X(cls, X):
    ret = None
    for t in cls.estimators_[:,0]:
        s = t.tree_.predict(np.array(X, dtype="float32")) / cls.n_estimators * 10
        if ret is None:
            ret = s
        else:
            ret += s
    return 2.0/(1.0+np.exp(-2.0*ret))-1
