from WMCore.Configuration import Configuration

global config

config = Configuration()

config.section_("General")
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.maxJobRuntimeMin = 200
config.JobType.psetName = "../python/runAnalyzerMiniAOD.py"

config.section_("Data")
config.Data.inputDataset = "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM"
config.Data.splitting = 'FileBased'
config.Data.publication = False

config.Data.unitsPerJob = 1
config.Data.totalUnits = 20

config.section_("Site")
config.Site.storageSite = "T2_CH_CSCS"


