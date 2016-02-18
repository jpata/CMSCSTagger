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

ptbins = np.linspace(20, 620, 11)
etabins = np.linspace(0.5, 11)

def load_dataset(fn, treename, i):
    print "loading {0}:{1}".format(fn, treename)
    arr = rnpy.root2rec(
        fn,
        selection="Jet_pt>20",
        treename=treename,
        start=0,
        stop=1000000
    )
    df = pandas.DataFrame(arr)
    df["id"] = i
    df[np.isnan(df)] = 0.0
    df[np.isinf(df)] = 0.0
    df["abs_eta"] = df["Jet_eta"].abs()
    df["training"] = 0

    perminds = np.random.permutation(df.index)
    df.loc[perminds[:len(perminds)/2], "training"] = 1
    df["ptbin"] = map(lambda x: ptbins.searchsorted(x), df["Jet_pt"])
    df["etabin"] = map(lambda x: ptbins.searchsorted(x), df["abs_eta"])
    df["w"] = 1.0
    return df

def cumerr(arr, nb=100000):
    h = np.histogram(
        arr,
        bins=np.linspace(-5,5,nb)
    )
    h = h[0]
    hc = np.cumsum(h)
    he = np.sqrt(np.cumsum(h))
    hc = hc / float(np.sum(h))
    he = he / float(np.sum(h))
    return hc, he

def roc(d, sig, bkg, col, **kwargs):
    ds = d[d.eval(sig)]
    db = d[d.eval(bkg)]
    c1, e1 = cumerr(ds[col], nb=10000)
    c2, e2 = cumerr(db[col], nb=10000)
    plt.plot(1.0 - c1, 1.0 - c2, **kwargs)

md = None
d = None
memmap_fn = "/scratch/joosep/data.mmap"

if not os.path.isfile(memmap_fn):
    print "could not find memmap, projecting"
    d1 = load_dataset("data/jun11/ttjets.root", "tree_b", 2)
    d2 = load_dataset("data/jun11/ttjets.root", "tree_c", 1)
    d3 = load_dataset("data/jun11/ttjets.root", "tree_l", 0)

    print "done loading data"

    d = pandas.concat((d1, d2, d3))

    mp = np.memmap(memmap_fn, dtype='float32', mode='w+', shape=d.shape)
    mp[:] = d.as_matrix().astype("float32")[:]
    md = open("metadata.pkl", "w")
    pickle.dump((d.shape, d.columns, d.dtypes), md)
    md.close()
    del md
else:
    print "loading memmap"
    md = open("metadata.pkl", "r")
    (shape, columns, dtypes) = pickle.load(md)
    md.close()

    mp = np.memmap(memmap_fn, dtype='float32', mode='r', shape=shape)

    d = pandas.DataFrame(mp, columns=columns, dtype=dtypes)

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

