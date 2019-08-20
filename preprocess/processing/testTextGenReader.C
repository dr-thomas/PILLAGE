#include "./textGenReader.C"

void testTextGenReader(){
	textGenReader* reader = new textGenReader("../txt/multi-0000.txt");
	reader->printSampleLine(22);
	float* pos = reader->getEvtPos(22);
	for(int ii=0; ii<3; ii++){
		cout << pos[ii] << endl;
	}
	cout << reader->getEvtPDG(22) << endl;
}
