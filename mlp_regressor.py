import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn import preprocessing
from scipy import stats
import pickle

X_data = np.load('./data/protons-0-300/X_train.npy')
y_data = np.load('./data/protons-0-300/y_train.npy')

for ii in range(len(y_data)):
    y_data[ii] = y_data[ii]*1000.

X_data_scaled = preprocessing.scale(X_data)
std_scaler = preprocessing.StandardScaler()
std_scaler.fit(X_data)
pickle.dump(std_scaler, open('protons_300_nn_full_ss_std_scaler.sav', 'wb'))
X_data_scaled = std_scaler.transform(X_data)
#X_data_scaled = X_data

ntrain = 0
ntest = 0
for ii, xx in enumerate(X_data):
    if ii%10 == 0:
        ntest += 1
    else:
        ntrain += 1

nfeatures = len(X_data_scaled[0])

X_train = np.ndarray((ntrain,nfeatures))
y_train = np.ndarray(ntrain)

X_test = np.ndarray((ntest,nfeatures))
y_test = np.ndarray(ntest)

itrain = 0
itest = 0
for ii, xx in enumerate(X_data_scaled):
    if ii%10 == 0:
        for jj, yy in enumerate(xx):
            X_test[itest][jj] = yy
        y_test[itest] = y_data[ii]
        itest += 1
    else:
        for jj, yy in enumerate(xx):
            X_train[itrain][jj] = yy
        y_train[itrain] = y_data[ii]
        itrain += 1

#reg = MLPRegressor(hidden_layer_sizes=(int(nfeatures/2),int(nfeatures/4),int(nfeatures/8)), 
reg = MLPRegressor(hidden_layer_sizes=(100), 
                  activation='logistic', solver='adam', alpha=1e-3, verbose=True, tol=5e-6)#lbfgs, adam, sgd for solver
"""
reg = MLPRegressor(hidden_layer_sizes=(int(nfeatures/2)), 
                  activation='logistic', solver='adam', alpha=1e-4, verbose=True, tol=1e-4)#lbfgs, adam, sgd for solver
                  -> this gets mu=0 and sigma=0.04 for residuals!!  roughly 20% spread in resoltuion at less than 200MeV!
                  -> adding second hidden layer gets sigma down to 0.33, a third brings it to 0.29
                  -> increasing alpa to 1e-1 durastically increases number of iterations and widens residual 
                     distribution to almost flat.  seems minimizer is struggling
                       -> critial alpha seems to be around 1e-2, -3 has little effect, -2 starts to be noticable

~700 files data:
reg = MLPRegressor(hidden_layer_sizes=(int(nfeatures/2),int(nfeatures/4),int(nfeatures/8)), 
                  activation='logistic', solver='adam', alpha=1e-3, verbose=True, tol=1e-4)#lbfgs, adam, sgd for solver
                  -> this gets mu=0 and sigma=0.22!
Full data:
reg = MLPRegressor(hidden_layer_sizes=(int(nfeatures/2),int(nfeatures/4),int(nfeatures/8)), 
                  activation='logistic', solver='adam', alpha=1e-3, verbose=True, tol=5e-6)#lbfgs, adam, sgd for solver
                  -> when scaled to MeV, this give mu=0.03 and sigma=13.6!  it also displays less of the intersting 
                     behavior for very low momentum.  the sigma is relatively constant all the way down to 10-20 MeV!

"""

reg.fit(X_train, y_train)

pickle.dump(reg, open('protons_300_nn_full_ss.sav', 'wb'))

y_pred = reg.predict(X_test)

residuals = (y_pred - y_test)

np.save('residuals.npy', residuals)
np.save('y_pred.npy', y_pred)
np.save('y_test.npy', y_test)

residuals_draw = np.array([])
y_test_draw = np.array([])
for ii in range(len(residuals)):
    if y_test[ii] < 0.0:
        continue
    residuals_draw = np.append(residuals_draw, residuals[ii])
    y_test_draw = np.append(y_test_draw, y_test[ii])


ax = plt.subplot(111)
ax.hist(residuals_draw, bins=100)

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
ax3.hist2d(y_test_draw, residuals_draw, bins=50)
plt.savefig("HPgTPC_NN_2D_Residuals.png")
