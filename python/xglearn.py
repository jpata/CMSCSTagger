import pandas
import numpy as np
from collections import OrderedDict
import sys
#sys.path.append("/Users/joosep/Documents/xgboost/wrapper/")
sys.path.append("/home/joosep/local-sl6/xgboost/wrapper/")
import xgboost as xgb
from rootpy.plotting import Hist


class XGBoostClassifier:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.variables = kwargs.get("variables")
        #self.spectators = kwargs.get("spectators", [])
        self.ntrees = kwargs.get("ntrees", 200)
        self.shrinkage = kwargs.get("shrinkage", 0.1)
        self.max_depth = kwargs.get("max_depth", 3)
        self.subsample = kwargs.get("subsample", 1.0)
        self.gamma = kwargs.get("gamma", 0.0)
        #self.min_samples_split = kwargs.get("min_samples_split", 100)
        self.min_samples_leaf = kwargs.get("min_samples_leaf", 100)
        
        self.weight = kwargs.get("weight", None)
        self.label = kwargs.get("label", None)
        
        self.data = OrderedDict()
        self.data_testing = OrderedDict()
        
        self.param = {
            'bst:max_depth': self.max_depth,
            'bst:eta': self.shrinkage,
            'bst:subsample': self.subsample,
            "bst:min_child_weight": self.min_samples_leaf,
            "bst:gamma": self.gamma,
            'silent':1,
            'objective':'binary:logistic',
            "eval_metric": "logloss"
        }
        self.param['nthread'] = 4

    def prepare(self):
        pass
    
    def add_data(self, data, class_name, kind="training"):
        if kind == "training":
            dd = self.data
        elif kind == "testing":
            dd = self.data_testing
        
        dd[class_name] = data 

    def train(self):
        
        d_testing = xgb.DMatrix(
            pandas.concat([data[self.variables] for data in self.data_testing.values()]),
            label=pandas.concat([data[self.label] for data in self.data_testing.values()]),
            weight=pandas.concat([data[self.weight] for data in self.data_testing.values()])
        )
        d_training = xgb.DMatrix(
            pandas.concat([data[self.variables] for data in self.data.values()]),
            label=pandas.concat([data[self.label] for data in self.data.values()]),
            weight=pandas.concat([data[self.weight] for data in self.data.values()])
        )
        evallist  = [(d_testing,'eval'), (d_training,'train')]
        evald = dict()

        print "training"
        self.model = xgb.train( self.param.items(), d_training, self.ntrees, evallist, evals_result=evald)
        return self.model

    def evaluate(self, data):
        data = xgb.DMatrix(
            data[self.variables],
            label=data[self.label],
            weight=data[self.weight]

        )
        return self.model.predict(data)
        
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
