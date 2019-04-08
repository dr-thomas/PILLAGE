import csv
import os
import math

def label_proton_mom_from_txt(download_csv_path, download_txt_path, write_path):

    txt_files = os.listdir(download_txt_path)
    csv_files = os.listdir(download_csv_path)
    txt_files.sort()
    csv_files.sort()
    if len(txt_files) != len(csv_files):
        print("number of text files and csv files do not match.  exiting")
        exit()
    for ifile in range(len(txt_files)):

        print('on file number:', ifile, 'of', len(txt_files))

        filepath_csv = download_csv_path + csv_files[ifile]
        hit_data = []
        with open(filepath_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                this_hit_data = []
                for ii, rr in enumerate(row):
                    if ii==0:
                        continue
                    this_hit_data.append(rr)
                hit_data.append(this_hit_data)

        filepath_txt = download_txt_path + txt_files[ifile]
        momentum_data = []
        with open(filepath_txt) as txt_file:
            csv_reader = csv.reader(txt_file, delimiter=' ')
            nparticles = 0
            ievent = 0
            iparticle = 0
            is_new_event = True
            evt_tot_momentums = []
            for row in csv_reader:
                if is_new_event:
                    nparticles = int(row[1])
                    iparticle = 0
                    if nparticles > 0:
                        is_new_event = False
                    else:
                        momentum_data.append([0])
                    continue
                if iparticle < nparticles and not is_new_event:
                    momentum = [row[ii+8] for ii in range(3)]
                    tot_momentum = 0.
                    for mm in momentum:
                        tot_momentum += float(mm)*float(mm)
                    tot_momentum = math.sqrt(tot_momentum)
                    evt_tot_momentums.append(tot_momentum)
                    iparticle += 1
                    if iparticle == nparticles:
                        is_new_event = True
                        momentum_data.append(evt_tot_momentums)
                        evt_tot_momentums = []


