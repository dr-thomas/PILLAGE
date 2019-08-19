import pickle
import matplotlib.pyplot as plt
import numpy as np
import random
import math

class event_momentums():
    def __init__(self):
        self.pred_moms = []
        self.true_moms = []

momentum_data = pickle.load(open('./event_momentum_data0001.sav', 'rb'))

#TODO: look at predicted momentum distribution and true momentum distribution.  something maybe fishy about pred...
res_hist = np.array([])
res_KE_hist = np.array([])
res_mom_hist = np.array([])

pred_hist = np.array([])
true_hist = np.array([])
for evt in momentum_data:
    for pred_mom in evt.pred_moms:
        pred_hist = np.append(pred_hist, pred_mom)
    for true_mom in evt.true_moms:
        if true_mom > 170.:
            print(true_mom)
        true_hist = np.append(true_hist, true_mom)

for evt in momentum_data:
    for pred_mom in evt.pred_moms:
        min_residual = 555e10
        for true_mom in evt.true_moms:
            if abs(pred_mom-true_mom) < abs(min_residual):
                min_residual = pred_mom-true_mom
        if min_residual < 1e5:
            res_hist = np.append(res_hist, min_residual)
            res_mom_hist = np.append(res_mom_hist, pred_mom)

res_KE_hist = np.array([])
pred_KE_hist = np.array([])
true_KE_hist = np.array([])
for evt in momentum_data:
    pred_KE_total = 0.
    true_KE_total = 0.
    for pred_mom in evt.pred_moms:
        pred_KE = math.sqrt(pred_mom*pred_mom+938.*938.)-938.
        pred_KE_total += pred_KE
        if pred_KE < 3 or pred_KE > 15:
            continue
        min_residual = 555e10
        closest_KE = 555e10
        for true_mom in evt.true_moms:
            true_KE = math.sqrt(true_mom*true_mom+938.*938.)-938.
            if abs(pred_KE-true_KE) < abs(min_residual):
                min_residual = pred_KE-true_KE
                closest_KE = true_KE
        if min_residual < 1e5:
            res_KE_hist = np.append(res_KE_hist, min_residual)
            true_KE_hist = np.append(true_KE_hist, closest_KE)
            pred_KE_hist = np.append(pred_KE_hist, pred_KE)

total_KE_residual_hist = np.array([])
pred_KE_total_hist = np.array([])
true_KE_total_hist = np.array([])
for evt in momentum_data:
    pred_KE_total = 0.
    for pred_mom in evt.pred_moms:
        pred_KE = math.sqrt(pred_mom*pred_mom+938.*938.)-938.
        pred_KE_total += pred_KE
    true_KE_total = 0.
    for true_mom in evt.true_moms:
        true_KE = math.sqrt(true_mom*true_mom+938.*938.)-938.
        true_KE_total += true_KE
    if abs(pred_KE_total-true_KE_total) < 50 and pred_KE_total > 3 and true_KE_total > 3 and pred_KE_total<15 and true_KE_total<15:
        pred_KE_total_hist = np.append(pred_KE_total_hist, pred_KE_total)
        true_KE_total_hist = np.append(true_KE_total_hist, true_KE_total)
        total_KE_residual_hist = np.append(total_KE_residual_hist, (pred_KE_total-true_KE_total))

n_eff_bins = 30
max_mom = 200.
eff_hist_pred = np.array([0 for ii in range(n_eff_bins)])
eff_hist_true = np.array([0 for ii in range(n_eff_bins)])
eff_KE_hist = np.array([(ii+1)*(max_mom/n_eff_bins) for ii in range(n_eff_bins)])
eff_hist_good = np.array([0 for ii in range(n_eff_bins)])
for evt in momentum_data:
    for pred_mom in evt.pred_moms:
        for ii, xx in enumerate(eff_KE_hist):
            if pred_mom < 1e-6:
                break
            if pred_mom > max_mom:
                break
            if pred_mom < xx:
                eff_hist_pred[ii] += 1.
                break
    for true_mom in evt.true_moms:
        temp_index = -1
        for ii, xx in enumerate(eff_KE_hist):
            if true_mom < 1e-6:
                break
            if true_mom > max_mom:
                break
            if true_mom < xx:
                eff_hist_true[ii] += 1.
                temp_index = ii
                break
        if temp_index > 0:
            for ipred, pred_mom in enumerate(evt.pred_moms):
                if abs(pred_mom - true_mom) < true_mom*0.2:
                    eff_hist_good[temp_index] += 1.
                    break

eff_hist = np.array([eff_hist_pred[ii]/eff_hist_true[ii] for ii in range(n_eff_bins)])
eff_hist_wasgood = np.array([eff_hist_good[ii]/eff_hist_true[ii] for ii in range(n_eff_bins)])

for ii, xx in enumerate(eff_KE_hist):
    eff_KE_hist[ii] = math.sqrt((xx**2+938.**2)) - 938.

print("KE, eff")
for ii, xx in enumerate(eff_KE_hist):
    print(xx, eff_hist_wasgood[ii])


plt.figure()
ax = plt.subplot(111)
ax.plot(eff_KE_hist,eff_hist)
ax.set_xlim([0, (math.sqrt(200**2+938**2)-938)])
ax.set_ylim([0, 1.01])
ax.set_xlabel("true Momentum (MeV/c)")
ax.set_ylabel("efficiency")
plt.savefig("./efficiency.png")

plt.figure()
ax = plt.subplot(111)
ax.plot(eff_KE_hist,eff_hist_wasgood)
ax.set_xlim([0, (math.sqrt(170**2+938**2)-938)])
ax.set_ylim([0, 1.01])
ax.set_xlabel("true KE (MeV)")
ax.set_ylabel("efficiency")
plt.savefig("./efficiency_wasgood.png")

plt.figure()
ax = plt.subplot(111)
ax.hist(total_KE_residual_hist, bins=50)
ax.set_xlabel("total KE_measured - total KE_true (MeV)")
mu = total_KE_residual_hist.mean()
sigma = total_KE_residual_hist.std()
textstr = '\n'.join((
    r'$\mu=%.2f$' % (mu, ),
    r'$\sigma=%.3f$' % (sigma, )))
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# place a text box in upper left in axes coords
ax.text(0.75, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
plt.savefig("./total_KE_residual.png")

plt.figure()
ax = plt.subplot(111)
ax.hist(true_KE_total_hist, bins=50)
plt.savefig("true_KE_total_dist.png")

plt.figure()
ax = plt.subplot(111)
ax.hist(pred_KE_total_hist, bins=50)
plt.savefig("pred_KE_total_dist.png")

plt.figure()
ax = plt.subplot(111)
ax.hist(true_KE_total_hist, bins=50, alpha=0.5, label='true')
ax.hist(pred_KE_total_hist, bins=50, alpha=0.5, label='reco')
ax.set_xlabel('total KE')
ax.legend(loc='upper right')
plt.savefig("overlay_KE_total_dist.png")


plt.figure()
ax = plt.subplot(111)
ax.hist2d(true_KE_total_hist, pred_KE_total_hist, bins=100)
ax.set_xlabel("true total KE")
ax.set_ylabel("measured total KE")
plt.savefig("./pred_true_2D_KE_total.png")

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
ax.hist(res_KE_hist, bins=100)
ax.set_title("Kinetic Energy Residual for 3-15 MeV Protons")
ax.set_xlabel("KE_measured - KE_true (MeV)")
#KE range is 2.6-21MeV (70-200 MeV/c momentum)

mu = res_KE_hist.mean()
sigma = res_KE_hist.std()
textstr = '\n'.join((
    r'$\mu=%.2f$' % (mu, ),
    r'$\sigma=%.3f$' % (sigma, )))

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
ax.text(0.75, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

plt.savefig("./residuals_hist_KE.png")

plt.figure()
ax = plt.subplot(111)
ax.hist2d(pred_KE_hist, res_KE_hist, bins=50)
ax.set_ylim([-5,5])
ax.set_xlim([3,15])
ax.set_xlabel("true KE (MeV)")
ax.set_ylabel("KE_predicted - KE_true (MeV)")
plt.savefig("./residuals_2D_KE_hist.png")

plt.figure()
ax = plt.subplot(111)
ax.hist2d(true_KE_hist, pred_KE_hist, bins=100)
ax.set_ylim([3,15])
ax.set_xlim([3,15])
ax.set_ylabel("measured KE (MeV)")
ax.set_xlabel("true KE (MeV)")
plt.savefig("./pred_true_2D_KE_hist.png")


plt.figure()
ax = plt.subplot(111)
ax.hist2d(res_mom_hist, res_hist, bins=100)
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

