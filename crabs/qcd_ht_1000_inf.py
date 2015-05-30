from WMCore.Configuration import Configuration

global config

config = Configuration()

config.section_("General")
config.General.transferLogs = True
config.General.requestName = "btagana_qcd_ht_1000_inf_May29_v1"

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
#config.JobType.maxJobRuntimeMin = 60*48 #maximal job runtime in minute
config.JobType.psetName = "../python/runAnalyzerAOD.py"

config.section_("Data")
config.Data.inputDataset = "/QCD_HT_1000ToInf_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1_ext1-v1/AODSIM"
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.publication = False

config.Data.unitsPerJob = 20
config.Data.totalUnits = 2000

config.section_("Site")
config.Site.storageSite = "T2_EE_Estonia"
config.Site.whitelist = ["T2_BE_IIHE"]

