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
#include "./textGenReader.C"

bool compareVecByX(const std::vector<float>& a, const std::vector<float>& b) {
	return a[0] < b[0];
};

void preprocessMLP(TString iFileStr) {

	//TODO
	// open txt file, get pdg and start pos
	TString inFstrTxt = "../txt/multi-";
	inFstrTxt += iFileStr;
	inFstrTxt += ".txt";
	textGenReader* txtReader = new textGenReader((string)inFstrTxt);

	TString inFstr = "../anatree_";
	inFstr += iFileStr;
	inFstr += ".root";
	TFile* inF = new TFile(inFstr, "OPEN");
	if(!inF){
		cout << "Falied to load input file, exiting" << endl;
		return;
	}
	TDirectory* dir = (TDirectory*)inF->Get("anatree");
	if(!dir) return;
	TTree* inT = (TTree*)dir->Get("GArAnaTree");
	if(!inT) return;

	if(inT->GetEntries() != txtReader->getNevents()){
		cout << "ana entries and txt file have different number of events, exiting!" << endl;
		return;
	}

	garEvt* gEvt = new garEvt();
	gEvt->SetBranchAddresses(inT);

	ofstream outf;
	string outFstr = "./csv/train_";
	outFstr += iFileStr;
	outFstr += ".csv";
	outf.open(outFstr.c_str());
	for(int iEvt=0; iEvt<inT->GetEntries(); iEvt++){
		if(iEvt%((inT->GetEntries())/10)==0) cout << iEvt*100./(inT->GetEntries()) << "%" << endl;
		inT->GetEntry(iEvt);

		float* txtEvtPos = txtReader->getEvtPos(iEvt);
		int txtEvtPDG = txtReader->getEvtPDG(iEvt);
		vector< vector<float> > hits;
		for(uint ihit=0; ihit<gEvt->HitSig->size(); ihit++){
			float* hitPos = new float[3];
			hitPos[0] = gEvt->HitX->at(ihit);
			hitPos[1] = gEvt->HitY->at(ihit);
			hitPos[2] = gEvt->HitZ->at(ihit);
			float hitDist = 0.;
			for(int ii=0; ii<3; ii++)
				hitDist += (hitPos[ii]-txtEvtPos[ii])*(hitPos[ii]-txtEvtPos[ii]);
			if(hitDist>400) continue;

			vector<float> hit;
			hit.push_back(gEvt->HitX->at(ihit));
			hit.push_back(gEvt->HitY->at(ihit));
			hit.push_back(gEvt->HitZ->at(ihit));
			hit.push_back(gEvt->HitSig->at(ihit));
			hits.push_back(hit);
		}
		if(hits.size() > 200) continue;

		std::sort(hits.begin(), hits.end(),compareVecByX);
		float origin[3] = {0,0,0};
		if(hits.size() > 0){
			for(uint ii=0; ii<3; ii++){
				origin[ii] = hits.at(0).at(ii);
			}
		}

		for(uint ii=0; ii<hits.size(); ii++){
			for(uint jj=0; jj<3; jj++){
				hits.at(ii).at(jj) = hits.at(ii).at(jj) - origin[jj];
			}
		}
	
		outf << txtEvtPDG << ",";
		uint iprint=0;
		for(uint ii=0; ii<hits.size(); ii++){
			for(uint jj=0; jj<hits.at(ii).size(); jj++){
				outf << hits.at(ii).at(jj) << ",";
				iprint++;
			}
		}

		while(iprint<800){
			outf << "0";
			iprint++;
			if(iprint<800) outf << ",";
		}
		outf << endl;
	}

	inF->Close();
	outf.close();
}
