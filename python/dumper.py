import ROOT, sys
from treeStructure import *
import math
import numpy as np
from array import array

def remove_nan_inf(val):
    if val!=val or np.isnan(val) or np.isinf(val):
        return -9999
    return val

class NTupleVariable:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.func = kwargs.get("func")
        self.dtype = kwargs.get("dtype", "d")
        self.var = array(self.dtype, [0.0])

    def set(self, x):
        self.var[0] = remove_nan_inf(self.func(x))

    def create_branch(self, tree):
        tree.Branch(
            self.name, self.var,
            "{0}/{1}".format(
                self.name, self.dtype
            )
        )

weightfile = ROOT.TFile("data/tt_weights.root")
fhist = {}
fhist["b"] = weightfile.Get("hb")
fhist["c"] = weightfile.Get("hc")
fhist["l"] = weightfile.Get("hl")

def get_weight(pt, eta, fl):
    h = fhist[fl]
    b = h.FindBin(abs(eta), pt)
    w = h.GetBinContent(b)
    #print pt, eta, fl, b, w
    if w>0:
        w = 1.0 / w
    elif w<=0:
        w = 0.0
    return w

jet_pt = NTupleVariable(
    name="pt",
    func=lambda x: x.pt
)

jet_vtxCat = NTupleVariable(
    name="vtxCat",
    func=lambda x: x.vertexCategory
)

jet_eta = NTupleVariable(
    name="eta",
    func=lambda x: x.eta
)

jet_bd1 = NTupleVariable(
    name="bd_csv1",
    func=lambda x: x.CombSvx
)

jet_bd2 = NTupleVariable(
    name="bd_csv2",
    func=lambda x: x.CombIVF
)

jet_bd3 = NTupleVariable(
    name="bd_jp",
    func=lambda x: x.Proba
)

jet_bd4 = NTupleVariable(
    name="bd_smu",
    func=lambda x: x.SoftMu
)

jet_bd5 = NTupleVariable(
    name="bd_sel",
    func=lambda x: x.SoftEl
)

jet_flavour = NTupleVariable(
    name="flavour",
    func=lambda x: x.flavour
)

jet_nsvs = NTupleVariable(
    name="nsvs",
    func=lambda x: x.nsvs
)

jet_sv_chi2ndf = NTupleVariable(
    name="sv_chi2ndf",
    func=lambda x: x.sv_chi2ndf
)

jet_sv_flight3dsig = NTupleVariable(
    name="sv_flight3dsig",
    func=lambda x: x.sv_flight3dsig
)

jet_sv_flight2dsig = NTupleVariable(
    name="sv_flight2dsig",
    func=lambda x: x.sv_flight2dsig
)

jet_w1 = NTupleVariable(
    name="w1",
    func=lambda x: x.w1
)

jet_w2 = NTupleVariable(
    name="w2",
    func=lambda x: x.w2
)

if __name__ == "__main__":


    INPUT = sys.argv[1]
    OUTPUT = sys.argv[2]

    tf = ROOT.TFile(INPUT)
    tt = tf.Get("btagana/ttree")
    brlist = tt.GetListOfBranches()
    #for br in sorted([b.GetName() for b in brlist]):
    #    print br

    ofile = ROOT.TFile(OUTPUT, "RECREATE")

    otrees = {fl:ROOT.TTree("tree_"+fl, "tree_"+fl) for fl in ["l", "c", "b"]}
    for ot in otrees.values():
        ot.SetDirectory(ofile)

    registered_branches_jet = [
        jet_pt, jet_eta, jet_bd1, jet_bd2, jet_bd3, jet_bd4, jet_bd5,
        jet_vtxCat,
        jet_flavour,
        jet_nsvs,
        jet_sv_chi2ndf, jet_sv_flight3dsig, jet_sv_flight2dsig,
        jet_w1, jet_w2
    ]

    for br in registered_branches_jet:
        for ot in otrees.values():
            br.create_branch(ot)

    n = tt.GetEntries()
    print "running on N entries", n
    for i in range(n):
        if i%1000==0:
            print i
        tt.GetEntry(i)
        ev = Event(tt)

        svs = ev.SV
        for ijet, jet in enumerate(ev.Jet):

            if jet.pt < 30:
                continue

            jet.sv_chi2ndf = 0.0
            jet.sv_flight3dsig = 0.0
            jet.sv_flight2dsig = 0.0
            jet.w1 = 0.0
            jet.w2 = 0.0

            jet.w2 = 0.0

            nsv_first = jet.nFirstSV
            nsv_last = jet.nLastSV

            jet_svs = sorted(
                svs[nsv_first:nsv_last],
                key=lambda x: x.chi2 / x.ndf
            )
            jet.nsvs = len(jet_svs)

            if len(jet_svs)>0:
                jet.sv_chi2ndf = jet_svs[0].chi2 / jet_svs[0].ndf
                jet.sv_flight3dsig = jet_svs[0].flight / jet_svs[0].flightErr
                jet.sv_flight2dsig = jet_svs[0].flight2D / jet_svs[0].flight2DErr

            if (abs(jet.flavour) == 5):
                flavour = "b"
            elif (abs(jet.flavour) == 4):
                flavour = "c"
            else:
                flavour = "l"

            jet.w1 = get_weight(jet.pt, jet.eta, flavour)
            for br in registered_branches_jet:
                br.set(jet)

            otrees[flavour].Fill()

    ofile.Write()
    ofile.Close()
