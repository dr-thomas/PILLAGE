#include <iostream>
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TCanvas.h>
#include <TMath.h>
#include <TStyle.h>
#include <TLatex.h>
#include <fstream>
#include "../../EvtDisp/evtClass.C"

void preprocessMLPpsAndPis() {

	TFile* inF = new TFile("./rootFiles/anatree_0000.root", "OPEN");
	if(!inF){
		cout << "Falied to load input file, exiting" << endl;
		return;
	}
	TDirectory* dir = (TDirectory*)inF->Get("anatree");
	if(!dir) return;
	TTree* inT = (TTree*)dir->Get("GArAnaTree");
	if(!inT) return;

	garEvt* gEvt = new garEvt();
	gEvt->SetBranchAddresses(inT);

	TH1F* hitsHist = new TH1F("hitsHist", "", 50, 0, 10000);

	TH1F* nPsHist = new TH1F("nPsHist", "", 50, 0, 10);
	TH1F* nPisHist = new TH1F("nPisHist", "", 50, 0, 10);
	TH1F* nTotHist = new TH1F("nTotHist", "", 50, 0, 10);

	for(int iEvt=0; iEvt<inT->GetEntries(); iEvt++){
		//if(iEvt%((inT->GetEntries())/10)==0) cout << iEvt*100./(inT->GetEntries()) << "%" << endl;
		inT->GetEntry(iEvt);
		if(gEvt->HitSig->size() > 1000) continue;
		hitsHist->Fill(gEvt->HitSig->size());
		int nPs = 0;
		int nPis = 0;
		for(uint ii=0; ii<gEvt->PDG->size(); ii++){
			int pdg = gEvt->PDG->at(ii);
			if(pdg==2212){
				nPs++;
			} else if(pdg==211){
				nPis++;
			} else {
				break;
			}
		}
		nPsHist->Fill(nPs);
		nPisHist->Fill(nPis);
		nTotHist->Fill(nPs+nPis);
	}

	TCanvas* c = new TCanvas;
	hitsHist->Draw();
	c->Print("~/Desktop/hitsSize.png");

	c = new TCanvas;
	nPsHist->Draw();
	c->Print("~/Desktop/nPs.png");

	c = new TCanvas;
	nPisHist->Draw();
	c->Print("~/Desktop/nPis.png");

	c = new TCanvas;
	nTotHist->Draw();
	c->Print("~/Desktop/nTot.png");

	inF->Close();
}
