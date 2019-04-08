import os
import csv
from RANSAC import process_ransac

tagged_path = './data/multiple_protons_0-200/csv/momentum-tagged/'
for ifile, file_name in enumerate(os.listdir(tagged_path)):
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
            if len(clusters) > 2:
                print("hit data:")
                print(hit_data)
                print("clusters:")
                print(clusters)
                exit()

