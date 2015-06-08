#include "RecoBTag/TagVarExtractor/interface/TagVarBranches.h"
#include <assert.h>
#include "TFile.h"
#include "TMemFile.h"
#include "TH2D.h"
#include "TList.h"
#include <iostream>
#include <sstream>
#include <vector>
#include <algorithm>

using namespace std;
const int NMAX = 100;

void save_coll(TFile* outfile, TTree* in, TagVarBranches* tv, vector<vector<unsigned long int>> trees, const char* name) {
    TTree* _tot = new TTree(name, name);
    tv->RegisterTree(_tot);
    //_tot->SetAutoFlush(100000);
    //_tot->SetAutoSave(100000);
    //_tot->SetDirectory(outfile);
    int n = 0;
    in->SetCacheSize(0);
    vector<unsigned int> inds;
    for (auto& tree: trees) {
        n += tree.size();
        for (unsigned int i : tree) {
            inds.push_back(i);
        }
    }
    sort(inds.begin(), inds.end());
    cout << "Looping " << name << " " << n << endl;
    for (unsigned int i : inds) {
        in->GetEntry(i);
        _tot->Fill();
        //if (_tot->GetEntries() % 1000 == 0) {
        //    cout << _tot->GetEntries();
        //}
    }
    cout << endl;
    cout << _tot->GetName() << " has " << _tot->GetEntries() << " entries" << endl;

    cout << "Saving..." << endl;
    _tot->Write("", TObject::kOverwrite);
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
    outfile->cd(); 
    TH2D counter("hcounter", "hcounter", Nx, 20, 620, Ny, 0.0, 2.5);
    vector<vector<unsigned long int>> trees_b;
    vector<vector<unsigned long int>> trees_c;
    vector<vector<unsigned long int>> trees_l;
    
    for (int nx=0; nx<Nx+2; nx++) {
        for (int ny=0; ny<Ny+2; ny++) {
            vector<unsigned long int> v;
            trees_b.push_back(v);
            trees_c.push_back(v);
            trees_l.push_back(v);
        }
    }

    cout << "Looping over " << tree->GetEntries() << " events" << endl;
    tree->SetBranchStatus("*", false);
    tree->SetBranchStatus("Jet_pt", true);
    tree->SetBranchStatus("Jet_eta", true);
    tree->SetBranchStatus("Jet_flavour", true);
    for(unsigned long int i=0; i<tree->GetEntries(); i++) {
        memset(&tagvars, 0x00, sizeof(tagvars));
        tree->GetEntry(i);

        int nb = counter.FindBin(tagvars.Jet_pt, std::abs(tagvars.Jet_eta));
      
        vector<vector<unsigned long int>>* treecoll = 0;
        if (std::abs(int(tagvars.Jet_flavour)) == 5) {
            treecoll = &(trees_b);
        }
        else if (std::abs(int(tagvars.Jet_flavour)) == 4) {
            treecoll = &(trees_c);
        }
        else {
            treecoll = &(trees_l);
        }

        assert(nb>=0 && nb < treecoll->size());
       
        if ((*treecoll)[nb].size() < NMAX) {
            counter.Fill(tagvars.Jet_pt, std::abs(tagvars.Jet_eta));
            (*treecoll)[nb].push_back(i);
        }
    }
    tree->SetBranchStatus("*", true);
    
    save_coll(outfile, tree, &tagvars, trees_b, "tree_b");
    save_coll(outfile, tree, &tagvars, trees_c, "tree_c");
    save_coll(outfile, tree, &tagvars, trees_l, "tree_l");
    
    counter.Write("", TObject::kOverwrite);
    outfile->Close();
    return 0;
};
    
