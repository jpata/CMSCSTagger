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
        self.data_name = kwargs.get("data_name")
        self.mva_name = "bdt_" + self.name + "_" + self.data_name

        self.variables = kwargs.get("variables")
        self.spectators = kwargs.get("spectators", [])

        self.ntrees = kwargs.get("ntrees", 1200)
        self.shrinkage = kwargs.get("shrinkage", 0.1)
        #self.bag_fraction = kwargs.get("bag_fraction", 0.5)
        #self.ncuts = kwargs.get("ncuts", 50)
        self.max_depth = kwargs.get("max_depth", 3)
        self.data_classes = kwargs.get("data_classes", [])
        self.subsample = kwargs.get("subsample", 1.0)
        self.max_events = kwargs.get("max_events", None)
        self.min_samples_split = kwargs.get("min_samples_split", 100)
        self.min_samples_leaf = kwargs.get("min_samples_leaf", 100)
        
        self.weight = kwargs.get("weight", None)
        self.label_signal = kwargs.get("label_signal", None)
        
        self.data = OrderedDict()
        self.class_id = 0

    def prepare(self):
        self.cls = GradientBoostingClassifier(
            n_estimators=self.ntrees, learning_rate=self.shrinkage,
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            subsample=self.subsample,
            verbose=True
        )
    
    def add_data(self, data, class_name, cls_id):
        d = pandas.DataFrame(
            data[self.variables+["w"]]
        )
        d["id"] = cls_id
        self.data[class_name] = d
        
    def train(self):
        ks = self.data.keys()
        tot = pandas.concat(
            [self.data[k] for k in ks], ignore_index=True
        )
        if self.weight:
            self.cls.fit(tot[self.variables], tot["id"], tot[self.weight])
        else:
            self.cls.fit(tot[self.variables], tot["id"])

    def cumulative(self, classifier, cls):
        return cum(self.data[cls][classifier])
    # 
    # def evaluate(self, data, nprob=0):
    #     inp = copy.deepcopy(data[self.variables])
    #     inp[np.isnan(inp)] = 0.0
    #     inp[np.isinf(inp)] = 0.0
    #     ret = self.cls.predict_proba(inp)[:, nprob]
    #     ret[np.isnan(ret)] = 0.0
    #     ret[np.isinf(ret)] = 0.0
    #     return ret
    def evaluate(self, data):
        return evaluate_sklearn(self, data)
        
    def hists(self, bins, func, weight, data=None):
        ret = OrderedDict()
        for dn, d in data.items():
            ret[dn] = Hist(*bins)
            ret[dn].FillN(int(d.shape[0]), func(d).astype("float64"), weight(d).astype("float64"), 1)
        return ret
        
    def hists_cls(self, bins, data=None):
        if not data:
            data = self.data
        return self.hists(bins, lambda d: self.evaluate(d), lambda d: d["w"].as_matrix(), data)
        
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
