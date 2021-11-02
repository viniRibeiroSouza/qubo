import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_weighted_edges_from({(0, 1, .1), (0, 2, .5), (0, 3, .1), (1, 2, .1),(1, 3, .5), (2, 3, .1)})
plt.figure(figsize=(3, 3))
pos = nx.spring_layout(G)
nx.draw_networkx(G)
plt.axis("off")
plt.show()
