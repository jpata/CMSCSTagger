import root_numpy as rnpy

def load_dataset(fn, treename, i):
    arr = rnpy.root2rec(
        fn,
        selection="Jet_pt>20",
        branches=["Jet_pt", "Jet_eta", "Jet_flavour", "Jet_CSV", "Jet_CSVIVF", "Jet_CombMVA", "Jet_SoftMu", "Jet_SoftEl", "Jet_JP"],
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

path = "/home/joosep/btv/data/jun11"
d1 = load_dataset(path + "/ttjets.root", "tree_b", 2)
d2 = load_dataset(path + "/ttjets.root", "tree_c", 1)
d3 = load_dataset(path + "/ttjets.root", "tree_l", 0)

d = pandas.concat((d1, d2, d3))

d_training = d[d["training"]==1]
d_testing = d[d["training"]==0]

ptbins_w = np.linspace(20, 620, 101)
etabins_w = np.linspace(0, 2.5, 101)
def get_weights(df):
    vs, bx, by = np.histogram2d(
        df["Jet_pt"],
        df["abs_eta"],
        bins=[ptbins_w, etabins_w]
    )
    vs = vs / float(np.sum(vs))
    ws = 1.0/vs
    ws[np.isnan(ws)]=0.0
    ws[np.isnan(ws)]=0.0
    ws[np.isinf(ws)]=1
    ws[np.isinf(ws)]=1
    return ws

weight_b = get_weights(d[d["id"]==2])
weight_c = get_weights(d[d["id"]==1])
weight_l = get_weights(d[d["id"]==0])


def weight(pt, eta, fl):
    ibx = ptbins_w.searchsorted(pt) - 1
    iby = etabins_w.searchsorted(abs(eta)) - 1
    if ibx < 0:
        ibx = 0
    if iby < 0:
        iby = 0
    if ibx>=len(ptbins_w)-1:
        ibx = len(ptbins_w)-2
    if iby>=len(etabins_w)-1:
        iby = len(etabins_w)-2
        
    if fl == 2:
        ws = weight_b
    elif fl == 1:
        ws = weight_c
    elif fl==0:
        ws = weight_l
    return ws[ibx, iby]

d["w"]  = map(
    lambda _z: weight(_z[0], _z[1], _z[2]),
    zip(d["Jet_pt"], d["abs_eta"], d["id"])
)
