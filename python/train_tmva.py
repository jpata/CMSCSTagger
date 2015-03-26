import ROOT
from ROOT import TMVA, TCut


ofile_tree = ROOT.TFile("jets.root")
t = ofile_tree.Get("tree")
n = t.GetEntries()
print "Nentries",n

out = ROOT.TFile('TMVA.root', 'RECREATE')
factory = TMVA.Factory(
    "train", out,
    'Transformations=I;N:DrawProgressBar=False:!V'
)
out.cd()

factory.AddVariable("bd_csv_ivf", "F")
factory.AddVariable("bd_csv_avf", "F")

factory.AddTree(t, "b", 1.0, TCut("cl==2"))
factory.AddTree(t, "c", 1.0, TCut("cl==1"))
factory.AddTree(t, "l", 1.0, TCut("cl==0"))

factory.PrepareTrainingAndTestTree(TCut(""), "SplitMode=Random:NormMode=NumEvents:!V")
factory.BookMethod(
    TMVA.Types.kBDT,
    "BDTG",
    "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.10:GradBaggingFraction=0.50:nCuts=20"
)
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

out.Close()
