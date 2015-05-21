#!/bin/bash
python python/project_bins.py tree_b test/ttjets.root ttjets &
python python/project_bins.py tree_c test/ttjets.root ttjets &
python python/project_bins.py tree_l test/ttjets.root ttjets &

python python/project_bins.py tree_b test/qcd.root qcd &
python python/project_bins.py tree_c test/qcd.root qcd &
python python/project_bins.py tree_l test/qcd.root qcd &
wait

#for x in training testing rest; do
#    for y in ttjets qcd; do
#        for z in b c l; do
#            #echo "$x $y $z"
#            hadd -f ${y}_${z}_${x}.root ${y}_tree_${z}_${x}_*.root
#        done
#    done
#done
