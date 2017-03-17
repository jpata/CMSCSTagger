cmsrel CMSSW_8_1_0
cd CMSSW_8_1_0/src
cmsenv

setenv CMSSW_GIT_REFERENCE /cvmfs/cms.cern.ch/cmssw.git.daily
git cms-init

git remote add btv-cmssw https://github.com/cms-btv-pog/cmssw.git
git fetch --tags btv-cmssw

git cms-merge-topic -u cms-btv-pog:DeepFlavour-from-CMSSW_8_1_0
git cms-merge-topic -u cms-btv-pog:PATJetFix-v1_from-CMSSW_8_1_0
git cms-merge-topic -u cms-btv-pog:BoostedDoubleSVTaggerV4-WithWeightFiles-v1_from-CMSSW_8_1_0

git clone -b 8_1_X_v1.01 --depth 1 https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements.git RecoBTag/PerformanceMeasurements
git clone -b TensorFlow_tuple_cmva  https://github.com/jpata/RecoBTag-TagVarExtractor.git RecoBTag/TagVarExtractor
git clone https://github.com/jpata/CMSCSTagger.git RecoBTag/TagVarExtractor

scram b -j8
