from TspMap import TspMap
import networkx as nx
import numpy as np
# City Map dict[("NodeOrigin", (NodeDestiny1,...))]
city_dict = {'0':[('0','1', 3.0)],
             '1':[('1','2', 7.5)],
             '2':[('2','0', 7.5)],
             '3':[('3','2', 7.5)]}

tsp_instance = TspMap(dict_city=city_dict)
tsp_instance.build_map_graph()
tsp_instance.visualize_map()

adj = nx.adjacency_matrix(tsp_instance.graph)
print(adj.to_numpy_array())