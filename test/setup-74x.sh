export SCRAM_ARCH=slc6_amd64_gcc481
cmsrel CMSSW_7_4_0
cd CMSSW_7_4_0/src
cmsenv

git clone -b V00-00-01 git://github.com/cms-btv-pog/cms-EventCounter.git MyAnalysis/EventCounter
git clone -b 7_4_X_v1.05 git@github.com:cms-btv-pog/RecoBTag-BTagAnalyzerLite.git RecoBTag/BTagAnalyzerLite

scram b -j8

cd RecoBTag/BTagAnalyzerLite/test/

cmsRun runBTagAnalyzerLite_cfg.py miniAOD=True maxEvents=100 reportEvery=1 wantSummary=True
