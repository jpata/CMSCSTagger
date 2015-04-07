import ROOT
from ROOT import TMVA, TCut


ofile_tree = ROOT.TFile("jets.root")
t = ofile_tree.Get("tree")
n = t.GetEntries()
print "Nentries",n

out = ROOT.TFile('TMVA.root', 'RECREATE')
factory = TMVA.Factory(
    "train", out,
    'Transformations=I;N:DrawProgressBar=False:!V:AnalysisType=Multiclass'
)
out.cd()

factory.AddVariable("csv1", "F")
factory.AddVariable("csv2", "F")
factory.AddSpectator("pt", "F")
factory.AddSpectator("eta", "F")

factory.AddTree(t, "b", 1.0, TCut("abs(flavour) == 5"))
factory.AddTree(t, "c", 1.0, TCut("abs(flavour) == 4"))
factory.AddTree(t, "l", 1.0, TCut("abs(flavour) < 4"))
factory.AddTree(t, "g", 1.0, TCut("abs(flavour) == 21"))

pt_eta_cat = factory.BookMethod(
    TMVA.Types.kCategory,
    "pt_eta",
    ""
)

#factory.PrepareTrainingAndTestTree(TCut(""), "SplitMode=Random:NormMode=NumEvents:!V")

skipped = []
for ptbin in range(0, 9):
    for etabin in range(0, 3):
        cut_str = "(pt_bin - pt_bin%10)/10 == {0} && (eta_bin - eta_bin%10)/10 == {1}".format(ptbin, etabin)
        cut = ROOT.TCut(cut_str)
        n = t.GetEntries(cut_str)
        if n < 100:
            print "skipping", ptbin, etabin
            skipped += [(ptbin, etabin)]
            continue
        print ptbin, etabin, t.GetEntries(cut_str)
        pt_eta_cat.AddMethod(
            cut,
            ":".join(["csv1:csv2"]),
            TMVA.Types.kBDT,
            "bdt_{0}_{1}".format(ptbin, etabin),
            "!H:!V:NTrees=200:BoostType=Grad:Shrinkage=0.10:GradBaggingFraction=0.50:nCuts=20"
        )
        
skipcut = []
for (ptbin, etabin) in skipped:
    print "skipped", ptbin, etabin
    skipcut += [
        "((pt_bin - pt_bin%10)/10 == {0} && (eta_bin - eta_bin%10)/10 == {1})".format(ptbin, etabin)
    ]
skipcut = "||".join(skipcut)
skipcut = "!(" + skipcut + ")"
factory.PrepareTrainingAndTestTree(TCut(skipcut), "SplitMode=Random:NormMode=NumEvents:!V")

factory.TrainAllMethods()
#factory.TestAllMethods()
#factory.EvaluateAllMethods()

out.Close()
