
cmsrel CMSSW_8_1_0_pre8
cd CMSSW_8_1_0_pre8/src
cmsenv

git clone -b 8_1_X --depth 1 https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements.git RecoBTag/PerformanceMeasurements

scram b -j8

cd RecoBTag/PerformanceMeasurements/test/

cmsRun runBTagAnalyzer_cfg.py miniAOD=False maxEvents=100 reportEvery=1 wantSummary=True
