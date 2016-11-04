import sys

#add xgboost
sys.path += ["/mnt/t3nfs01/data01/shome/jpata/xgboost/python-package"]

import copy
from collections import OrderedDict

import numpy as np
import root_numpy as rnpy
import pandas
import dask
import cPickle

from matplotlib.colors import LogNorm
import rootpy
import rootpy.plotting

import sklearn
import sklearn.datasets
from sklearn import metrics
from sklearn.model_selection import KFold

import ROOT

import matplotlib.pyplot as plt
import seaborn

import xgboost

import rootpy.plotting.root2matplotlib as rplt

import sklearn_cls

from pandas.tools.plotting import scatter_matrix

import bcolz
import json


eval_set = sklearn_cls.load_set("eval_set_allvars")

print "training"

params = {
    "base_score": 0.5,
    "colsample_bylevel": 1,
    "colsample_bytree": 1,
    "gamma": 0,
    "learning_rate": 0.1,
    "max_delta_step": 0,
    "max_depth": 3,
    "min_child_weight": 1,
    "missing": None,
    "n_estimators": 500,
    "nthread": 1,
    "objective": "binary:logistic",
    "reg_alpha": 0,
    "reg_lambda": 1,
    "scale_pos_weight": 1,
    "seed": 0,
    "silent": False,
    "subsample": 1
}
params["eval_metric"] = ["error", "auc"]

watchlist = [(eval_set[0], "train"), (eval_set[1], "test")]
print "training over {0} rows, {1} features".format(eval_set[0].num_row(), eval_set[0].num_col())
bst = xgboost.train(params, eval_set[0], 500, watchlist)

for eset, name in watchlist:
    print name
    pred = bst.predict(eset)
    fpr, tpr, _ = metrics.roc_curve(eset.get_label(), pred)
    a = metrics.auc(fpr, tpr)
    print "AUC = {0:.4f}".format(a)

of = open("model.pkl", "wb")
cPickle.dump(bst, of)
of.close()
