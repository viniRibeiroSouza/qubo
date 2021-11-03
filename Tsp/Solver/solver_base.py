from pyqubo import Array, Placeholder, Constraint
import numpy as np

class AnelSolver:
    pass


class TspSolver:
    def __init__(self, distance):
        self.distance = distance
        self.number_of_cities = self.distance.shape[0]
        self.time_const = 0.0
        self.city_const = 0.0
        # Must choose only the path for the other N-1 cities
        self.binary_decision = Array.create('c', (self.number_of_cities-1, self.number_of_cities-1), 'BINARY')
        self.origin_city = np.random.choice(np.arange(self.number_of_cities))
        self.another_cities = list(range(self.number_of_cities))
        self.another_cities.remove(self.origin_city)
        
    def build_constraints(self):
        # Constraint not to visit more than two cities at the same time.
        for i in range(self.number_of_cities):
            # If you wrap the hamiltonian by Const(...), this part is recognized as constraint
            self.time_const += Constraint((sum(self.binary_decision[i, j] for j in range(self.number_of_cities)) - 1) ** 2,
                                          label="time_{}".format(i))
        # Constraint not to visit the same city more than twice.
        for j in range(self.number_of_cities):
            self.city_const += Constraint((sum(self.binary_decision[i, j] for i in range(self.number_of_cities)) - 1) ** 2,
                                          label="city_{}".format(j))

    def calculate_cost_total_distance(self):
        # Cost function
        exp_origin = sum(self.distance[self.origin_city][self.another_cities[i]] * 1 * self.binary_decision[i][0] +
                         self.distance[self.number_of_cities[i]][self.origin_city] *
                         self.binary_decision[i][self.number_of_cities - 2] * 1 for i in range(self.number_of_cities - 1))
        exp_others = sum(self.distance[self.number_of_cities[i]][self.number_of_cities[j]] *
                         self.binary_decision[i][t] * self.binary_decision[j][t + 1]
                         for i in range(self.number_of_cities - 1)
                         for j in range(self.number_of_cities - 1)
                         for t in range(self.number_of_cities - 2))

    def build_hamiltonian(self):
        pass

    def compile_model(self):
        pass

    def build_qubo(self):
        pass

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
