import sys
#add xgboost
sys.path += ["/mnt/t3nfs01/data01/shome/jpata/xgboost/python-package"]

import sklearn_cls
import pandas
import numpy as np
import json
import os

def prepare_xgb_format(infile, cache_dir, variable_sets):
    dd = pandas.concat([
        sklearn_cls.preprocess(
            sklearn_cls.load_data(
                infile,
                "tree_{0}".format(fl),
#                start=0, stop=50000
            )
        ) for fl in ["b", "c", "l"]
    ])
        
    is_training = dd["is_training"]==1
    
    for vs, outname, eval_target in variable_sets:
        logging.info("creating eval_set for {0}, {1} variables".format(
            outname,
            len(vs)
        ))
        dd["target"] = dd.eval(eval_target).astype("int32")
        logging.info("targets:\n{0}".format(dd["target"].value_counts()))
        eval_set = [
            #training set
            (
                dd.ix[is_training, vs].as_matrix(),
                dd.ix[is_training, "target"].as_matrix()
            ),
            #evaluation set
            (
                dd.ix[np.invert(is_training), vs].as_matrix(),
                dd.ix[np.invert(is_training), "target"].as_matrix()
            )
        ]
        sklearn_cls.save_set(eval_set, os.path.join(cache_dir, outname))

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)

    infile = open(sys.argv[1])
    conf = json.load(infile)
    infile.close()

    data_prep_objects = conf["data_preparation"]

    varsets = []
    for do in data_prep_objects:
        varsets += [(do["variables"], do["name"], do["eval_target"])]
    # vs2 = [
    #     'TagVarCSV_jetNTracks', 'TagVarCSV_jetNTracksEtaRel', 'TagVarCSV_trackSumJetEtRatio', 'TagVarCSV_trackSumJetDeltaR', 'TagVarCSV_trackSip2dValAboveCharm', 'TagVarCSV_trackSip2dSigAboveCharm', 'TagVarCSV_trackSip3dValAboveCharm', 'TagVarCSV_trackSip3dSigAboveCharm', 'TagVarCSV_vertexCategory', 'TagVarCSV_jetNSecondaryVertices', 'TagVarCSV_vertexMass', 'TagVarCSV_vertexNTracks', 'TagVarCSV_vertexEnergyRatio', 'TagVarCSV_vertexJetDeltaR', 'TagVarCSV_flightDistance2dVal',
    #     'TagVarCSV_flightDistance2dSig', 'TagVarCSV_flightDistance3dVal', 'TagVarCSV_flightDistance3dSig', 'TagVarCSV_trackSip2dSig_0', 'TagVarCSV_trackSip2dSig_1', 'TagVarCSV_trackSip2dSig_2', 'TagVarCSV_trackSip2dSig_3', 'TagVarCSV_trackSip3dSig_0', 'TagVarCSV_trackSip3dSig_1', 'TagVarCSV_trackSip3dSig_2', 'TagVarCSV_trackSip3dSig_3', 'TagVarCSV_trackPtRel_0', 'TagVarCSV_trackPtRel_1', 'TagVarCSV_trackPtRel_2', 'TagVarCSV_trackPtRel_3', 'TagVarCSV_trackDeltaR_0', 'TagVarCSV_trackDeltaR_1',
    #     'TagVarCSV_trackDeltaR_2', 'TagVarCSV_trackDeltaR_3', 'TagVarCSV_trackPtRatio_0', 'TagVarCSV_trackPtRatio_1', 'TagVarCSV_trackPtRatio_2', 'TagVarCSV_trackPtRatio_3', 'TagVarCSV_trackJetDist_0', 'TagVarCSV_trackJetDist_1', 'TagVarCSV_trackJetDist_2', 'TagVarCSV_trackJetDist_3', 'TagVarCSV_trackDecayLenVal_0', 'TagVarCSV_trackDecayLenVal_1', 'TagVarCSV_trackDecayLenVal_2', 'TagVarCSV_trackDecayLenVal_3', 'TagVarCSV_trackEtaRel_0', 'TagVarCSV_trackEtaRel_1', 'TagVarCSV_trackEtaRel_2',
    #     'TagVarCSV_trackEtaRel_3', 'Jet_CSV', 'Jet_CSVIVF', 'Jet_JP', 'Jet_JBP', 'Jet_SoftMu', 'Jet_SoftEl', 'Jet_pt', 'Jet_eta'
    # ]

    prepare_xgb_format(conf["infile"], conf["cache_dir"], varsets)
