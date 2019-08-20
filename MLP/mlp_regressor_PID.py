import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from scipy import stats
import pickle

#X_data_in = np.load('./data/PID/X_train_Species_3.npy')
#y_data_in = np.load('./data/PID/y_train_Species_3.npy')
X_data_in = np.load('./full/all/X_train.npy')
y_data_in = np.load('./full/all/y_train.npy')

process_fraction = 1.
process_n = int(process_fraction*len(X_data_in))
X_data = np.ndarray((process_n, len(X_data_in[0])))
y_data = np.ndarray((process_n, len(y_data_in[0])))
for ii in range(process_n):
    for jj, yy in enumerate(X_data_in[ii]):
        X_data[ii][jj] = yy
    for jj, yy in enumerate(y_data_in[ii]):
        y_data[ii][jj] = yy

X_data_scaled = preprocessing.scale(X_data)
std_scaler = preprocessing.StandardScaler()
std_scaler.fit(X_data)
pickle.dump(std_scaler, open('PID_ss_std_scaler.sav', 'wb'))
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
nclasses = len(y_data[0])

X_train = np.ndarray((ntrain,nfeatures))
y_train = np.ndarray((ntrain,nclasses))

X_test = np.ndarray((ntest,nfeatures))
y_test = np.ndarray((ntest,nclasses))

itrain = 0
itest = 0
for ii, xx in enumerate(X_data_scaled):
    if ii%10 == 0:
        for jj, yy in enumerate(xx):
            X_test[itest][jj] = yy
        for jj, yy in enumerate(y_data[ii]):
            y_test[itest][jj] = yy
        itest += 1
    else:
        for jj, yy in enumerate(xx):
            X_train[itrain][jj] = yy
        for jj, yy in enumerate(y_data[ii]):
            y_train[itrain][jj] = yy
        itrain += 1

#reg = MLPClassifier(hidden_layer_sizes=(int(nfeatures/2),int(nfeatures/4)), 
#reg = MLPRegressor(hidden_layer_sizes=(int(nfeatures/2)), 
reg = MLPRegressor(hidden_layer_sizes=(400,200), 
                  activation='relu', solver='adam', alpha=1e-4, verbose=True, tol=1e-6)#lbfgs, adam, sgd for solver

'''

reg = MLPRegressor(hidden_layer_sizes=(int(nfeatures), int(nfeatures)), 
                  activation='logistic', solver='adam', alpha=1e-4, verbose=True, tol=1e-5)#lbfgs, adam, sgd for solver
                   - this got 65% for each p and pi+ 
'''

reg.fit(X_train, y_train)

pickle.dump(reg, open('PID_ss.sav', 'wb'))

y_pred = reg.predict(X_test)

np.save('y_pred.npy', y_pred)
np.save('y_test.npy', y_test)
