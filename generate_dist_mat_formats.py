import pandas as pd
import numpy as np

from sklearn.metrics import pairwise_distances


import os


group= input("Experiment: ")
dataset = input("Dataset: ")

frame_in_path = "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+group+"/"+dataset+".csv"
frame_out_path = "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+group+"/"+dataset+"_Dist_Form.txt"
folder_maker = "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+group+"/"

try:
    os.makedirs(folder_maker)
except OSError:
    print ("Creation of the directory %s failed" % folder_maker)
else:
    print ("Successfully created the directory %s" % folder_maker)

data= pd.read_csv(frame_in_path, index_col = 0)

index_list= data.index.values.tolist()
adj_data_matrix = data.iloc[:,1:].values

dist_mat = pairwise_distances(adj_data_matrix)
min_dist=(np.amin(dist_mat[np.nonzero(dist_mat)]))
max_dist= (np.amax(dist_mat[np.nonzero(dist_mat)]))


ind_list = []
ind2_list = []
dist_list = []
for i in range(0, dist_mat.shape[0]):
    for j in range(i+1,dist_mat.shape[0]):
        ind_list.append(index_list[i])
        ind2_list.append(index_list[j])
        dist_list.append(dist_mat[i,j])

        ind_list.append(index_list[j])
        ind2_list.append(index_list[i])
        dist_list.append(dist_mat[i,j])
last_frame= pd.DataFrame({"Name_1":ind_list, "Name_2":ind2_list, "Distance":dist_list})
last_frame.to_csv(frame_out_path,header = False, index= False, sep = "\t")
