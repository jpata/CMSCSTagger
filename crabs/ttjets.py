from WMCore.Configuration import Configuration

global config

config = Configuration()

config.section_("General")
config.General.transferLogs = True
config.General.requestName = "btagana_ttjets_May27_test"

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.maxJobRuntimeMin = 1400
config.JobType.psetName = "../python/runAnalyzerAOD.py"
config.JobType.inputFiles = ["MVAJetTags_newCMVA.db"]

config.section_("Data")
config.Data.inputDataset = "/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM"
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.publication = False

config.Data.unitsPerJob = 10
config.Data.totalUnits = 2900
#config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1

config.section_("Site")
config.Site.storageSite = "T2_EE_Estonia"


