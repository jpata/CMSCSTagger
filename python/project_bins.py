import ROOT, sys

tt = ROOT.TChain("tree")

infs = sys.argv[1:]
for inf in infs:
    tt.AddFile(inf)
skipped = []

def save_tree(tree, cut, name):
    of = ROOT.TFile("tree_{0}.root".format(name), "RECREATE")
    of.cd()
    tree2 = tree.CopyTree(cut_str)
    tree2.SetDirectory(of)
    of.Write()
    of.Close()

skipped = []
for ptbin in range(0, 11):
    for etabin in range(0, 11):
        cut_str = "pt_bin=={0} && eta_bin=={1}".format(ptbin, etabin)
        #cut = ROOT.TCut(cut_str)
        min_n = tt.GetEntries(cut_str)
        if min_n < 100:
            print "skipping", ptbin, etabin, min_n
            skipped += [(ptbin, etabin)]
            continue
        else:
            save_tree(tt, cut_str, name="pt_{0}_eta_{1}".format(ptbin, etabin))
        print ptbin, etabin, min_n

skipcut = []
for (ptbin, etabin) in skipped:
    print "skipped", ptbin, etabin
    skipcut += [
        "(pt_bin == {0} && eta_bin == {1})".format(ptbin, etabin)
    ]
skipcut = "||".join(skipcut)
skipcut = "!({0})".format(skipcut)
save_tree(tt, skipcut, name="skip")
