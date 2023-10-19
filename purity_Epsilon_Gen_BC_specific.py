import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import os
from networkx.algorithms.centrality import betweenness_centrality

def drop_zeros(a_list):
    return [i for i in a_list if i>0]

exp_name= input("Experiment Name: ")
dataset = input("Dataset: ")
radius = float(input("Radius: "))
neigh_cutoff= int(input("Minimum number of Neighbors to Consider: "))

frame_out_path= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp_name+"/Epsilon_Results/Epsilon_Files/Epsilon_Single_BC/"
frame_out_path_2= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp_name+"/Epsilon_Results/Epsilon_Plots/Epsilon_Single_BC/"
frame_out_path_3= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp_name+"/Epsilon_Results/Epsilon_Plots/Epsilon_Single_BC_EPS/"


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
center_holder = [0]*len(index_list)

pic_title= "_Betweenness_Centrality"



G=nx.Graph()
G.add_nodes_from(index_list)

sub_dist_mat= dist_mat.loc[dist_mat["Dist"]<= radius,["Out","In"]]
sub_dist_mat= sub_dist_mat.loc[dist_mat["Out"]!=dist_mat["In"],:]
new_red= sub_dist_mat.to_records(index=False)
t_list= list(new_red)
G.add_edges_from(t_list)
print("Calculating _Betweenness_Centrality")
node_dict=betweenness_centrality(G)

print("Saving _Betweenness_Centrality")

for n in nx.classes.function.nodes(G):
    if len(list(G.neighbors(n)))!=0:
        fork_in= index_dict[n]
        neigh_holder[fork_in]= len(list(G.neighbors(n)))
        center_holder[fork_in]=node_dict[n]

G.remove_edges_from(G.edges())

count_frame= pd.DataFrame({"Degree":neigh_holder, "BC":center_holder} ,index= index_list)

count_frame.to_csv(frame_out_path+dataset+"_"+str(radius)+pic_title+".csv")

label = dataset+"_"+str(radius)+"_Centralty"



num_neigh = np.asarray(neigh_holder)
homog_neigh =np.asarray(center_holder)
non_zero= num_neigh>=neigh_cutoff
homog_neigh=homog_neigh[non_zero]
num_neigh= num_neigh[non_zero]

num_nodes= num_neigh.shape[0]
if (num_nodes==0):
    print("skipped")
else:


    fig, axs = plt.subplots(nrows=1, ncols=1)
    fig.suptitle(dataset+" Degree Distribution Epsilon:"+ str(radius))
    axs.set_title('Betweeness Centrality vs Epsilon')
    axs.set_xlabel('Node degree')
    axs.set_ylabel('Betweeness Centrality')
    #axs.set_yscale('log')
    axs.set_xscale('log')
    #axs.set_aspect('equal')
    axs.scatter(num_neigh,homog_neigh, alpha=0.3)
    #h=axs.hist2d(num_neigh,homog_neigh,norm=mpl.colors.LogNorm(),bins =bin_count)
    #fig.colorbar(h[3], ax= axs)

    #axs.legend()
        #h=ax.hist2d(new_degree,new_homog,norm=mpl.colors.LogNorm(),bins =50)
        #fig.colorbar(h[3], ax= ax)
    fig.tight_layout()
    plt.savefig(frame_out_path_2+label+"_bc_scatter.png")
    plt.savefig(frame_out_path_3+label+"_bc_scatter.eps")

    fig.clear()
