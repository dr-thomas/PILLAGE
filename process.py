import csv
from RANSAC import process_ransac
import numpy as np
import pickle
from sklearn import preprocessing

class event_momentums():
    def __init__(self):
        self.pred_moms = []
        self.true_moms = []

def process_files(in_file_list, batch):
    momentum_data_out = []
    mlp_regressor = pickle.load(open('./model_saves/protons_neural_net.sav', 'rb'))
    std_scaler = pickle.load(open('./model_saves/protons_neural_net_std_scaler.sav', 'rb'))

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
                    elif ifeature <= n_particles:
                        evt_moms.true_moms.append(float(feature)*1000.)
                    else:
                        hit_data.append(float(feature))

                clusters = process_ransac.cluster(hit_data)

                for cluster in clusters:
                    data_X = np.ndarray((1,len(cluster)))
                    for ii, cc in enumerate(cluster):
                        data_X[0][ii] = float(cc)
                    data_X_scaled = std_scaler.transform(data_X)
                    evt_moms.pred_moms.append(mlp_regressor.predict(data_X_scaled))
                momentum_data_out.append(evt_moms)

    save_str = 'event_momentum_data' + str(batch) + '.sav'
    pickle.dump(momentum_data_out, open(save_str, 'wb'))

