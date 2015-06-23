#include <assert.h>
#include "TFile.h"
#include "TTree.h"
#include "TH2D.h"
#include <iostream>
#include <sstream>
#include <vector>
#include <algorithm>

int main(int argc, char** argv) {
    TFile* tf = new TFile(argv[1]);
    TTree* tr = (TTree*)tf->Get(argv[2]);
    
    float pt = 0;
    float eta = 0;
    float w = 0;
    float flavour = 0;
    tr->SetBranchAddress("Jet_pt", &pt);
    tr->SetBranchAddress("Jet_eta", &eta);
    tr->SetBranchAddress("Jet_flavour", &flavour);
    tr->SetBranchAddress("Jet_Weight", &w);
    
    TFile* of = new TFile(argv[3], "RECREATE");
    TTree* tr2 = tr->CloneTree(0);
    
    TFile* wfile = new TFile("../data/jun17/tt_weights.root");
    TH2D* hb = (TH2D*)wfile->Get("hb");
    TH2D* hc = (TH2D*)wfile->Get("hc");
    TH2D* hl = (TH2D*)wfile->Get("hl");

    for (int i=0; i<tr->GetEntries(); i++) {
        tr->GetEntry(i);
        TH2D* h = 0;
        if (std::abs(flavour) == 5) h = hb; 
        else if (std::abs(flavour) == 4) h = hc; 
        else h = hl;

        w = h->GetBinContent(h->FindBin(std::abs(eta), pt));
        tr2->Fill();
    }
    of->Write();
    of->Close();
    return 0;
};
    
