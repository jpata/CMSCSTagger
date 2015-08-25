from collections import OrderedDict
import sklearn.ensemble
from sklearn.ensemble import GradientBoostingClassifier
import pandas
import numpy as np
import copy
import rootpy
from rootpy.plotting import Hist
import sys
sys.path.append("/Users/joosep/Documents/ROOTDataHelpers/python/")
import sklearn_to_tmva

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
        self.label = kwargs.get("label", None)
        
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
    # 
    # def cumulative(self, classifier, cls):
    #     return cum(self.data[cls][classifier])

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
    
def evaluate_sklearn(cls, data):
    ret = None
    for t in cls.cls.estimators_[:,0]:
        s = t.tree_.predict(np.array(data[cls.variables], dtype="float32")) / cls.cls.n_estimators * 10
        if ret is None:
            ret = s
        else:
            ret += s
    return 2.0/(1.0+np.exp(-2.0*ret))-1
