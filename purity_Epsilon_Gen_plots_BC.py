import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

#Helper function to help with Log-Binninng
def drop_zeros(a_list):
    return [i for i in a_list if i>0]

exp = input("Experiment Name: ")
group= input("Group Name: ")
dir_name = input("Directory Name with matrices: ")
neigh_cutoff= int(input("Minimum number of neighbors to consider: "))
#May need to be changed depending on user local paths
source_dir =  "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp+"/Epsilon_Results/Epsilon_Files/Epsilon_Degree_BC/"+dir_name
out_dir= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp+"/Epsilon_Results/Epsilon_Plots/Epsilon_Degree_BC/"+dir_name
out_dir_2= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp+"/Epsilon_Results/Epsilon_Plots/Epsilon_Degree_BC_EPS/"+dir_name

#out_dir= "/media/timothyhamilton/data1/Tim_Hamilton/Zheng_DDG/"+group+"/Results/Epsilon_Plots"
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
data_source_2= source_dir+"/Centrality.csv"
data = pd.read_csv(data_source, index_col = 0)
data_2= pd.read_csv(data_source_2, index_col = 0)
radlist= data.keys().values.tolist()
print(radlist)
mi_x= 0
ma_x=0
ma_y=0
mi_y=0
#y_i =0
for r in radlist:
    num_neigh = data.loc[:,r].values
    bc_list = data_2.loc[:,r].values
    non_zero= num_neigh>=neigh_cutoff
    bc_list=bc_list[non_zero]
    num_neigh= num_neigh[non_zero]

    if (num_neigh.shape[0]==0):
        print("skipped")
    else:
        min_x=np.min(num_neigh)
        max_x =np.max(num_neigh)
        min_y= np.min(bc_list)
        max_y= np.max(bc_list)
        if mi_x > min_x:
            mi_x = min_x
        if ma_x <= max_x:
            ma_x = max_x
        if mi_y >= min_y:
            mi_y= min_y
        if ma_y <= max_y:
            ma_y= max_y






for r in radlist:
    label = group+"_"+r+"_No"
    num_neigh = data.loc[:,r].values
    bc_list = data_2.loc[:,r].values
    non_zero= num_neigh>=neigh_cutoff
    bc_list=bc_list[non_zero]
    num_neigh= num_neigh[non_zero]

    if (num_neigh.shape[0]==0):
        print("skipped")
    else:
        fig, axs = plt.subplots(nrows=1, ncols=1)
        fig.suptitle(dir_name+" Degree Distribution Epsilon: "+ r)
        axs.set_title('Betweeness Centrality vs Epsilon')
        axs.set_xlabel('Node degree')
        axs.set_ylabel('Betweeness Centrality')
        #axs.set_yscale('log')
        axs.set_xscale('log')
        axs.set_xlim((mi_x,ma_x))
        axs.set_ylim((mi_y,ma_y))
        #axs.set_aspect('equal')
        axs.scatter(num_neigh,bc_list, alpha=0.3)
        #h=axs.hist2d(num_neigh,homog_neigh,norm=mpl.colors.LogNorm(),bins =bin_count)
        #fig.colorbar(h[3], ax= axs)

        #axs.legend()
            #h=ax.hist2d(new_degree,new_homog,norm=mpl.colors.LogNorm(),bins =50)
            #fig.colorbar(h[3], ax= ax)
        fig.tight_layout()
        plt.savefig(out_dir+"/"+label+"_bc_scatter.png")
        plt.savefig(out_dir_2+"/"+label+"_bc_scatter.eps")
        fig.clear()













    ### Write the result to .csv



### if you want to read a loom file:
# adata = sc.read_loom(filename)

# Do a nearest neighbor search:
