import ROOT, sys
ROOT.gROOT.SetBatch(True)

tf = ROOT.TFile(sys.argv[1])
tt = tf.Get("btagana/ttree")

# for br in tt.GetListOfBranches():
#     bn = br.GetName()
#     tt.Draw(bn + " >> h")
#     m, s = tf.Get("h").GetMean(), tf.Get("h").GetRMS()
#     print bn, m, s
for nev, ev in enumerate(tt):
    nj = ev.nJet

    nsv = ev.nSV
    #print "nsv", nsv
    for i in range(nj):
        pt = ev.Jet_pt[i]
        eta = ev.Jet_eta[i]
        csv_ivf = ev.Jet_CombIVF[i]
        csv = ev.Jet_CombSvx[i]
        csv_sl = ev.Jet_CombCSVSL[i]
        fl = ev.Jet_flavour[i]
        is_b = int(abs(fl) == 5)
        is_c = int(abs(fl) == 4)

        nsv_first = ev.Jet_nFirstSV[i]
        nsv_last = ev.Jet_nLastSV[i]

        svs = []
        for isv in range(nsv_first, nsv_last):
            chi2_ndf = ev.SV_chi2[isv] / ev.SV_ndf[isv]
            vtx_mass = ev.SV_mass[isv]
            ntrk = ev.SV_nTrk[isv]
            vtx_pt = ev.SV_vtx_pt[isv]
            vtx_eta = ev.SV_vtx_eta[isv]
            svs += [(vtx_pt, vtx_eta, ntrk, vtx_mass, chi2_ndf)]
        if (len(svs)==0):
            svs += [(0,0,0,0,0)]
        cl = 0
        if is_c:
           cl = 1
        if is_b:
           cl = 2

        print nev, i, pt, eta, fl, csv_ivf, csv, csv_sl, cl, nsv_last - nsv_first, " ".join(map(str, svs[0]))
