from collections import OrderedDict
import sklearn.ensemble
from sklearn.ensemble import GradientBoostingClassifier
import pandas
import numpy as np
import copy
import rootpy
from rootpy.plotting import Hist

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
            self.cls.fit(tot[self.variables], tot["id"], tot[weight])
        else:
            self.cls.fit(tot[self.variables], tot["id"])

    def cumulative(self, classifier, cls):
        return cum(self.data[cls][classifier])
    
    def evaluate(self, data, nprob=0):
        inp = copy.deepcopy(data[self.variables])
        inp[np.isnan(inp)] = 0.0
        inp[np.isinf(inp)] = 0.0
        ret = self.cls.predict_proba(inp)[:, nprob]
        ret[np.isnan(ret)] = 0.0
        ret[np.isinf(ret)] = 0.0
        return ret

    def evaluate_multi(self, data):
        inp = copy.deepcopy(data[self.variables])
        inp[np.isnan(inp)] = 0.0
        inp[np.isinf(inp)] = 0.0
        ret = self.cls.predict_proba(inp)
        ret[np.isnan(ret)] = 0.0
        ret[np.isinf(ret)] = 0.0
        return ret
        
    def hists(self, bins, func, data=None):
        ret = OrderedDict()
        for dn, d in data.items():
            ret[dn] = Hist(*bins)
            ret[dn].FillN(len(d), func(d).astype("float64"), d["w"].as_matrix().astype("float64"))
        return ret
        
    def hists_cls(self, bins, data=None):
        if not data:
            data = self.data
        return self.hists(bins, lambda d: self.evaluate(d), data)
        
