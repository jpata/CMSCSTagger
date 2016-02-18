import pandas
import numpy as np
import root_numpy as rnpy
import sys
sys.path.append("/home/joosep/local-sl6/xgboost/wrapper/")
import xgboost as xgb

def load_dataset(fn, treename, i):
    print "loading", fn
    arr = rnpy.root2rec(
        fn,
        selection="Jet_pt>20",
        #branches=["Jet_pt", "Jet_eta", "Jet_flavour"],
        branches=["Jet_pt", "Jet_eta", "Jet_flavour", "Jet_CSV", "Jet_CSVIVF", "Jet_CombMVA", "Jet_CombMVANEW", "Jet_CombMVAETH", "Jet_SoftMu", "Jet_SoftEl", "Jet_JP", "Jet_JBP", "TagVarCSV_vertexCategory"],
        treename=treename,
        start=0,
        stop=5000000
    )
    df = pandas.DataFrame(arr)
    df["id"] = i
    df[np.isnan(df)] = 0.0
    df[np.isinf(df)] = 0.0
    for c in ["Jet_CSV", "Jet_CSVIVF", "Jet_SoftEl", "Jet_SoftMu"]:
        df.loc[df[c]<=0, c] = 0
        df.loc[df[c]>=1, c] = 1
    df["abs_eta"] = df["Jet_eta"].abs()
    df["training"] = 0
    
    perminds = np.random.permutation(df.index)
    df.loc[perminds[:len(perminds)/2], "training"] = 1
    df["w"] = 1.0
    return df

d1 = load_dataset("data/jul13/ttjets.root", "tree_b", 2)
d2 = load_dataset("data/jul13/ttjets.root", "tree_c", 1)
d3 = load_dataset("data/jul13/ttjets.root", "tree_l", 0)
d = pandas.concat((d1, d2, d3))

print "loaded data", d.shape
d_training = d[d["training"]==1]
d_testing = d[d["training"]==0]

varlist = ["Jet_CSV", "Jet_CSVIVF", "Jet_JP", "Jet_JBP", "Jet_SoftEl", "Jet_SoftMu", "Jet_pt", "abs_eta"]

dts = xgb.DMatrix(d_training[varlist], label=(d_training["id"]==2))
dtr = xgb.DMatrix(d_testing[varlist], label=(d_testing["id"]==2))

param = {'bst:max_depth':4, 'bst:eta':0.1, 'silent':1, 'objective':'binary:logistic' }
param['nthread'] = 20
plst = param.items()
plst += [('eval_metric', 'auc')] # Multiple evals can be handled in this way
#plst += [('eval_metric', 'ams@0')]
evallist  = [(dts,'eval'), (dtr,'train')]
num_round = 1000
evald = dict()

print "training"
bst = xgb.train( plst, dtr, num_round, evallist, evals_result=evald)

of = open("model.pkl", "w")
import pickle
pickle.dump(bst, of)
of.close()
