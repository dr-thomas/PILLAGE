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
#include "./evtClass.C"

/* TODO:
 *      
 *      - Clean up this and parent directory, git commit
 *      - Truth Match tracks .... not yet .... 
 */

void preprocessMLP() {

	TFile* inF = new TFile("./rootFiles/anatree_0000.root", "OPEN");
	if(!inF){
		cout << "Falied to load input file, exiting" << endl;
		return;
	}
	TDirectory* dir = (TDirectory*)inF->Get("anatree");
	if(!dir) return;
	TTree* inT = (TTree*)dir->Get("GArAnaTree");
	//TTree* inT = (TTree*)inF->Get("GArAnaTree");
	if(!inT) return;

	garEvt* gEvt = new garEvt();
	gEvt->SetBranchAddresses(inT);

	ofstream outf;
	outf.open("train.csv");
	for(int iEvt=0; iEvt<inT->GetEntries(); iEvt++){
		if(iEvt%((inT->GetEntries())/10)==0) cout << iEvt*100./(inT->GetEntries()) << "%" << endl;
		inT->GetEntry(iEvt);
		if(gEvt->PDG->at(0)!=2212) continue;
		if(gEvt->HitSig->size()>250) continue;
		float pMomTrue = 0;
		pMomTrue += (gEvt->MCPPX->at(0))*(gEvt->MCPPX->at(0));
		pMomTrue += (gEvt->MCPPY->at(0))*(gEvt->MCPPY->at(0));
		pMomTrue += (gEvt->MCPPZ->at(0))*(gEvt->MCPPZ->at(0));
		pMomTrue = TMath::Sqrt(pMomTrue);
		vector<vector<float>> hits;
		for(uint ihit=0; ihit<gEvt->HitSig->size(); ihit++){
			vector<float> hit;
			hit.push_back(gEvt->HitX->at(ihit));
			hit.push_back(gEvt->HitY->at(ihit));
			hit.push_back(gEvt->HitZ->at(ihit));
			hit.push_back(gEvt->HitSig->at(ihit));
			hits.push_back(hit);
		}
		std::sort(hits.begin(), hits.end(),
          [](const std::vector<float>& a, const std::vector<float>& b) {
		  return a[0] < b[0];
		  });
		for(uint ii=0; ii<hits.size(); ii++){
			for(uint jj=0; jj<3; jj++){
				hits.at(ii).at(jj) -= hits.at(0).at(jj);
			}
		}

		/*
		cout << "sorted, relative:" << endl;
		for(uint ii=0; ii<hits.size(); ii++){
			for(uint jj=0; jj<hits.at(ii).size(); jj++){
				cout << hits.at(ii).at(jj) << " ";
			}
			cout << endl;
		}
		*/

		outf << pMomTrue << ",";
		uint iprint=0;
		for(uint ii=0; ii<hits.size(); ii++){
			for(uint jj=0; jj<hits.at(ii).size(); jj++){
				outf << hits.at(ii).at(jj) << ",";
				iprint++;
			}
		}
		while(iprint<1000){
			outf << "0";
			iprint++;
			if(iprint<1000) outf << ",";
		}
		outf << endl;
	}

	inF->Close();
	outf.close();
}
