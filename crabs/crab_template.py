import argparse, os, glob
from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import getUsernameFromSiteDB, config

class Sample:
    def __init__(self, name, dataset):
        self.name = name
        self.dataset = dataset

samples = [
#    Sample("ttjets", "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"),
#    Sample("qcd_1000_1500", "/QCD_bEnriched_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"),

#    Sample("ttjets_phase1", "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM")

    
    #/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM
    #/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM
    #/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM
    #/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM
    #/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM

    Sample("qcd_170_300", "/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM"),
    Sample("qcd_300_470", "/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM"),
    Sample("qcd_470_600", "/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM"),
    Sample("qcd_600_800", "/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM"),
    Sample("qcd_800_1000", "/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM"),
    Sample("qcd_1000_1400", "/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM"),
    Sample("qcd_1400_1800", "/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM"),
    Sample("qcd_2400_3200", "/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM"),
    Sample("qcd_3200_inf", "/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM"),
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Submits crab jobs')
    parser.add_argument('--out', action="store", required=True, help="output site, e.g. T2_CH_CSCS", type=str)
    parser.add_argument('--tag', action="store", required=True, help="unique tag for processing", type=str)
    parser.add_argument('--user', action="store", help="username on grid", type=str, default=getUsernameFromSiteDB())
    args = parser.parse_args()
   
    jobs_file = open("jobs_{0}.txt".format(args.tag), "w")
    for sample in samples:
        cfg = config()
        
        cfg.section_("General")
        cfg.General.transferLogs = True
        cfg.General.requestName = 'btv_{0}_{1}'.format(args.tag, sample.name)
        cfg.General.workArea = 'crab_projects/{0}'.format(args.tag)
        if not os.path.exists(cfg.General.workArea):
            os.makedirs(cfg.General.workArea)
        
        cfg.section_("JobType")
        cfg.JobType.pluginName = 'Analysis'
        cfg.JobType.maxJobRuntimeMin = 500
        cfg.JobType.psetName = "../python/runAnalyzerMiniAOD.py"
        
        cfg.section_("Data")
        cfg.Data.inputDataset = sample.dataset
        cfg.Data.splitting = 'FileBased'
        cfg.Data.publication = False
        
        cfg.Data.unitsPerJob = 2
        cfg.Data.totalUnits = 600
        cfg.Data.outLFNDirBase = '/store/user/{0}/btv/{1}'.format(
            args.user, args.tag 
        )
        cfg.Data.ignoreLocality = True
        
        cfg.section_("Site")
        cfg.Site.storageSite = "T2_CH_CSCS"
        cfg.Site.whitelist = ["T2_CH_CSCS"]

        res = crabCommand('submit', config = cfg)

        outpath = "{0}/crab_{1}".format(cfg.General.workArea, cfg.General.requestName)
        print outpath
        jobs_file.write(outpath + "\n") 
    
    jobs_file.close()
