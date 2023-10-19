import pandas as pd
import numpy as np
import os
import networkx as nx



exp_name= input("Experiment Name: ")
dataset = input("Dataset: ")
min_dist=float(input("Min_Distance: "))
max_dist=float(input("Max Distance: "))
step_size=float(input("step_size: "))

frame_out_path= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp_name+"/Epsilon_Results/Epsilon_Files/Epsilon_Degree_Only/"+dataset+"_"+str(min_dist)+"_"+str(max_dist)+"_"+str(step_size)



dist_mat_path =  "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp_name+"/"+ dataset+"_Dist_Form.txt"




try:
    os.makedirs(frame_out_path)
except OSError:
    print ("Creation of the directory %s failed" % frame_out_path)
else:
    print ("Successfully created the directory %s" % frame_out_path)




dist_mat = pd.read_csv(dist_mat_path,sep = "\t",header= None)
print("Reading Distance_Matrix")
dist_mat.columns= ["Out","In", "Dist"]

index_list=list(set(dist_mat["Out"].values.tolist()))# This is for making csv Order is not preserved

index_dict = dict(zip(index_list,list(range(len(index_list)))))

rad_list= np.arange(min_dist,max_dist,step_size).tolist()

neigh_holder = np.zeros((len(index_list),len(rad_list)))

pic_title= "/Neighborhoods"


G=nx.Graph()
G.add_nodes_from(index_list)

for indexer, rad in enumerate(rad_list):
    sub_dist_mat= dist_mat.loc[dist_mat["Dist"]<= rad,["Out","In"]]
    sub_dist_mat= sub_dist_mat.loc[dist_mat["Out"]!=dist_mat["In"],:]
    new_red= sub_dist_mat.to_records(index=False)
    t_list= list(new_red)
    G.add_edges_from(t_list)


    print("Saving Neighborhoods")

    for n in nx.classes.function.nodes(G):
        if len(list(G.neighbors(n)))!=0:
            fork_in= index_dict[n]
            degree_val= len(list(G.neighbors(n)))
            neigh_holder[fork_in, indexer]= degree_val

    G.remove_edges_from(G.edges())

count_frame= pd.DataFrame(neigh_holder,columns=rad_list, index= index_list)

count_frame.to_csv(frame_out_path+pic_title+".csv")
