from WMCore.Configuration import Configuration

global config

config = Configuration()

config.section_("General")
config.General.transferLogs = True
config.General.requestName = "btagana_ttjets_v3"

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.allowNonProductionCMSSW = True
config.JobType.maxJobRuntimeMin = 60*48 #maximal job runtime in minute
config.JobType.psetName = "../python/runAnalyzerAOD.py"

config.section_("Data")
config.Data.inputDataset = "/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM"
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.publication = False

config.Data.unitsPerJob = 2
config.Data.totalUnits = 1000

config.section_("Site")
config.Site.storageSite = "T2_EE_Estonia"


