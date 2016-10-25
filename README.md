## Workflow

### BTagAnalyzer
 
via crab

### TagVarExtractor

via local batch

### ProjectBins

via GNU parallel
~~~
ls data/tagvar/Oct25/TT_TuneCUETP8M1_13TeV-powheg-pythia8/job_*.root | parallel --gnu ./project_bins {} tagVars/ttree out_{#}.root
~~~
