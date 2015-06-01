import ROOT, sys
import numpy as np
import tempfile
import os

tree_name = sys.argv[1]
tt = ROOT.TChain(tree_name)

inf = sys.argv[2]
tt.AddFile(inf)

outf = sys.argv[3]

def save_tree(tree, cut, name, first_entry=0, max_entries=20000):
    of = ROOT.TFile("{0}_{1}_{2}.root".format(outf, tree_name, name), "RECREATE")
    of.cd()
    tname = tempfile.mktemp()
    print of.GetName(), first_entry, max_entries, outf, cut, name, tname
    tmpfile = ROOT.TFile(tname, "RECREATE")
    tmpfile.cd()
    tree2 = tree.CopyTree(cut)
    tree2.Write()
    of.cd()
    tree3 = tree2.CopyTree("", "", max_entries, first_entry).CloneTree()
    tree3.SetDirectory(of)
    #tree3.Write("", ROOT.TObject.kOverwrite)
    of.Write()
    of.Close()
    tmpfile.Close()
    os.remove(tname)

ptbins = np.linspace(30, 530, 11)
etabins = np.linspace(0.0, 2.5, 11)

for ptbin in range(0, 10):
    for etabin in range(0, 10):
        pt_low = ptbins[ptbin]
        pt_high = ptbins[ptbin+1]
        eta_low = etabins[etabin]
        eta_high = etabins[etabin+1]
        cut_str = "pt>={0} && pt<{1}".format(pt_low, pt_high)
        cut_str += " && abs(eta) >= {0} && abs(eta) < {1}".format(eta_low, eta_high)
        #cut = ROOT.TCut(cut_str)
        n = tt.GetEntries(cut_str)
        upto = min(10000, n/2)
        print ptbin, etabin, n, upto
        save_tree(
            tt,
            cut_str,
            name="training_pt_{0}_eta_{1}".format(ptbin, etabin),
            first_entry=0,
            max_entries=upto
        )
        save_tree(
            tt,
            cut_str,
            name="testing_pt_{0}_eta_{1}".format(ptbin, etabin),
            first_entry=upto,
            max_entries=upto
        )
        if n - 2*upto > 0:
            save_tree(
                tt,
                cut_str,
                name="rest_pt_{0}_eta_{1}".format(ptbin, etabin),
                first_entry=2*upto,
                max_entries=n-(2*upto)
            )
