import ROOT, sys
ROOT.gROOT.SetBatch(True)

tf = ROOT.TFile(sys.argv[1])
tt = tf.Get("btagana/ttree")

for br in tt.GetListOfBranches():
    bn = br.GetName()
    tt.Draw(bn + " >> h")
    m, s = tf.Get("h").GetMean(), tf.Get("h").GetRMS()
    print bn, m, s
