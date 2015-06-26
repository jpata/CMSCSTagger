export SCRAM_ARCH=slc6_amd64_gcc491
cmsrel CMSSW_7_4_5
cd CMSSW_7_4_5/src
cmsenv
git cms-init
git cms-addpkg RecoBTau/JetTagProducer
git cms-addpkg RecoBTag/Configuration
git cms-addpkg PhysicsTools/PatAlgos

git remote add btv-cmssw https://github.com/cms-btv-pog/cmssw.git
git fetch btv-cmssw
git cms-merge-topic -u cms-btv-pog:BoostedDoubleSVTagger-WithWeightFiles-v2_from-CMSSW_7_4_1
git cms-merge-topic -u cms-btv-pog:FixSoftElectronTagger_from-CMSSW_7_4_5
git cms-merge-topic -u cms-btv-pog:CommonTMVAEvaluatorForBTagging_from-CMSSW_7_5_X_2015-06-18-1100
git clone -b 7_4_X_v1.06 git@github.com:cms-btv-pog/RecoBTag-PerformanceMeasurements.git RecoBTag/PerformanceMeasurements
