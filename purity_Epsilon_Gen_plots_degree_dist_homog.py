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
bin_count= int(input("Number of Bins for Log_Binnng: "))
#May need to be changed depending on user local paths
source_dir =  "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp+"/Epsilon_Results/Epsilon_Files/Epsilon_Degree_Homog/"+dir_name
out_dir= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp+"/Epsilon_Results/Epsilon_Plots/Epsilon_Degree_Homog/"+dir_name
out_dir_2= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp+"/Epsilon_Results/Epsilon_Plots/Epsilon_Degree_Homog_EPS/"+dir_name

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
data = pd.read_csv(data_source, index_col = 0)
radlist= data.keys().values.tolist()
print(radlist)
mi_x= 10
ma_x=0
ma_y=0
mi_y=10
#y_i =0
for r in radlist[1:]:
    num_neigh = data.loc[:,r].values
    num_nodes= num_neigh.shape[0]
    degree_list,freq=np.unique(num_neigh,return_counts= True)
    freq= freq/num_nodes
    if ((freq.shape[0]==0) or (freq.shape[0]==1 and degree_list[0]==0)):
        print("skipped first part")
    else:
        coll= {degree_list[i]:freq[i] for i in range(degree_list.shape[0])}
        min_x = min(drop_zeros(coll.keys()))
        max_x= max(coll.keys())
        min_y= min(drop_zeros(coll.values()))
        max_y =max(coll.values())
        if mi_x > min_x:
            mi_x = min_x
        if ma_x <= max_x:
            ma_x = max_x
        if mi_y >= min_y:
            mi_y= min_y
        if ma_y <= max_y:
            ma_y= max_y
ma_base= max([ma_x,ma_y])
ref_bins= np.logspace(np.log10(mi_x),np.log10(ma_base),num=bin_count)
y_inter_f= ma_y





for r in radlist[1:]:
    label = group+"_"+r+"_No"
    i= float(r)
    num_neigh = data.loc[:,r].values
    num_nodes= num_neigh.shape[0]
    degree_list,freq=np.unique(num_neigh,return_counts= True)
    freq= freq/num_nodes
    if ((freq.shape[0]==0) or (freq.shape[0]==1 and degree_list[0]==0)):
        print("skipped")
    else:
        coll= {degree_list[i]:freq[i] for i in range(degree_list.shape[0])}
        max_x= np.log10(max(coll.keys()))
        max_y= np.log10(max(coll.values()))
        y_inter = max(coll.values())*10
        max_base = max([max_x,max_y])
        min_x = np.log10(min(drop_zeros(coll.keys())))
        bins = np.logspace(min_x,max_base,num=bin_count)

        bin_means_y = (np.histogram(list(coll.keys()),bins,weights=list(coll.values()))[0] / np.histogram(list(coll.keys()),bins)[0])
        bin_means_x = (np.histogram(list(coll.keys()),bins,weights=list(coll.keys()))[0] / np.histogram(list(coll.keys()),bins)[0])

        fig, axs = plt.subplots(nrows=1, ncols=1)
        fig.suptitle(dir_name+" Degree Distribution Epsilon:"+ r)
        axs.set_title('All Cell Types')
        axs.set_yscale('log')
        axs.set_xscale('log')
        axs.set_ylim((mi_y,ma_y))
        axs.set_xlim((mi_x,ma_x))
        #axs.set_aspect('equal')
        ref_line=[y_inter_f/i for i in ref_bins]
        axs.plot(ref_bins,ref_line, 'r', label = "y=-x" )
        axs.plot(bin_means_x,bin_means_y,'o', label = "Distribution")

        print(ref_line)


        axs.set_xlabel('Node degree')
        axs.set_ylabel('P(deg)')
        #axs.legend()
            #h=ax.hist2d(new_degree,new_homog,norm=mpl.colors.LogNorm(),bins =50)
            #fig.colorbar(h[3], ax= ax)
        fig.tight_layout()
        plt.savefig(out_dir+"/"+label+"_degree_dist_adjusted_binned.png")
        plt.savefig(out_dir_2+"/"+label+"_degree_dist_adjusted_binned.eps")

        fig.clear()












    ### Write the result to .csv



### if you want to read a loom file:
# adata = sc.read_loom(filename)

# Do a nearest neighbor search:
