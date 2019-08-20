import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

y_test = np.load('./results/pions-0-200/y_test.npy')
y_pred = np.load('./results/pions-0-200/y_pred.npy')
residuals = np.load('./results/pions-0-200/residuals.npy')

residuals_draw = np.array([])
y_test_draw = np.array([])
for ii in range(len(residuals)):
    if y_test[ii] < 0.0:
        continue
    residuals_draw = np.append(residuals_draw, residuals[ii])
    y_test_draw = np.append(y_test_draw, y_test[ii])


ax = plt.subplot(111)
ax.hist(residuals_draw, bins=100, range=(-75, 75))
ax.set_xlabel('residual (MeV)')
ax.set_title('test set momentum residual')

mu = residuals_draw.mean()
sigma = residuals_draw.std()
textstr = '\n'.join((
    r'$\mu=%.2f$' % (mu, ),
    r'$\sigma=%.3f$' % (sigma, )))

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
ax.text(0.75, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

plt.savefig("HPgTPC_NN_Residuals.png")

plt.figure()
ax3 = plt.subplot(111)
ax3.hist2d(y_test_draw, residuals_draw, bins=30, range=[[0,200], [-90,90]])

ax3.set_xlabel('true momentum (MeV)')
ax3.set_ylabel('residual (MeV)')
ax3.set_title('test set 2D residual')


plt.savefig("HPgTPC_NN_2D_Residuals.png")

