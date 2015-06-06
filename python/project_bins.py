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
    #tree2 = tree.CopyTree(cut)
    tree2.Write()
    of.cd()
    tree3 = tree2.CopyTree("", "", max_entries, first_entry).CloneTree()
    tree3.SetDirectory(of)
    #tree3.Write("", ROOT.TObject.kOverwrite)
    of.Write()
    of.Close()
    tmpfile.Close()
    os.remove(tname)

upto = 20000

for (name, cut) in [("b", "abs(Jet_flavour)==5"), ("c", "abs(Jet_flavour)==4"), ("l", "abs(Jet_flavour)!=5 && abs(Jet_flavour)!=4")]:
    n = tt.GetEntries(cut)
    tree2 = tt.CopyTree(cut)
    save_tree(
        tree2,
        cut,
        name="training_{0}".format(name),
        first_entry=0,
        max_entries=upto
    )
    save_tree(
        tree2,
        cut,
        name="testing_{0}".format(name),
        first_entry=upto,
        max_entries=upto
    )
    save_tree(
        tree2,
        cut,
        name="rest_{0}".format(name),
        first_entry=2*upto,
        max_entries=n-(2*upto)
    )
