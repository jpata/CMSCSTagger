export SCRAM_ARCH=slc6_amd64_gcc481
cmsrel CMSSW_7_2_1
cd CMSSW_7_2_1/src
cmsenv
git cms-merge-topic cms-btv-pog:Dnowatsc_TrackHistory_from-CMSSW_7_2_1
git clone -b V00-00-01 git://github.com/cms-btv-pog/cms-EventCounter.git MyAnalysis/EventCounter
git clone -b V05-00-06 git://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements.git RecoBTag/PerformanceMeasurements

