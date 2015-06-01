#include "RecoBTag/TagVarExtractor/interface/TagVarBranches.h"
#include <assert.h>
#include "TFile.h"
#include "TH2D.h"
#include "TList.h"
#include <iostream>
#include <sstream>
#include <vector>

using namespace std;
const int NMAX = 10000;

int main(int argc, char** argv) {
    assert(argc == 3);
    const char* infile_name = argv[1];
    const char* tree_name = argv[2];
    TFile* inf = new TFile(infile_name);
    TTree* tree = (TTree*)inf->Get(tree_name);
    assert(tree != 0);
   
    TagVarBranches tagvars;
    tagvars.doTagVarsCSV = false;
    tagvars.ReadTree(tree);


    TH2D counter("hcounter", "hcounter", 10, 30, 530, 10, 0.0, 2.5);
    TFile* outfile = new TFile("outfile.root", "RECREATE");
    vector<TTree*> trees; 
    
    for (int nx=0; nx<12; nx++) {
        for (int ny=0; ny<12; ny++) {
            stringstream ss;
            ss << "tree_pt_" << nx << "_eta_" << ny;
            const char* tn = ss.str().c_str();

            TTree* tree = new TTree(tn, tn);
            trees.push_back(tree);
            tagvars.RegisterTree(tree);
        }
    }
    cout << "Looping over " << tree->GetEntries() << " events" << endl;
    for(int i=0; i<tree->GetEntries(); i++) {
        memset(&tagvars, 0x00, sizeof(tagvars));
        tree->GetEntry(i);

        int nb = counter.FindBin(tagvars.Jet_pt, std::abs(tagvars.Jet_eta));
        
        assert(nb>=0 && nb<trees.size());
       
        if (trees[nb]->GetEntries() < NMAX) {
            trees[nb]->Fill();
        }
    }
    TList treelist;
    for(auto& tree : trees) {
        treelist.Add(tree);
    }

    TTree* tot = TTree::MergeTrees(&treelist);
    tot->SetName(tree->GetName());
    tot->Write();
    outfile->Close();
    return 0;
};
