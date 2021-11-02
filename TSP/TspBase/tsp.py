from pyqubo import Array, Placeholder, Constraint
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class Map:
    def __init__(self, dict_city: dict):
        self.graph = nx.Graph()
        self.dict_city = dict_city
                        

    def build_city_map(self, cities, sol=None):
        n_city = len(cities)
        cities_dict = dict(cities)
        for city in cities_dict:
            self.graph.add_node(city)

    # draw path
    if sol:
        city_order = []
        for i in range(n_city):
            for j in range(n_city):
                if sol.array('c', (i, j)) == 1:
                    city_order.append(j)
        for i in range(n_city):
            city_index1 = city_order[i]
            city_index2 = city_order[(i + 1) % n_city]
            G.add_edge(cities[city_index1][0], cities[city_index2][0])

    plt.figure(figsize=(3, 3))
    pos = nx.spring_layout(G)
    nx.draw_networkx(G)
    plt.axis("off")
    plt.show()


def dist(i, j, cities):
    pos_i = cities[i][1]
    pos_j = cities[j][1]
    return np.sqrt((pos_i[0] - pos_j[0]) ** 2 + (pos_i[1] - pos_j[1]) ** 2)


# City names and coordinates list[("name", (x, y))]
cities = [
    ("a", (0, 0)),
    ("b", (1, 3)),
    ("c", (3, 2)),
    ("d", (2, 1)),
    ("e", (0, 1))
]
plot_city(cities)

# n_city = len(cities)
# x = Array.create('c', (n_city, n_city), 'BINARY')
#
# # Constraint not to visit more than two cities at the same time.
# time_const = 0.0
# for i in range(n_city):
#     # If you wrap the hamiltonian by Const(...), this part is recognized as constraint
#     time_const += Constraint((sum(x[i, j] for j in range(n_city)) - 1)**2, label="time{}".format(i))
#
# # Constraint not to visit the same city more than twice.
# city_const = 0.0
# for j in range(n_city):
#     city_const += Constraint((sum(x[i, j] for i in range(n_city)) - 1)**2, label="city{}".format(j))
#
# # distance of route
# distance = 0.0
# for i in range(n_city):
#     for j in range(n_city):
#         for k in range(n_city):
#             d_ij = dist(i, j, cities)
#             distance += d_ij * x[k, i] * x[(k+1)%n_city, j]
#
#
# # Construct hamiltonian
# A = Placeholder("A")
# H = distance + A * (time_const + city_const)
#
# # Compile model
# model = H.compile()
#
# # Generate QUBO
# feed_dict = {'A': 4.0}
# bqm = model.to_bqm(feed_dict=feed_dict)