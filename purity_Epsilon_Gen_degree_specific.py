import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import os

def drop_zeros(a_list):
    return [i for i in a_list if i>0]

exp_name= input("Experiment Name: ")
dataset = input("Dataset: ")
radius = float(input("Radius: "))
bin_count = int(input("Number of Bins: "))

frame_out_path= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp_name+"/Epsilon_Results/Epsilon_Files/Epsilon_Single_Degree/"
frame_out_path_2= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp_name+"/Epsilon_Results/Epsilon_Plots/Epsilon_Single_Degree/"
frame_out_path_3= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp_name+"/Epsilon_Results/Epsilon_Plots/Epsilon_Single_Degree_EPS/"


dist_mat_path =  "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp_name+"/"+ dataset+"_Dist_Form.txt"




try:
    os.makedirs(frame_out_path)
except OSError:
    print ("Creation of the directory %s failed" % frame_out_path)
else:
    print ("Successfully created the directory %s" % frame_out_path)

try:
    os.makedirs(frame_out_path_2)
except OSError:
    print ("Creation of the directory %s failed" % frame_out_path_2)
else:
    print ("Successfully created the directory %s" % frame_out_path_2)

try:
    os.makedirs(frame_out_path_3)
except OSError:
    print ("Creation of the directory %s failed" % frame_out_path_3)
else:
    print ("Successfully created the directory %s" % frame_out_path_3)


dist_mat = pd.read_csv(dist_mat_path,sep = "\t",header= None)
print("Reading Distance_Matrix")
dist_mat.columns= ["Out","In", "Dist"]

index_list=list(set(dist_mat["Out"].values.tolist()))

index_dict = dict(zip(index_list,list(range(len(index_list)))))


neigh_holder = [0]*len(index_list)

pic_title= "_Density"



G=nx.Graph()
G.add_nodes_from(index_list)

sub_dist_mat= dist_mat.loc[dist_mat["Dist"]<= radius,["Out","In"]]
sub_dist_mat= sub_dist_mat.loc[dist_mat["Out"]!=dist_mat["In"],:]
new_red= sub_dist_mat.to_records(index=False)
t_list= list(new_red)
G.add_edges_from(t_list)


print("Saving Neighborhoods")

for n in nx.classes.function.nodes(G):
    if len(list(G.neighbors(n)))!=0:
        fork_in= index_dict[n]
        degree_val= len(list(G.neighbors(n)))
        neigh_holder[fork_in]= degree_val

G.remove_edges_from(G.edges())

count_frame= pd.DataFrame({radius:neigh_holder} ,index= index_list)

count_frame.to_csv(frame_out_path+dataset+"_"+str(radius)+pic_title+".csv")

mi_x= 10
ma_x=0
ma_y=0
mi_y=10


num_nodes= len(neigh_holder)
degree_list,freq=np.unique(neigh_holder,return_counts= True)
freq= freq/num_nodes
if ((freq.shape[0]==0) or (freq.shape[0]==1 and degree_list[0]==0)):
    print("Unable to print degree distribution as no edges were drawn")
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
    max_x= np.log10(max(coll.keys()))
    max_y= np.log10(max(coll.values()))
    y_inter = max(coll.values())*10
    max_base = max([max_x,max_y])
    min_x = np.log10(min(drop_zeros(coll.keys())))
    bins = np.logspace(min_x,max_base,num=bin_count)

    bin_means_y = (np.histogram(list(coll.keys()),bins,weights=list(coll.values()))[0] / np.histogram(list(coll.keys()),bins)[0])
    bin_means_x = (np.histogram(list(coll.keys()),bins,weights=list(coll.keys()))[0] / np.histogram(list(coll.keys()),bins)[0])

    fig, axs = plt.subplots(nrows=1, ncols=1)
    fig.suptitle(dataset+" Degree Distribution Epsilon:"+ str(radius))
    axs.set_title('All Cell Types')
    axs.set_yscale('log')
    axs.set_xscale('log')
    axs.set_ylim((mi_y,ma_y))
    axs.set_xlim((mi_x,ma_x))
    #axs.set_aspect('equal')
    ref_line=[y_inter_f/i for i in ref_bins]
    axs.plot(ref_bins,ref_line, '0.8', label = "y=-x" )
    axs.plot(bin_means_x,bin_means_y,'ro', label = "Distribution")

    print(ref_line)


    axs.set_xlabel('Node degree')
    axs.set_ylabel('P(deg)')
    #axs.legend()
        #h=ax.hist2d(new_degree,new_homog,norm=mpl.colors.LogNorm(),bins =50)
        #fig.colorbar(h[3], ax= ax)
    fig.tight_layout()
    plt.savefig(frame_out_path_2+dataset+"_"+str(radius)+"_degree_dist_adjusted_binned.png")
    plt.savefig(frame_out_path_3+dataset+"_"+str(radius)+"_degree_dist_adjusted_binned.eps")

    fig.clear()
