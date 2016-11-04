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

//maximum number of entries per pt/eta bin
const int NMAX = 100;
//number of bins in pt/eta
const int Nx = 100;
const int Ny = 100;

void save_coll(TFile* outfile, TTree* in, TagVarBranches* tv, vector<vector<unsigned long int>> trees, const char* name) {
    int index = 0; 
    TTree* _tot = new TTree(name, name);
    tv->RegisterTree(_tot);
    _tot->Branch("index", &index, "index/I");
    //_tot->SetAutoFlush(100000);
    //_tot->SetAutoSave(100000);
    //_tot->SetDirectory(outfile);
    int n = 0;
    in->SetCacheSize(0);

    //get the total vector of all events
    vector<unsigned int> inds;
    for (auto& tree: trees) {
        n += tree.size();
        for (unsigned int i : tree) {
            inds.push_back(i);
        }
    }
    //sort it in increasing order to make scan fast
    sort(inds.begin(), inds.end());

    //copy all the given entries
    cout << "Looping " << name << " " << n << endl;
    unsigned int cur_entry = 0;
    for (unsigned int i : inds) {
        in->GetEntry(i);
        _tot->Fill();
        index = cur_entry%10;
        if (cur_entry % 100000 == 0) {
            cout << cur_entry << endl;
        }
        cur_entry += 1;
    }
    cout << _tot->GetName() << " has " << _tot->GetEntries() << " entries" << endl;

    cout << "Saving..." << endl;
    _tot->Write("", TObject::kOverwrite);
}

int main(int argc, char** argv) {
    if (argc != 4) {
        cerr << "project_bins infile.root tree outfile.root" << endl;
        exit(0);
    };
    const char* infile_name = argv[1];
    const char* tree_name = argv[2];
    const char* outfile_name = argv[3];
    TFile* inf = new TFile(infile_name);
    TTree* tree = (TTree*)inf->Get(tree_name);
    assert(tree != 0);
   
    TagVarBranches tagvars;
    tagvars.ReadTree(tree);

    TFile* outfile = new TFile(outfile_name, "RECREATE");
    outfile->cd(); 
    TH2D counter("hcounter", "hcounter", Nx, 20, 620, Ny, 0.0, 2.5);

    //store indices of events that belong to bins
    vector<vector<unsigned long int>> trees_b;
    vector<vector<unsigned long int>> trees_c;
    vector<vector<unsigned long int>> trees_l;
   
    //create empty vectors for each bin
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
    
    map<int, int> counters_pre;
    counters_pre[0] = 0;
    counters_pre[1] = 0;
    counters_pre[2] = 0;
    
    map<int, int> counters_post;
    counters_post[0] = 0;
    counters_post[1] = 0;
    counters_post[2] = 0;

    for(unsigned long int i=0; i<tree->GetEntries(); i++) {
        memset(&tagvars, 0x00, sizeof(tagvars));
        tree->GetEntry(i);

        //find the index of the bin where this jet belongs to
        int nb = counter.FindBin(tagvars.Jet_pt, std::abs(tagvars.Jet_eta));
        
        int map_idx = -1;
        vector<vector<unsigned long int>>* treecoll = 0;
        if (std::abs(int(tagvars.Jet_flavour)) == 5) {
            treecoll = &(trees_b);
            map_idx = 0;
        }
        else if (std::abs(int(tagvars.Jet_flavour)) == 4) {
            treecoll = &(trees_c);
            map_idx = 1;
        }
        else {
            treecoll = &(trees_l);
            map_idx = 2;
        }
        counters_pre[map_idx] += 1;

        assert(nb>=0 && nb < treecoll->size());
      
        //if we didn't already have too many events in this bin, fill it
        if ((*treecoll)[nb].size() < NMAX) {
            counter.Fill(tagvars.Jet_pt, std::abs(tagvars.Jet_eta));
            (*treecoll)[nb].push_back(i);
            counters_post[map_idx] += 1;
        }
    }
    tree->SetBranchStatus("*", true);
   
    for (int i=0; i < 3; i++) {
        cout << i << " pre=" << counters_pre[i] << " post=" << counters_post[i] << " frac=" << (float)(counters_post[i])/(float)(counters_pre[i]) << endl;
    }
    save_coll(outfile, tree, &tagvars, trees_b, "tree_b");
    save_coll(outfile, tree, &tagvars, trees_c, "tree_c");
    save_coll(outfile, tree, &tagvars, trees_l, "tree_l");
    
    counter.Write("", TObject::kOverwrite);
    outfile->Close();
    return 0;
};
    
