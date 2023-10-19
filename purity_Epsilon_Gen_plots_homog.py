import pandas as pd
import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt






exp = input("Experiment Name: ")
group= input("Group Name: ")
dir_name = input("Directory Name with matrices: ")
bin_count= int(input("Number of Bins for Log_Binnng: "))
neigh_cutoff= int(input("Minimum number of Neighbors to Consider: "))
source_dir =  "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp+"/Epsilon_Results/Epsilon_Files/Epsilon_Degree_Homog/"+dir_name

out_dir= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp+"/Epsilon_Results/Epsilon_Plots/Epsilon_Homog_Dist/"+dir_name+"_"+str(neigh_cutoff)
out_dir_2= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp+"/Epsilon_Results/Epsilon_Plots/Epsilon_Homog_Dist_EPS/"+dir_name+"_"+str(neigh_cutoff)

try:
    os.makedirs(out_dir)
except OSError:
    print ("Creation of the directory %s failed" % out_dir)
else:
    print ("Successfully created the directory %s" % out_dir)

try:
    os.makedirs(out_dir_2)
except OSError:
    print ("Creation of the directory %s failed" % out_dir)
else:
    print ("Successfully created the directory %s" % out_dir)


data_source = source_dir+"/Neighborhoods.csv"
data_2_path = source_dir+"/Homogeneity.csv"
data = pd.read_csv(data_source, index_col = 0)
data_2 = pd.read_csv(data_2_path,index_col= 0)
radlist= data.keys().values.tolist()
print(radlist)

for r in radlist[1:]:
    label = group+"_"+r+"_Homogeneity"
    i= float(r)
    num_neigh = data.loc[:,r].values
    homog_neigh =data_2.loc[:,r].values
    non_zero= num_neigh>=neigh_cutoff#np.nonzero(num_neigh)
    homog_neigh=homog_neigh[non_zero]
    num_neigh= num_neigh[non_zero]
    num_nodes= num_neigh.shape[0]
    if (num_nodes==0):
        print("skipped")
    else:


        fig, axs = plt.subplots(nrows=1, ncols=1)
        fig.suptitle(dir_name+" Degree Distribution Epsilon:"+ r)
        axs.set_title('All Cell Types')
        axs.set_xlabel('Node degree')
        axs.set_ylabel('%Homogeneity')

        h=axs.hist2d(num_neigh,homog_neigh*100,norm=mpl.colors.LogNorm(),bins =bin_count)
        fig.colorbar(h[3], ax= axs)

        plt.savefig(out_dir+"/"+label+"_homog_degree_hist.png")
        plt.savefig(out_dir_2+"/"+label+"_homog_degree_hist.eps")

        fig.clear()











    ### Write the result to .csv



### if you want to read a loom file:
# adata = sc.read_loom(filename)

# Do a nearest neighbor search:
