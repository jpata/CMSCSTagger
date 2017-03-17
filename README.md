## Workflow
In terms of preprocessing the inputs, the following steps need to be done:
First you need to run the BTagAnalyzer, typically via crab.
Then, one needs to dump from the event-based ntuples the per-jet variables using TagVarExtractor.
Finally, the 3 flavours (b, c and udsg) are split into separate trees and flattened in pt/eta.

See the command `make all-steps-test` for a code example of how to run these steps locally.

### BTagAnalyzer

This step produces the well-known BTV PerformanceMeasurement trees (so-called BTagAnalyzer).

The cmsRun python configuration is dumped into `$CMSSW_BASE/src/RecoBTag/PerformanceMeasurements/test/pydump.py`.
If you want to submit crab jobs on it, it needs to be copied to `python/runAnalyzerMiniAOD.py`.
The crab jobs can be submitted using

~~~
python crabs/crab_template.py --site T2_WHATEVER --tag my_custom_run_name
~~~

to store the output on your favourite T2 under the tag you specified.
The output PFN-s should then be dumped into text files which can be further processed
locally.

### TagVarExtractor

Once the crab jobs of the previous step is done, you need to convert the event-based trees to jet-based trees.
For this we use the BTV TagVarExtractor tool called via `cmsRun`.

### ProjectBins

via GNU parallel
~~~
ls data/tagvar/Oct25/TT_TuneCUETP8M1_13TeV-powheg-pythia8/job_*.root | parallel --gnu ./project_bins {} tagVars/ttree out_{#}.root
~~~
