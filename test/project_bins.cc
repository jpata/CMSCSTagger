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

void save_coll(TFile* outfile, vector<TTree*> trees, const char* name) {
    TList treelist;
    for(auto& tree : trees) {
        treelist.Add(tree);
    }

    TTree* _tot = TTree::MergeTrees(&treelist);
    _tot->SetDirectory(outfile);

    cout << "Saving..." << endl;
    _tot->SetName(name);
    _tot->SetTitle(name);
    _tot->Write("", TObject::kOverwrite);
    treelist.Delete();
}

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
    vector<TTree*> trees_b; 
    vector<TTree*> trees_c; 
    vector<TTree*> trees_l; 
    
    for (int nx=0; nx<Nx+2; nx++) {
        for (int ny=0; ny<Ny+2; ny++) {
            stringstream ss;
            ss << "tree_pt_" << nx << "_eta_" << ny;
            const string tn = ss.str();

            TTree* tree_b = new TTree((tn + "_b").c_str(), tn.c_str());
            trees_b.push_back(tree_b);
            tagvars.RegisterTree(tree_b);
            
            TTree* tree_c = new TTree((tn + "_c").c_str(), tn.c_str());
            trees_c.push_back(tree_c);
            tagvars.RegisterTree(tree_c);
            
            TTree* tree_l = new TTree((tn + "_l").c_str(), tn.c_str());
            trees_l.push_back(tree_l);
            tagvars.RegisterTree(tree_l);
        }
    }

    cout << "Looping over " << tree->GetEntries() << " events" << endl;
    for(int i=0; i<tree->GetEntries(); i++) {
        memset(&tagvars, 0x00, sizeof(tagvars));
        tree->GetEntry(i);

        int nb = counter.FindBin(tagvars.Jet_pt, std::abs(tagvars.Jet_eta));
      
        vector<TTree*>* treecoll = 0;
        if (std::abs(tagvars.Jet_flavour) == 5) {
            treecoll = &(trees_b);
        }
        else if (std::abs(tagvars.Jet_flavour) == 4) {
            treecoll = &(trees_c);
        }
        else {
            treecoll = &(trees_l);
        }

        assert(nb>=0 && nb < treecoll->size());
       
        if ((*treecoll)[nb]->GetEntries() < NMAX) {
            counter.Fill(tagvars.Jet_pt, std::abs(tagvars.Jet_eta));
            (*treecoll)[nb]->Fill();
        }
    }
    
    save_coll(outfile, trees_b, "tree_b");
    save_coll(outfile, trees_c, "tree_c");
    save_coll(outfile, trees_l, "tree_l");
    
    counter.Write("", TObject::kOverwrite);
    outfile->Close();
    return 0;
};
    
