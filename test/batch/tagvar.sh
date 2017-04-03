#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh
source env.sh
cd $CMSSW_BASE
eval `scram runtime -sh`

cd $GC_SCRATCH
cmsRun $CMSSW_BASE/src/RecoBTag/CMSCSTagger/test/tagvarextractor_cfg.py 
