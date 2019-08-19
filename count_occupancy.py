import csv
import numpy as np
import os
import matplotlib.pyplot as plt

class event_momentums():
    def __init__(self):
        self.pred_moms = []
        self.true_moms = []

tagged_path = './data/multiple_protons_0-200/csv/momentum-tagged/'
in_file_list = []
for ifile, file_name in enumerate(os.listdir(tagged_path)):
    file_path = tagged_path + file_name
    in_file_list.append(file_path)

evt_occupancies = np.ndarray([])

for ifile, file_path in enumerate(in_file_list):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            evt_moms = event_momentums()
            n_particles = 0
            hit_data = []
            for ifeature, feature in enumerate(row):
                if ifeature == 0:
                    n_particles = int(float(feature))
                if ifeature > n_particles:
                    hit_data.append(float(feature))

            if len(hit_data) == 0:
                continue

            tot_vol = [[555e10, -555e10] for ii in range(3)]
            for ii, hh in enumerate(hit_data):
                index = ii%4
                if index == 3:
                    continue
                if hh < tot_vol[index][0]:
                    tot_vol[index][0] = hh
                if hh > tot_vol[index][1]:
                    tot_vol[index][1] = hh

            voxel_size = [2.,1.5,1]
            nvoxels = [int(1+(tot_vol[ii][1]-tot_vol[ii][0])/voxel_size[ii]) for ii in range(3)]
            voxels = [[(tot_vol[ii][0]+voxel_size[ii]*jj) for jj in range(nvoxels[ii])] for ii in range(3)]
            voxel_was_hit = [[[0 for kk in range(nvoxels[2])] for jj in range(nvoxels[1])] for ii in range(nvoxels[0])]

            voxel_indecies = [-1,-1,-1]
            for ihit, hit in enumerate(hit_data):
                index = ihit%4
                if index == 3:
                    skip = False
                    for ii in voxel_indecies:
                        if ii < 0:
                            skip = True
                    if not skip:
                        voxel_was_hit[voxel_indecies[0]][voxel_indecies[1]][voxel_indecies[2]] += 1

                    voxel_indecies = [-1,-1,-1]
                    continue

                found_voxel_index = -1
                if len(voxels[index]) == 1:
                    found_voxel_index = 0
                for ii, vv in enumerate(voxels[index]):
                    if hit < vv:
                        found_voxel_index = (ii-1)
                        break
                voxel_indecies[index] = found_voxel_index

            nvoxels_tot = 0
            nvoxels_occ = 0
            for xx in voxel_was_hit:
                for yy in xx:
                    for zz in yy:
                        nvoxels_tot += 1
                        if zz > 0:
                            nvoxels_occ += 1

            if nvoxels_tot > 1:
                occupation = float(nvoxels_occ/nvoxels_tot)
                if occupation > 0. and occupation < 1.:
                    #print(occupation)
                    evt_occupancies = np.append(evt_occupancies, occupation)
                #print('occupation:', occupation, nvoxels_occ, nvoxels_tot)

for ii in range(len(evt_occupancies)):
    if evt_occupancies[ii] > 1 or evt_occupancies[ii] < 0:
        evt_occupancies[ii] = 0.


plt.figure()
ax = plt.subplot(111)
ax.hist(evt_occupancies, bins=100)
ax.set_title("Occupancy")
ax.set_xlabel("fractional occupancy")

mu = evt_occupancies.mean()
sigma = evt_occupancies.std()
textstr = '\n'.join((
    r'$\mu=%.2f$' % (mu, ),
    r'$\sigma=%.3f$' % (sigma, )))

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
ax.text(0.75, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

plt.savefig("./occupancies.png")



