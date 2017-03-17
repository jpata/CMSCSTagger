TAGVARPARS="useExternalInput=True jetPtMin=20 jetPtMax=620 jetAbsEtaMin=0 jetAbsEtaMax=2.5 maxEvents=-1"
RECOBTAG=$(CMSSW_BASE)/src/RecoBTag
PARCMD=~/parallel

projector: test/project_bins.cc
	g++ `root-config --libs --cflags` -I$(CMSSW_BASE)/src/ test/project_bins.cc -o project_bins

#run all steps chained together as a test
all-steps-test:
	cd $(RECOBTAG)/PerformanceMeasurements/test && cmsRun runBTagAnalyzer_cfg.py miniAOD=True maxEvents=1000 reportEvery=1 wantSummary=True
	cmsRun $(RECOBTAG)/TagVarExtractor/test/tagvarextractor_cfg.py useExternalInput=True jetPtMin=20 jetPtMax=620 jetAbsEtaMin=0 jetAbsEtaMax=2.5 maxEvents=-1 externalInput=$(RECOBTAG)/CMSCSTagger/input.txt outFilename=test.root
	$(RECOBTAG)/CMSCSTagger/project_bins test.root tagVars/ttree test_sub.root
	rootls test_sub.root

tagvar-qcd:
	rm -f x*
	split ~/btv/qcd_spring15.txt -l10
	ls x* | $(PARCMD) -j20 cmsRun $(CMSSW_BASE)/src/RecoBTag/TagVarExtractor/test/tagvarextractor_cfg.py $(TAGVARPARS) externalInput={} outFilename=qcd_{#}.root
	rm -f x*

project-qcd:
	ls qcd_*.root | ~/parallel -j20 ./project_bins {} tagVars/ttree sub_qcd_{#}.root
	hadd -f qcd.root sub_qcd_*.root

tagvar-ttjets:
	rm -f x*
	split /home/joosep/btv/ttjets_spring15.txt -l10
	ls x* | $(PARCMD) -j20 cmsRun $(CMSSW_BASE)/src/RecoBTag/TagVarExtractor/test/tagvarextractor_cfg.py $(TAGVARPARS) externalInput={} outFilename=ttjets_{#}.root
	rm -f x*

project-ttjets:
	ls ttjets_*.root | ~/parallel -j20 ./project_bins {} tagVars/ttree sub_ttjets_{#}.root
	hadd -f ttjets.root sub_ttjets_*.root

reduce:
	../ROOTDataHelpers/TreeSelector qcd.root tree_b qcd_b_10M.root 10000000
	../ROOTDataHelpers/TreeSelector qcd.root tree_c qcd_c_10M.root 10000000
	../ROOTDataHelpers/TreeSelector qcd.root tree_l qcd_l_10M.root 10000000
	../ROOTDataHelpers/TreeSelector ttjets.root tree_b ttjets_b_10M.root 10000000
	../ROOTDataHelpers/TreeSelector ttjets.root tree_c ttjets_c_10M.root 10000000
	../ROOTDataHelpers/TreeSelector ttjets.root tree_l ttjets_l_10M.root 10000000
