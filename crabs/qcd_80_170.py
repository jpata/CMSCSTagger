from WMCore.Configuration import Configuration

global config

config = Configuration()

config.section_("General")
config.General.transferLogs = True
config.General.requestName = "btagana_qcd_80_170_May29_v1"

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
#config.JobType.maxJobRuntimeMin = 60*48 #maximal job runtime in minute
config.JobType.psetName = "../python/runAnalyzerAOD.py"

config.section_("Data")
config.Data.inputDataset = "/QCD_Pt_80to170_bcToE_Tune4C_13TeV_pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v2/AODSIM"
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.publication = False

config.Data.unitsPerJob = 20
config.Data.totalUnits = 2000

config.section_("Site")
config.Site.storageSite = "T2_EE_Estonia"
config.Site.whitelist = ["T2_BE_IIHE"]
