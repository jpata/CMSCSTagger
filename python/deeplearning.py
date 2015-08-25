import sys
sys.setrecursionlimit(50000)
sys.path.append("/home/joosep/keras")
import keras
import root_numpy as rnpy
import numpy as np
import pandas
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import cPickle as pickle

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.utils import np_utils, generic_utils
from keras.layers.advanced_activations import PReLU
from keras.layers.normalization import BatchNormalization

# for c in d.columns:
#     print c
def normalize_col(d, col):
    m = d[col].mean()
    d[col] = d[col] - m
    s = d[col].std()
    d[col] = d[col] / s

trainvars1 = [
    "Jet_CSV", "Jet_CSVIVF",
]

trainvars2 = [
    "Jet_CSV", "Jet_CSVIVF",
    "Jet_SoftMu", "Jet_SoftEl", "Jet_JP",
]

trainvars3 = [
    "Jet_CSV", "Jet_CSVIVF",
    "Jet_SoftMu", "Jet_SoftEl", "Jet_JP",

    "TagVarCSV_jetNTracks",
    "TagVarCSV_jetNTracksEtaRel",
    "TagVarCSV_trackSumJetEtRatio",
    "TagVarCSV_trackSumJetDeltaR",
    "TagVarCSV_trackSip2dValAboveCharm",
    "TagVarCSV_trackSip2dSigAboveCharm",
    "TagVarCSV_trackSip3dValAboveCharm",
    "TagVarCSV_trackSip3dSigAboveCharm",
    "TagVarCSV_vertexCategory",
    "TagVarCSV_jetNSecondaryVertices",
    "TagVarCSV_vertexMass",
    "TagVarCSV_vertexNTracks",
    "TagVarCSV_vertexEnergyRatio",
    "TagVarCSV_vertexJetDeltaR",
    "TagVarCSV_flightDistance2dVal",
    "TagVarCSV_flightDistance2dSig",
    "TagVarCSV_flightDistance3dVal",
    "TagVarCSV_flightDistance3dSig",
    "TagVarCSV_trackSip2dSig_0",
    "TagVarCSV_trackSip2dSig_1",
    "TagVarCSV_trackSip2dSig_2",
    "TagVarCSV_trackSip2dSig_3",
    "TagVarCSV_trackSip3dSig_0",
    "TagVarCSV_trackSip3dSig_1",
    "TagVarCSV_trackSip3dSig_2",
    "TagVarCSV_trackSip3dSig_3",
    "TagVarCSV_trackPtRel_0",
    "TagVarCSV_trackPtRel_1",
    "TagVarCSV_trackPtRel_2",
    "TagVarCSV_trackPtRel_3",
    "TagVarCSV_trackEtaRel_0",
    "TagVarCSV_trackEtaRel_1",
    "TagVarCSV_trackEtaRel_2",
]


for tv in trainvars3:
    m =  d[tv].mean()
    s = d[tv].std()
    print tv, d[tv].min(), d[tv].max(), d[tv].mean(), d[tv].std()

    if "Jet" in tv:
        d.loc[d[tv]<= -9, tv] = 0
    if "TagVar" in tv:
        d.loc[d[tv]<= -98, tv] = 0

    d.loc[d[tv]<(m-2*s), tv] = m-2*s
    d.loc[d[tv]>(m+2*s), tv] = m+2*s
    normalize_col(d, "Jet_CSV")
    print tv, d[tv].min(), d[tv].max(), d[tv].mean(), d[tv].std()

d_training = d[d["training"]==1]
d_testing = d[d["training"]==0]

class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs):
        self.loss = []
        self.val_loss = []
        self.accuracy = []
        self.val_accuracy = []

    def on_epoch_end(self, batch, logs={}):
        self.loss.append(logs.get('loss'))
        self.val_loss.append(logs.get('val_loss'))
        self.accuracy.append(logs.get('accuracy'))
        self.val_accuracy.append(logs.get('val_accuracy'))

for scenario, trainvars in [("sc1", trainvars1), ("sc2", trainvars2), ("sc3", trainvars3)]:
    print "scenario", scenario
    X_train = d_training[trainvars].as_matrix()
    y_train = d_training["id"].as_matrix()
    y_train2 = (d_training["id"]==2).as_matrix()

    X_test = d_testing[trainvars].as_matrix()
    y_test = d_testing["id"].as_matrix()
    y_test2 = (d_testing["id"]==2).as_matrix()


    print "training nn..."

    dims = X_train.shape[1]
    nclasses = 2

    layer_size = 512

    model = Sequential()
    model.add(Dense(dims, 512, init='glorot_uniform'))
    model.add(PReLU((512,)))

    for ilayer in range(20):
        model.add(PReLU((512,)))
        model.add(Dense(512, 512, init='glorot_uniform'))
        model.add(Dropout(0.5))

    model.add(Dense(512, nclasses, init='glorot_uniform'))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.5, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='mean_squared_error', optimizer=sgd)

    history = LossHistory()
    model.fit(X_train, np_utils.to_categorical(y_train2),
        nb_epoch=1000, batch_size=4096, verbose=2, callbacks=[history],
        validation_data=(X_test, np_utils.to_categorical(y_test2)),
        show_accuracy=True
    )
    # plt.figure(figsize=(4,4))
    # plt.plot(history.loss)
    # plt.plot(history.val_loss)
    # plt.savefig("nn_loss_{0}.pdf".format(scenario))
    #
    # plt.figure(figsize=(4,4))
    # plt.plot(history.accuracy)
    # plt.plot(history.val_accuracy)
    # plt.savefig("nn_acc_{0}.pdf".format(scenario))
    #
    pickle.dump(model, open("nn_{0}.pkl".format(scenario), "w"))

    print "training bdt..."

    from sklearn.ensemble import GradientBoostingClassifier
    cls = GradientBoostingClassifier(
        n_estimators=100, learning_rate=0.05,
        max_depth=3,
        min_samples_split=100,
        min_samples_leaf=100,
        subsample=1.0,
        verbose=True
    )

    cls.fit(X_train, y_train2)
    pickle.dump(cls, open("bdt_{0}.pkl".format(scenario), "w"))

    print "predicting..."
    d["p"] = model.predict_proba(d[trainvars])[:, 1]
    d["p2"] = cls.predict_proba(d[trainvars])[:, 1]

    d_training = d[d["training"]==1]
    d_testing = d[d["training"]==0]

    plt.figure(figsize=(10,10))
    plt.grid()
    roc(d, "id==2", "id==0", "Jet_CSV", color="red")
    roc(d, "id==2", "id==0", "Jet_CSVIVF", color="blue")
    roc(d, "id==2", "id==0", "Jet_CombMVA", color="orange")
    roc(d_testing, "id==2", "id==0", "p", color="black")
    roc(d_training, "id==2", "id==0", "p", color="black", ls="--")

    roc(d_testing, "id==2", "id==0", "p2", color="gray")
    roc(d_training, "id==2", "id==0", "p2", color="gray", ls="--")

    roc(d, "id==2", "id==1", "Jet_CSV", color="red", ls="-")
    roc(d, "id==2", "id==1", "Jet_CSVIVF", color="blue", ls="-")
    roc(d, "id==2", "id==1", "Jet_CombMVA", color="orange", ls="-")
    roc(d_testing, "id==2", "id==1", "p", color="black", ls="-")
    roc(d_training, "id==2", "id==1", "p", color="black", ls="--")

    roc(d_testing, "id==2", "id==1", "p2", color="gray", ls="-")
    roc(d_training, "id==2", "id==1", "p2", color="gray", ls="--")

    plt.yscale("log")
    plt.ylim(0.001, 1.0)
    plt.xlim(0.5, 1.0)
    plt.savefig("/home/joosep/public_html/learn_{0}.pdf".format(scenario))
