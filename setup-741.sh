export SCRAM_ARCH=slc6_amd64_gcc481
cmsrel CMSSW_7_4_1
cd CMSSW_7_4_1/src
cmsenv
git cms-init
git remote add btv-cmssw https://github.com/cms-btv-pog/cmssw.git
git fetch btv-cmssw
git cms-merge-topic -u cms-btv-pog:BoostedDoubleSVTagger-WithWeightFiles-v2_from-CMSSW_7_4_1
git clone -b V00-00-01 git://github.com/cms-btv-pog/cms-EventCounter.git MyAnalysis/EventCounter
git clone -b 7_4_X_v1.00 git@github.com:cms-btv-pog/RecoBTag-PerformanceMeasurements.git RecoBTag/PerformanceMeasurements
