import pickle
import matplotlib.pyplot as plt
import numpy as np

class event_momentums():
    def __init__(self):
        self.pred_moms = []
        self.true_moms = []

momentum_data = pickle.load(open('./event_momentum_data.sav', 'rb'))

res_hist = np.array([])
for evt in momentum_data:
    for pred_mom in evt.pred_moms:
        min_residual = 555e10
        for true_mom in evt.true_moms:
            if abs(pred_mom-true_mom) < min_residual:
                min_residual = pred_mom-true_mom
        if min_residual < 1e5:
            res_hist = np.append(res_hist, min_residual)

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


