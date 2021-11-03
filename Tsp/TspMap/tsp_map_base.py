import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class TspMap:
    def __init__(self, dict_city: dict):
        self.graph = nx.Graph()
        self.dict_city = dict_city
        self.len_dict = len(self.dict_city)

    def build_map_graph(self):
        self.graph.add_nodes_from(self.dict_city.keys())
        for keys, values in self.dict_city.items():
            self.graph.add_weighted_edges_from(values, color='black')

    def visualize_map(self):
        plt.figure(figsize=(5, 5))
        colors = nx.get_edge_attributes(self.graph, 'color').values()
        nx.draw_networkx(self.graph,
                         nx.spring_layout(self.graph),
                         node_color=['red' if i == 2 else 'lightblue' for i in range(self.len_dict)],
                         edge_color=colors,
                         with_labels=True)
        plt.title('Tsp Map')
        plt.axis("off")
        plt.show()

    # draw path
    # if sol:
    #     city_order = []
    #     for i in range(n_city):
    #         for j in range(n_city):
    #             if sol.array('c', (i, j)) == 1:
    #                 city_order.append(j)
    #     for i in range(n_city):
    #         city_index1 = city_order[i]
    #         city_index2 = city_order[(i + 1) % n_city]
    #         G.add_edge(cities[city_index1][0], cities[city_index2][0])


def dist(i, j, cities):
    pos_i = cities[i][1]
    pos_j = cities[j][1]
    return np.sqrt((pos_i[0] - pos_j[0]) ** 2 + (pos_i[1] - pos_j[1]) ** 2)


