import ROOT, sys
import numpy as np

inp_tree = sys.argv[1]
tt = ROOT.TChain(inp_tree)

infs = sys.argv[2:]
for inf in infs:
    tt.AddFile(inf)
skipped = []

def save_tree(tree, cut, name, max_entries=10000):
    of = ROOT.TFile("{0}_{1}.root".format(inp_tree, name), "RECREATE")
    of.cd()
    tree2 = tree.CopyTree(cut_str, "")
    tree3 = tree2.CloneTree(max_entries)
    tree3.SetDirectory(of)
    of.Write()
    of.Close()

pt_bins = np.linspace(20, 520, 11)
eta_bins = np.linspace(0.0, 2.5, 11)

skipped = []
for ptbin in range(0, len(pt_bins)-1):
    for etabin in range(0, len(eta_bins)-1):
        cut_str = "pt>={0} && pt<{1}".format(pt_bins[ptbin], pt_bins[ptbin+1])
        cut_str += "&& abs(eta)>={0} && abs(eta)<{1}".format(eta_bins[etabin], eta_bins[etabin+1])
        #cut = ROOT.TCut(cut_str)
        min_n = tt.GetEntries(cut_str)
        #if min_n < 100:
        #    print "skipping", ptbin, etabin, min_n
        #    skipped += [(ptbin, etabin, min_n)]
        #    continue
        #else:
        #    save_tree(tt, cut_str, name="pt_{0}_eta_{1}".format(ptbin, etabin))
        save_tree(tt, cut_str, name="pt_{0}_eta_{1}".format(ptbin, etabin))
        print ptbin, etabin, min_n

print skipped
