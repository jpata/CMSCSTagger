import sys
#add xgboost
sys.path += ["/mnt/t3nfs01/data01/shome/jpata/xgboost/python-package"]

import xgboost
import sklearn_cls
import pandas
import numpy as np

fn = "/mnt/t3nfs01/data01/shome/jpata/btv/CMSSW_8_1_0_pre8/src/RecoBTag/CMSCSTagger/root_data/project/ttjets.root"
vs = ["Jet_CSV", "Jet_CSVIVF", "Jet_JP", "Jet_JBP", "Jet_SoftMu", "Jet_SoftEl"]
def prepare_xgb_format(fn, variable_sets):
    dd = pandas.concat([sklearn_cls.preprocess(sklearn_cls.load_data(
        fn,
        "tree_{0}".format(fl),
        #start=0, stop=50000
        )) for fl in ["b", "c", "l"]])
    
    unique_classes = dd["flavour_category"].unique()
    
    training = dd["is_training"]==1
    
    for vs, outname in variable_sets:
        eval_set = [
            (dd.ix[training, vs].as_matrix(), (dd.ix[training, "flavour_category"]==2).as_matrix()),
            (dd.ix[np.invert(training), vs].as_matrix(), (dd.ix[np.invert(training), "flavour_category"]==2).as_matrix())
        ]
        sklearn_cls.save_set(eval_set, outname)

if __name__ == "__main__":

    vs = [
        'Jet_CSV', 'Jet_CSVIVF', 'Jet_JP', 'Jet_JBP', 'Jet_SoftMu', 'Jet_SoftEl', 'Jet_pt', 'Jet_eta'
    ]

    vs2 = [
        'TagVarCSV_jetNTracks', 'TagVarCSV_jetNTracksEtaRel', 'TagVarCSV_trackSumJetEtRatio', 'TagVarCSV_trackSumJetDeltaR', 'TagVarCSV_trackSip2dValAboveCharm', 'TagVarCSV_trackSip2dSigAboveCharm', 'TagVarCSV_trackSip3dValAboveCharm', 'TagVarCSV_trackSip3dSigAboveCharm', 'TagVarCSV_vertexCategory', 'TagVarCSV_jetNSecondaryVertices', 'TagVarCSV_vertexMass', 'TagVarCSV_vertexNTracks', 'TagVarCSV_vertexEnergyRatio', 'TagVarCSV_vertexJetDeltaR', 'TagVarCSV_flightDistance2dVal',
        'TagVarCSV_flightDistance2dSig', 'TagVarCSV_flightDistance3dVal', 'TagVarCSV_flightDistance3dSig', 'TagVarCSV_trackSip2dSig_0', 'TagVarCSV_trackSip2dSig_1', 'TagVarCSV_trackSip2dSig_2', 'TagVarCSV_trackSip2dSig_3', 'TagVarCSV_trackSip3dSig_0', 'TagVarCSV_trackSip3dSig_1', 'TagVarCSV_trackSip3dSig_2', 'TagVarCSV_trackSip3dSig_3', 'TagVarCSV_trackPtRel_0', 'TagVarCSV_trackPtRel_1', 'TagVarCSV_trackPtRel_2', 'TagVarCSV_trackPtRel_3', 'TagVarCSV_trackDeltaR_0', 'TagVarCSV_trackDeltaR_1',
        'TagVarCSV_trackDeltaR_2', 'TagVarCSV_trackDeltaR_3', 'TagVarCSV_trackPtRatio_0', 'TagVarCSV_trackPtRatio_1', 'TagVarCSV_trackPtRatio_2', 'TagVarCSV_trackPtRatio_3', 'TagVarCSV_trackJetDist_0', 'TagVarCSV_trackJetDist_1', 'TagVarCSV_trackJetDist_2', 'TagVarCSV_trackJetDist_3', 'TagVarCSV_trackDecayLenVal_0', 'TagVarCSV_trackDecayLenVal_1', 'TagVarCSV_trackDecayLenVal_2', 'TagVarCSV_trackDecayLenVal_3', 'TagVarCSV_trackEtaRel_0', 'TagVarCSV_trackEtaRel_1', 'TagVarCSV_trackEtaRel_2',
        'TagVarCSV_trackEtaRel_3', 'Jet_CSV', 'Jet_CSVIVF', 'Jet_JP', 'Jet_JBP', 'Jet_SoftMu', 'Jet_SoftEl', 'Jet_pt', 'Jet_eta'
    ]

    prepare_xgb_format(fn, [
        (vs2, "eval_set_allvars"),
        (vs, "eval_set_cmva")
    ])
