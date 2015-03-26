import ROOT, sys
ROOT.gROOT.SetBatch(True)

tt = ROOT.TChain("btagana/ttree")
for fn in sys.argv[1:]:
    tt.AddFile(fn)

for nev, ev in enumerate(tt):
    nj = ev.nJet
    #print nev

    nsv = ev.nSV
    #print "nsv", nsv
    for i in range(nj):
        #Simple jet variables
        pt = ev.Jet_pt[i]
        eta = ev.Jet_eta[i]
        bd_jp = ev.Jet_Proba[i]
        bd_jpb = ev.Jet_Bprob[i]
        bd_svx = ev.Jet_Svx[i]
        bd_csv_ivf = ev.Jet_CombIVF[i]
        bd_csv_avf = ev.Jet_CombSvx[i]
        fl = ev.Jet_flavour[i]

        is_b = int(abs(fl) == 5)
        is_c = int(abs(fl) == 4)

        #Jet SV info
        nsv_first = ev.Jet_nFirstSV[i]
        nsv_last = ev.Jet_nLastSV[i]
        svs = []
        for isv in range(nsv_first, nsv_last):
            chi2_ndf = ev.SV_chi2[isv] / ev.SV_ndf[isv]
            vtx_mass = ev.SV_mass[isv]
            ntrk = int(ev.SV_nTrk[isv])
            dr1 = ev.SV_deltaR_jet[isv]
            flight_sig = ev.SV_flight[isv] / ev.SV_flightErr[isv]
            svs += [(flight_sig, dr1, ntrk, vtx_mass, chi2_ndf)]
        svs = sorted(svs, key=lambda x: x[4])
        while (len(svs) <= 2):
            svs += [(0,0,0,0,0)]
        verts_str = " ".join([" ".join([str(v) for v in s]) for s in svs[0:2]])

        #Jet class
        cl = 0
        if is_c:
           cl = 1
        if is_b:
           cl = 2

        #Simple printout
        print nev, i, pt, eta, fl, bd_jp, bd_jpb, bd_svx, bd_csv_ivf, bd_csv_avf, cl, nsv_last - nsv_first, verts_str
