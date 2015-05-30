#!/bin/bash
set -e

#cat data/ttjets.txt | ~/parallel -j20 python python/dumper.py {} ttjets_{#}.root &
cat data/ttjets2.txt | ~/parallel -j20 python python/dumper.py {} ttjets2_{#}.root &
#cat data/qcd.txt | ~/parallel -j20 python python/dumper.py {} qcd_{#}.root &
#wait

#hadd -f test/ttjets.root ttjets_*.root
hadd -f test/ttjets2.root ttjets2_*.root
#hadd -f test/qcd.root qcd_*.root

rm ttjets2_*.root
#rm ttjets_*.root
#rm qcd_*.root

#python python/project_bins.py tree_b test/ttjets.root ttjets &
#python python/project_bins.py tree_c test/ttjets.root ttjets &
#python python/project_bins.py tree_l test/ttjets.root ttjets &

python python/project_bins.py tree_b test/ttjets2.root ttjets2 &
python python/project_bins.py tree_c test/ttjets2.root ttjets2 &
python python/project_bins.py tree_l test/ttjets2.root ttjets2 &

#python python/project_bins.py tree_b test/qcd.root qcd &
#python python/project_bins.py tree_c test/qcd.root qcd &
#python python/project_bins.py tree_l test/qcd.root qcd &
wait

for x in training testing rest; do
    #for y in ttjets2 ttjets qcd; do
    for y in ttjets2; do
        for z in b c l; do
            #echo "$x $y $z"
            hadd -f ${y}_${z}_${x}.root ${y}_tree_${z}_${x}_*.root
        done
    done
done

rm ttjets2_*tree*.root
#rm ttjets_*tree*.root
#rm qcd_*tree*.root
