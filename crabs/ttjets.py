from WMCore.Configuration import Configuration

global config

config = Configuration()

config.section_("General")
config.General.transferLogs = True
config.General.requestName = "btagana_ttjets_Jul9_v1"

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.maxJobRuntimeMin = 1400
config.JobType.psetName = "../python/runAnalyzerAOD.py"
#config.JobType.inputFiles = ["MVAJetTags_newCMVA.db"]

config.section_("Data")
config.Data.inputDataset = "/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.publication = False

config.Data.unitsPerJob = 2
#config.Data.totalUnits = 600
#config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1

config.section_("Site")
config.Site.storageSite = "T2_EE_Estonia"
#config.Site.whitelist = ["T2_BE_IIHE"]

