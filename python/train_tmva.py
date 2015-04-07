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

factory.AddVariable("csv1", "F")
factory.AddVariable("csv2", "F")
factory.AddSpectator("pt", "F")
factory.AddSpectator("eta", "F")

factory.AddTree(t, "b", 1.0, TCut("abs(flavour) == 5"))
factory.AddTree(t, "c", 1.0, TCut("abs(flavour) == 4"))
factory.AddTree(t, "l", 1.0, TCut("abs(flavour) < 4"))

factory.PrepareTrainingAndTestTree(TCut(""), "SplitMode=Random:NormMode=NumEvents:!V")
factory.BookMethod(
    TMVA.Types.kBDT,
    "BDTG",
    "!H:!V:NTrees=200:BoostType=Grad:Shrinkage=0.10:GradBaggingFraction=0.50:nCuts=20"
)
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

out.Close()
