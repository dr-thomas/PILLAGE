import numpy as np
import matplotlib.pyplot as plt

y_pred = np.load('./photons/y_pred.npy')
y_test = np.load('./photons/y_test.npy')
y_E_test = np.load('./photons/y_E_test.npy')

PID_cut = 0.1
n_E_bins = 5
E_bins = [ii*1./n_E_bins for ii in range(n_E_bins+1)]
E_bins[n_E_bins] = 1e10

acc_hist_photon = [0. for ii in range(n_E_bins)]
E_hist_photon = [0. for ii in range(n_E_bins)]

for iEvt in range(len(y_pred)):
    if y_E_test[iEvt] < 0.:
        continue
    temp_e_bin = -1
    for ii, xx in enumerate(E_bins):
        if y_E_test[iEvt] < xx:
            temp_e_bin = ii
            break
    temp_e_bin -= 1
    if temp_e_bin == -1:
        continue
    if y_test[iEvt] > 0.5:
        E_hist_photon[temp_e_bin] += 1.
        if y_pred[iEvt] > PID_cut:
            acc_hist_photon[temp_e_bin] += 1.

for ii in range(n_E_bins):
    if E_hist_photon[ii] > 0:
        acc_hist_photon[ii] *= 1.0/E_hist_photon[ii]
    else:
        acc_hist_photon[ii] = 0.

E_bins[n_E_bins] = 1.
E_bins_draw = [(E_bins[ii]+E_bins[ii+1])/2 for ii in range(n_E_bins)]
plt.figure()
plt.ylim([0.9,1.])
plt.ylabel('accuracy')
plt.xlabel('KE (GeV)')
plt.title('Photon PID Accuracy')
plt.plot(E_bins_draw, acc_hist_photon, linestyle='-')
#plt.scatter(E_bins_draw, acc_hist_photon)
plt.savefig("photon_accuracy.png")

n_E_bins = 1

p_E_hist = np.ndarray([])
for yy in y_E_test:
    p_E_hist = np.append(p_E_hist, yy)
plt.figure()
plt.hist(p_E_hist, bins=50)
plt.savefig('test_set_p_Es.png')
bins = np.linspace(-0.5, 2.0, 50)

eMax = -1.
for yy in y_E_test:
    if yy > eMax:
        eMax = yy

n_E_bins = 1

eMax = 1.

p_hist = [np.ndarray([]) for ii in range(n_E_bins)]
mu_hist = np.ndarray([])
p_Es = [ii*(eMax/(n_E_bins)) for ii in range(n_E_bins+1)]
for ii in range(len(y_pred)):
    if abs(y_pred[ii])>1e6:
        continue
    if abs(y_E_test[ii])<1e6:
        p_E_hist = np.append(p_E_hist, y_E_test[ii])
    if y_test[ii] == 0:
        E_ind = -1
        for jj, yy in enumerate(p_Es):
            if y_E_test[ii] < yy:
                E_ind = jj
                break
        E_ind += -1
        if E_ind > (n_E_bins-1):
            E_ind = (n_E_bins-1)
        if E_ind < 0:
            E_ind = 0
        p_hist[E_ind] = np.append(p_hist[E_ind], y_pred[ii])
    else:
        if y_E_test[ii] < 1.5:
            mu_hist = np.append(mu_hist, y_pred[ii])



plt.figure()
plt.hist(mu_hist, bins, alpha=0.5, label='photon')
plt.xlabel('PID score')
p_labels = ['e: %.1f-%.1fGeV/c'%(p_Es[ii],p_Es[ii+1]) for ii in range(n_E_bins)]
if n_E_bins > 1:
    plt.hist(p_hist, bins, stacked=True, alpha=0.5, label=p_labels)
else:
    plt.hist(p_hist, bins, stacked=True, alpha=0.5, label='e')
plt.legend(loc='upper right')
plt.savefig('particle_score.png')


