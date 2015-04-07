import ROOT, sys
from treeStructure import *
import math
import numpy as np
from array import array

class NTupleVariable:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.func = kwargs.get("func")
        self.dtype = kwargs.get("dtype", "f")
        self.var = array(self.dtype, [0.0])

    def set(self, x):
        self.var[0] = self.func(x)

    def create_branch(self, tree):
        tree.Branch(
            self.name, self.var,
            "{0}/{1}".format(
                self.name, self.dtype
            )
        )

tf = ROOT.TFile(sys.argv[1])
tt = tf.Get("btagana/ttree")
#brlist = tt.GetListOfBranches()

jet_pt = NTupleVariable(
    name="pt",
    func=lambda x: x.pt
)

jet_pt_bin = NTupleVariable(
    name="pt_bin",
    func=lambda x: x.pt_bin
)

jet_eta = NTupleVariable(
    name="eta",
    func=lambda x: x.eta
)

jet_eta_bin = NTupleVariable(
    name="eta_bin",
    func=lambda x: x.eta_bin
)


jet_csv1 = NTupleVariable(
    name="csv1",
    func=lambda x: x.CombSvx
)

jet_csv2 = NTupleVariable(
    name="csv2",
    func=lambda x: x.CombIVF
)

jet_csv3 = NTupleVariable(
    name="csv3",
    func=lambda x: x.Proba
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


ofile = ROOT.TFile(sys.argv[2], "RECREATE")
otree = ROOT.TTree("tree", "tree")
otree.SetDirectory(ofile)

registered_branches_jet = [
    jet_pt, jet_eta, jet_csv1, jet_csv2, jet_csv3,
    jet_flavour,
    jet_nsvs,
    jet_sv_chi2ndf, jet_sv_flight3dsig, jet_sv_flight2dsig
]

for br in registered_branches_jet:
    br.create_branch(otree)

pt_bins = np.linspace(20, 820, 81)
eta_bins = np.linspace(0.0, 2.5, 21)

n = tt.GetEntries()
print n
for i in range(n):
    if i%1000==0:
        print i
    tt.GetEntry(i)
    ev = Event(tt)

    svs = ev.SV
    for ijet, jet in enumerate(ev.Jet):
        if jet.pt < 20:
            continue
        jet.pt_bin = pt_bins.searchsorted(jet.pt)
        jet.eta_bin = eta_bins.searchsorted(abs(jet.eta))
        jet.sv_chi2ndf = 0.0
        jet.sv_flight3dsig = 0.0
        jet.sv_flight2dsig = 0.0

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

        for br in registered_branches_jet:
            br.set(jet)

        otree.Fill()

ofile.Write()
ofile.Close()
