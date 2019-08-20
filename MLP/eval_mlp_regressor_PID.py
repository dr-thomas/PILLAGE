import numpy as np
import matplotlib.pyplot as plt

#y_pred = np.load('./results/PID/y_pred_full.npy')
#y_test = np.load('./results/PID/y_test_full.npy')
y_pred = np.load('./y_pred.npy')
y_test = np.load('./y_test.npy')

if len(y_pred) != len(y_test):
    print("mismatched lengths, exiting")
    exit()

nclasses = len(y_pred[0])

acc_mat = [[0. for ii in range(nclasses)] for ii in range(nclasses)]
true_vec = [0. for ii in range(nclasses)]

for iEvt in range(len(y_pred)):
    true_class = -1
    for ii, xx in enumerate(y_test[iEvt]):
        if xx:
            true_class = ii
            break

    pred_class = -1
    max_prob = -1e10
    for ii, xx in enumerate(y_pred[iEvt]):
        if xx > max_prob:
            max_prob = xx
            pred_class = ii
    if pred_class < 0:
        continue

    true_vec[true_class] += 1.
    acc_mat[true_class][pred_class] += 1.

for ii, xx in enumerate(acc_mat):
    for jj, yy in enumerate(xx):
        acc_mat[ii][jj] *= 1./true_vec[ii]

#TODO: labels  ->axes work how you think they should, x is first index, y is second 
if nclasses == 7:
    labels = ['p', 'pi-', 'pi+', 'mu-', 'mu+', 'e-', 'e+']
elif nclasses == 2:
    #labels = ['p, e', 'pi, mu']
    labels = ['p', 'pi+']
elif nclasses == 4:
    labels = ['p', 'pi', 'mu', 'e']
elif nclasses == 3:
    labels = ['p', 'pi,mu', 'e']
else:
    labels = []

plt.figure()
ax = plt.subplot(111)
im = ax.matshow(acc_mat)
for ii, xx in enumerate(acc_mat):
    for jj, yy in enumerate(xx):
        text = ax.text(jj, ii, "%0.2f"%(acc_mat[ii][jj]), ha="center", va="center", color="w")
im.set_clim(0,1.)
cbar = ax.figure.colorbar(im, ax=ax)

ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))
ax.set_xticklabels(labels)
ax.set_yticklabels(labels)

ax.set_xlabel('measured PID')
ax.set_ylabel('true PID')
ax.xaxis.set_label_position('top')

plt.tight_layout()
plt.savefig("./PID_acc_mat.png")
