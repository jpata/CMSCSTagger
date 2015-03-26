import ROOT
ofile_tree = ROOT.TFile("jets.root", "RECREATE")
ofile_tree.cd()
t = ROOT.TTree("tree", "tree")
print "reading csv file"
t.ReadFile("jets_comma.csv",
    "nev/I:i/I:pt/F:eta/F:fl/I:bd_jp/F:bd_jpb/F:bd_svx/F:bd_csv_ivf/F:bd_csv_avf/F:cl/I:nsv/I:sv1_flight_sig/F:sv1_dr1/F:sv1_ntrk/I:sv1_mass/F:sv1_chi2/F:sv2_flight_sig/F:sv2_dr1/F:sv2_ntrk/I:sv2_mass/F:sv2_chi2/F",
    ',',
)
t.Write()
ofile_tree.Close()
