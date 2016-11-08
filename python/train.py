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

import sklearn_cls

import json
import logging

if __name__ == "__main__":
    infile = open(sys.argv[1])
    conf = json.load(infile)
    infile.close()

    eval_set = sklearn_cls.load_set(conf["input_data"])

    params = conf["params"]
    params["eval_metric"] = conf["eval_metric"]

    roc_pairs = map(tuple, conf["roc_pairs"])

    watchlist = [(eval_set[0], "train"), (eval_set[1], "test")]
    logging.info(
        "training over {0} rows, {1} features".format(
            eval_set[0].num_row(), eval_set[0].num_col()
        )
    )
    evals_result = {}
    bst = xgboost.train(
        params,
        eval_set[0],
        num_boost_round = conf["num_boost_round"],
        evals = watchlist,
        evals_result = evals_result
    )

    training_result = {}
    training_result["rocs"] = {}
    for eset, name in watchlist:
        training_result["rocs"][name] = {}
        label_array = eset.get_label()
        labels = np.unique(label_array)
        print "unique labels", labels
        for ilab, lab in enumerate(labels):
            sel = label_array == lab
            idx = np.where(sel)[0]
            pred = bst.predict(eset.slice(idx))
            print lab, pred[0:10]
        for lab_1, lab_2 in roc_pairs:
            
            ls1 = label_array == lab_1
            ls2 = label_array == lab_2

            idx = np.where(ls1+ls2)[0]
            pred = bst.predict(eset.slice(idx))

            fpr, tpr, _ = metrics.roc_curve(
                label_array[idx]==lab_1,
                pred[:, lab_1]
            )
            training_result["rocs"][name]["{0}_{1}".format(lab_1, lab_2)] = [list(fpr), list(tpr)]
            a = metrics.auc(fpr, tpr)
            print "AUC({0} vs {1}) = {2:.4f}".format(lab_1, lab_2, a)

    training_result["evals_result"] = evals_result

    of = open(conf["output_model"], "wb")
    cPickle.dump(bst, of)
    of.close()

    of = open(conf["output_evals"], "w")
    json.dump(training_result, of, indent=4)
    of.close()
