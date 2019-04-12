import pickle
import matplotlib.pyplot as plt
import numpy as np
import random

class event_momentums():
    def __init__(self):
        self.pred_moms = []
        self.true_moms = []

momentum_data = pickle.load(open('./model_saves/results/event_momentum_data_full.sav', 'rb'))

#TODO: look at predicted momentum distribution and true momentum distribution.  something maybe fishy about pred...
res_hist = np.array([])
res_mom_hist = np.array([])
pred_hist = np.array([])
true_hist = np.array([])
for evt in momentum_data:
    for pred_mom in evt.pred_moms:
        pred_hist = np.append(pred_hist, pred_mom)
    for true_mom in evt.true_moms:
        true_hist = np.append(true_hist, true_mom)
for evt in momentum_data:
    for pred_mom in evt.pred_moms:
        if pred_mom > 160. or pred_mom < 70.:
            continue
        min_residual = 555e10
        for true_mom in evt.true_moms:
            if abs(pred_mom-true_mom) < abs(min_residual):
                min_residual = pred_mom-true_mom
        if min_residual < 1e5:
            res_hist = np.append(res_hist, min_residual)
            res_mom_hist = np.append(res_mom_hist, pred_mom)

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

plt.savefig("./residuals_hist_test.png")

plt.figure()
ax = plt.subplot(111)
ax.hist2d(res_mom_hist, res_hist, bins=50)
ax.set_ylim([-50,50])
ax.set_xlabel("pred. momentum (MeV/c)")
ax.set_ylabel("min. residual (MeV/c)")
plt.savefig("./residuals_2D_hist.png")

plt.figure()
ax = plt.subplot(131)
ax.hist(pred_hist, bins=100)
ax.set_title("predicted")
ax = plt.subplot(132)
ax.hist(true_hist, bins=100)
ax.set_title("true")

smeared_true_hist = np.array([])
for mm in true_hist:
    if mm < 70 or mm > 160:
        continue
    randx = random.gauss(mu=1,sigma=0.2)
    smeared_true_hist = np.append(smeared_true_hist, mm*randx)
ax = plt.subplot(133)
ax.hist(smeared_true_hist, bins=100)
ax.set_xlim([0,200])
ax.set_title("smeared_true")

plt.tight_layout()
plt.savefig("./momentum_hists.png")

