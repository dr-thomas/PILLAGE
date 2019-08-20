#include <iostream>
#include <fstream>
#include <string>
#include <vector>

vector<string> split(const string& str, const string& delim)
{
	vector<string> tokens;
	size_t prev = 0, pos = 0;
	do
	{
		pos = str.find(delim, prev);
		if (pos == string::npos) pos = str.length();
		string token = str.substr(prev, pos-prev);
		if (!token.empty()) tokens.push_back(token);
		prev = pos + delim.length();
	}
	while (pos < str.length() && prev < str.length());
	return tokens;
}

class textGenReader {
	private:
		vector<vector<string> > data;
		//pdg,x,y,z
	public:
		textGenReader(string filename){
			ifstream file(filename.c_str());
			string line = "";
			while(getline(file, line)){
				vector<string> linedata = split(line, " ");
				if(linedata.size()==2) continue;
				vector<string> keepdata;
				keepdata.push_back(linedata.at(1));//pdg
				keepdata.push_back(linedata.at(11));//x
				keepdata.push_back(linedata.at(12));//y
				keepdata.push_back(linedata.at(13));//z
				data.push_back(keepdata);
			}
			file.close();
		}
		~textGenReader(){
		}

		int getEvtPDG(int evtIndex){
			return atoi(data.at(evtIndex).at(0).c_str());
		}
		float* getEvtPos(int evtIndex){
			float* out = new float[3];
			for(size_t ii=0; ii<3; ii++){
				out[ii] = atof(data.at(evtIndex).at(ii+1).c_str());
			}
			return out;
		}
		int getNevents(){
			return data.size();
		}

		//test fxns 
		void printData(){
			for(size_t irow=0; irow<data.size(); irow++){
				for(size_t icol=0; icol<data.at(irow).size(); icol++){
					cout << (data.at(irow).at(icol)) << " ";
				}
				cout << endl;
			}
		}
		void printSampleLine(int line){
			for(size_t ii=0; ii<data.at(line).size(); ii++){
				cout << ii << " " << data.at(line).at(ii) << endl;
			}
		}
};
