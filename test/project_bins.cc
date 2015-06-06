#include "RecoBTag/TagVarExtractor/interface/TagVarBranches.h"
#include <assert.h>
#include "TFile.h"
#include "TMemFile.h"
#include "TH2D.h"
#include "TList.h"
#include <iostream>
#include <sstream>
#include <vector>

using namespace std;
const int NMAX = 1000;

int main(int argc, char** argv) {
    assert(argc == 4);
    const char* infile_name = argv[1];
    const char* tree_name = argv[2];
    const char* outfile_name = argv[3];
    TFile* inf = new TFile(infile_name);
    TTree* tree = (TTree*)inf->Get(tree_name);
    assert(tree != 0);
   
    TagVarBranches tagvars;
    tagvars.doTagVarsCSV = true;
    tagvars.ReadTree(tree);

    int Nx = 100;
    int Ny = 100;
    TFile* outfile = new TFile(outfile_name, "RECREATE");
    TH2D counter("hcounter", "hcounter", Nx, 20, 620, Ny, 0.0, 2.5);
    vector<TTree*> trees; 
    
    for (int nx=0; nx<Nx+2; nx++) {
        for (int ny=0; ny<Ny+2; ny++) {
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
            counter.Fill(tagvars.Jet_pt, std::abs(tagvars.Jet_eta));
            trees[nb]->Fill();
        }
    }
    TList treelist;
    for(auto& tree : trees) {
        treelist.Add(tree);
    }

    TTree* _tot = TTree::MergeTrees(&treelist);
    _tot->SetDirectory(outfile);

    cout << "Saving..." << endl;
    _tot->SetName("tree");
    _tot->SetTitle("tree");
    _tot->Write("", TObject::kOverwrite);
    counter.Write("", TObject::kOverwrite);
    treelist.Delete();
    outfile->Close();
    return 0;
};
