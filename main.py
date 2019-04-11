import os
import csv
from RANSAC import process_ransac
import numpy as np
import pickle
import matplotlib.pyplot as plt

mlp_regressor = pickle.load(open('./model_saves/protons_nn_full_ss_new.sav', 'rb'))

res_hist = np.array([])
class event_momentums():
    def __init__(self):
        self.pred_moms = []
        self.true_moms = []
momentum_data_out = []

tagged_path = './data/multiple_protons_0-200/csv/momentum-tagged/'
for ifile, file_name in enumerate(os.listdir(tagged_path)):
    print('on file:', ifile, 'out of', len(os.listdir(tagged_path)))
    file_path = tagged_path + file_name
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            n_particles = 0
            true_momenta = []
            hit_data = []
            for ifeature, feature in enumerate(row):
                if ifeature == 0:
                    n_particles = int(float(feature))
                elif ifeature <= n_particles:
                    true_momenta.append(float(feature))
                else:
                    hit_data.append(float(feature))

            clusters = process_ransac.cluster(hit_data)

            pred_moms = []
            for cluster in clusters:
                data_X = np.ndarray((1,len(cluster)))
                for ii, cc in enumerate(cluster):
                    data_X[0][ii] = float(cc)
                pred_moms.append(mlp_regressor.predict(data_X))

            evt_moms = event_momentums()
            for mm in pred_moms:
                evt_moms.pred_moms.append(mm)
            for mm in true_momenta:
                evt_moms.true_moms.append(mm*1000.)
            momentum_data_out.append(evt_moms)

            min_residual = [555e10 for ii in range(len(pred_moms))]
            for ii in range(len(pred_moms)):
                if pred_moms[ii][0] < 100:
                    continue
                for jj in range(len(true_momenta)):
                    #print(pred_moms[ii], true_momenta[jj]*1000.)
                    residual = pred_moms[ii][0] - true_momenta[jj]*1000.
                    if abs(residual) < abs(min_residual[ii]):
                        min_residual[ii] = residual

            for rr in min_residual:
                if rr < 1e3:
                    res_hist = np.append(res_hist, rr)

pickle.dump(momentum_data_out, open('event_momentum_data.sav', 'wb'))

plt.figure()
ax = plt.subplot(111)
ax.hist(res_hist, bins=100)
ax.set_xlabel("min. residual (MeV/c)")

mu = res_hist.mean()
sigma = res_hist.std()
textstr = '\n'.join((
    r'$\mu=%.2f$' % (mu, ),
    r'$\sigma=%.3f$' % (sigma, )))

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
ax.text(0.75, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

plt.savefig("./residuals_hist.png")

