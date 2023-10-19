import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
import networkx as nx


import os




group= input("Experiment")
dataset = input("Dataset: ")
rad=float(input("Radius: "))


frame_out_path= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+group+"/Epsilon_Results/Epsilon_Plots/Epsilon_Graphs_FDL/"

data_path = "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+group+"/"+dataset+".csv"
dist_path= "/media/timothyhamilton/Seagate Desktop Drive/Tim_Hamilton/Epsilon_Borders/"+group+"/"+dataset+"_Dist_Form.txt"

data = pd.read_csv(data_path,index_col=0,usecols=[0,1])

cell_ids = data.index.values.tolist()
cell_values = data.iloc[:,0].values.tolist()

cell_dict=dict(list(zip(cell_ids,cell_values)))


cmap = mpl.colormaps['tab10']
cell_types = list(set(cell_values))
cell_types.sort()
if len(cell_types)==1:
    step_size = 1
    col_float= np.arange(0,step_size,step_size).tolist()
else:
    step_size = 1/(len(cell_types)-1)
    col_float= np.arange(0,1+step_size,step_size).tolist()
cell_col_dict= dict(list(zip(cell_types, [cmap(i) for i in col_float])))



try:
    os.makedirs(frame_out_path)
except OSError:
    print ("Creation of the directory %s failed" % frame_out_path)
else:
    print ("Successfully created the directory %s" % frame_out_path)






dist_mat = pd.read_csv(dist_path,sep = "\t",header= None)
dist_mat.columns= ["Out","In", "Dist"]
sub_dist_mat= dist_mat.loc[dist_mat["Dist"]<= rad,["Out","In"]]
sub_dist_mat= sub_dist_mat.loc[dist_mat["Out"]!=dist_mat["In"],:]

G= nx.Graph()
new_red= sub_dist_mat.to_records(index=False)
t_list= list(new_red)
G.add_edges_from(t_list)

node_list=[]
for n in nx.classes.function.nodes(G):
    if len(list(G.neighbors(n)))==0:
        node_list.append(n)
G.remove_nodes_from(node_list)

reverse_dict_holder=np.zeros((nx.classes.function.number_of_nodes(G),4))

for i,n in enumerate(nx.classes.function.nodes(G)):
    type_holder= cell_col_dict[cell_dict[n]]
    reverse_dict_holder[i,:]= type_holder
print("Coloring Cells")

fig= plt.figure(figsize=(16,8))
pos = nx.spring_layout(G)
options = {"node_size": 100}
nx.draw_networkx_nodes(G, pos,node_color=reverse_dict_holder,cmap = cmap ,**options)

custom_lines = [Line2D([0], [0], color=cell_col_dict[j], lw=4) for j in cell_types]

nx.draw_networkx_edges(G,pos, edge_color="r")
plt.axis('off')
plt.savefig(frame_out_path+dataset+"_r_"+str(rad)+"_network_viz.png")
plt.savefig(frame_out_path+dataset+"_r_"+str(rad)+"_network_viz.eps")
plt.clf()
plt.axis('off')
plt.legend(custom_lines, cell_types,ncol=3)#Change n_cols for apprearn
plt.savefig(frame_out_path+dataset+"_r_"+str(rad)+"_network_viz_Legend.png")
plt.savefig(frame_out_path+dataset+"_r_"+str(rad)+"_network_viz_Legend.eps")
