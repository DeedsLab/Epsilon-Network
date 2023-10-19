import pandas as pd
import numpy as np
import numpy.random as random
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import scanpy as sc
import anndata as ad
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import DistanceMetric
from scipy.stats import linregress


import smtplib
import os
import sys



# read the data from 10x .mtx:
def neighbors(data, k=20):
    # for a given dataset, finds the k nearest neighbors for each point
    nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='ball_tree').fit(data)
    distances, indices = nbrs.kneighbors(data)
    return indices[:,1:]
def radius_neighbors(data,rad):
    nbrs =  NearestNeighbors( algorithm='ball_tree').fit(data)
    dist, indices = nbrs.radius_neighbors(radius= rad, sort_results= True)
    return indices

def jaccard(A,B):
    # for two sets A and B, finds the Jaccard distance J between A and B
    A = set(A)
    B = set(B)
    union = list(A|B)
    intersection = list(A & B)
    J = ((len(union) - len(intersection))/(len(union)))
    return(J)
def equalizer(A):
    for i in range(A.shape[1]):
        if np.mean(A[:,i])>=1.0:
            A[:,i]/=np.mean(A[:,i])
    return A
def drop_zeros(a_list):
    return [i for i in a_list if i>0]

exp = input("Experiment Name: ")
#group= input("Group Name: ")
dir_name = input("Directory Name with matrices: ")

#bin_count= int(input("Number of Bins for Log_Binnng: "))
source_dir =  "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp+"/"+dir_name
#source_dir_2= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp+"/Epsilon_Results/Epsilon_Files/"+dir_name
out_dir= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton//Epsilon_Borders/"+exp+"/Epsilon_Results/Epsilon_Plots/Giant_Component_Results/"


#out_dir= "/media/timothyhamilton/data1/Tim_Hamilton/Zheng_DDG/"+group+"/Results/Epsilon_Plots"
try:
    os.makedirs(out_dir)
except OSError:
    print ("Creation of the directory %s failed" % out_dir)
else:
    print ("Successfully created the directory %s" % out_dir)


data_source = source_dir+".txt"
data= pd.read_csv(data_source, index_col=0, sep= "\t",header= None)
data.columns= ["Size_of_GCC"]
rad_list= data.index.values.tolist()
size_list = data.loc[:,"Size_of_GCC"].values.tolist()






fig, ax1 = plt.subplots(nrows=1, ncols=1)
fig.suptitle(dir_name)

p1, = ax1.plot(rad_list,size_list,"r-", label = "Size_of_GCC")

lines = [p1]
ax1.set_xlabel("Epsilon")
ax1.set_ylabel("Size_of_GCC")

ax1.set_title("Giant_Component_Results")



formatting = dict(size=4, width=1.5)

ax1.tick_params(axis='y', **formatting)

ax1.tick_params(axis='x', **formatting)
plt.tight_layout()
plt.savefig(out_dir+"/"+dir_name+"_results.png")
plt.savefig(out_dir+"/"+dir_name+"_results.eps")

fig.clear()












    ### Write the result to .csv



### if you want to read a loom file:
# adata = sc.read_loom(filename)

# Do a nearest neighbor search:
