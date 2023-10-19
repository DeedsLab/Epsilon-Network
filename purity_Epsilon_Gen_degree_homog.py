import pandas as pd
import numpy as np


import networkx as nx
import os

#DOCSTRING HEADER For This barcodes
#Dependencies: pandas,numpy. networkx





exp_name= input("Experiment Name: ")
dataset = input("Dataset: ")
min_dist=float(input("Min_Distance: "))
max_dist=float(input("Max Distance: "))
step_size=float(input("step_size: "))

frame_out_path= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp_name+"/Epsilon_Results/Epsilon_Files/Epsilon_Degree_Homog/"+dataset+"_"+str(min_dist)+"_"+str(max_dist)+"_"+str(step_size)

data_path = "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp_name+"/"+ dataset+".csv"


dist_mat_path =  "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+exp_name+"/"+ dataset+"_Dist_Form.txt"




try:
    os.makedirs(frame_out_path)
except OSError:
    print ("Creation of the directory %s failed" % frame_out_path)
else:
    print ("Successfully created the directory %s" % frame_out_path)


data= pd.read_csv(data_path, index_col=0,usecols= [0,1])
cell_values= data.iloc[:,0].values.tolist()
index_list= data.index.values.tolist()#Saving list of index of dataframe (can be integers or barcodes )
index_dict = dict(zip(index_list,list(range(len(index_list)))))
type_dict= dict(zip(index_list,cell_values))




dist_mat = pd.read_csv(dist_mat_path,sep = "\t",header= None)
dist_mat.columns= ["Out","In", "Dist"]
rad_list= np.arange(min_dist,max_dist,step_size).tolist()

neigh_holder = np.zeros((len(index_list),len(rad_list)))
homog_holder= np.zeros((len(index_list),len(rad_list)))
pic_title= "/Neighborhoods"
pic_title_2="/Homogeneity"
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
            for j in list(G.neighbors(n)):
                if type_dict[n]==type_dict[j]:
                    homog_holder[fork_in,indexer]+=1
            homog_holder[fork_in,indexer]/=len(list(G.neighbors(n)))

    G.remove_edges_from(G.edges())




print("hi")
count_frame= pd.DataFrame(neigh_holder,columns=rad_list, index= index_list)
count_frame.insert(0,"Cell_Type", cell_values, True)

count_frame.to_csv(frame_out_path+pic_title+".csv")

homog_frame= pd.DataFrame(homog_holder,columns=rad_list, index= index_list)
homog_frame.insert(0,"Cell_Type", cell_values, True)
homog_frame.to_csv(frame_out_path+pic_title_2+".csv")
