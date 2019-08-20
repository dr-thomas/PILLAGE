#! /usr/bin/python

"should be ran in directory where it lives"
"make sure envirionment is properly set up before running this script"

import os
import time

for ii in range(0,10000):
        os.system('Qsub -e -l sl6 -N makeTrainCsv%0004d -o logFiles/log%0004d.log "root -l -b -q \'preprocessMLP.C+(\\\"%0004d\\\")\'"'%(ii,ii,ii))
	time.sleep(2)
