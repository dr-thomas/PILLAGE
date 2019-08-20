"""
read_train_data turns the csv output of ./preprocessMLP.C into numpy arrays to toss at models
"""
import csv
import numpy as np
import os
import math

xdata_in = []
ydata_in = []
ydata_E_in = []

nclasses = 7
PDGs = {}
PDGs[2212] = 0
PDGs[211] = 1
PDGs[-211] = 2
PDGs[13] = 3
PDGs[-13] = 4
PDGs[11] = 5
PDGs[-11] = 6

PDG_masses = {}
PDG_masses[2212] = 0.938
PDG_masses[211] = 0.139
PDG_masses[-211] = 0.139
PDG_masses[13] = 0.106
PDG_masses[-13] = 0.106
PDG_masses[11] = 0.000511
PDG_masses[-11] = 0.000511

csvpath = "./csv/PID/delta20cmFull/"
for ii, filename in enumerate(os.listdir(csvpath)):
    print("on file:", ii)
    filepath = csvpath + filename
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            xdata_row = []
            ydata_row = [0 for ii in range(nclasses)]
            skip = False
            temp_mass = -1.
            for ii, rr in enumerate(row):
                if ii == 0:
                    if int(PDGs[int(rr)]) == -1:
                        skip = True
                        break
                    ydata_row[int(PDGs[int(rr)])] = 1
                    ydata_in.append(ydata_row)
                    temp_mass = float(PDG_masses[int(rr)])
                elif ii == 1:
                    temp_E = float(rr)
                    if temp_E > temp_mass:
                        temp_mom = math.sqrt((temp_E)**2-temp_mass**2)
                    else:
                        temp_mom = 0.
                    ydata_E_in.append(temp_mom)
                    xdata_row.append(temp_mom)
                else:
                    xdata_row.append(rr)
            if not skip:
                xdata_in.append(xdata_row)

xdata = np.ndarray((len(xdata_in),len(xdata_in[0])))
print(len(xdata_in), len(xdata_in[0]))
for ii, xx in enumerate(xdata_in):
    for jj, yy in enumerate(xx):
        if ii>=len(xdata_in) or jj>=len(xdata_in[0]):
            continue
        xdata[ii][jj] = yy

ydata = np.ndarray((len(ydata_in),len(ydata_in[0])))
ydata_E = np.ndarray(len(ydata_in))
print(len(ydata_in), len(ydata_in[0]))
for ii, xx in enumerate(ydata_in):
    ydata_E[ii] = ydata_E_in[ii]
    for jj, yy in enumerate(xx):
        if ii>=len(ydata_in) or jj>=len(ydata_in[0]):
            continue
        ydata[ii][jj] = yy

#ydata = np.ndarray(len(ydata_in))
#for ii, xx in enumerate(ydata_in):
#    ydata[ii] = xx

#np.save('./data/PID/X_train_Species_3.npy', xdata)
#np.save('./data/PID/y_train_Species_3.npy', ydata)
np.save('./full/all/X_train.npy', xdata)
np.save('./full/all/y_train.npy', ydata)
np.save('./full/all/y_train_E.npy', ydata_E)
