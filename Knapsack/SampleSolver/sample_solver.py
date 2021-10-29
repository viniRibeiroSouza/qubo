import neal
from pyqubo import Binary, Constraint, Placeholder, Array, OneHotEncInteger
weights = [1, 3, 7, 9]
values = [10, 2, 3, 6]
max_weight = 10
# create the array of 0-1 binary variables
# representing the selection of the items
n=len(values)
items = Array.create('item', shape=n, vartype="BINARY")
# define the sum of weights and values using variables
knapsack_weight = sum(weights[i] * items[i] for i in range(n))
knapsack_value = sum(values[i] * items[i] for i in range(n))

# define the coefficients of the penalty terms,
# lmd1 and lmd2, using Placeholder class
# so that we can change their values after compilation
lmd1 = Placeholder("lmd1")
lmd2 = Placeholder("lmd2")
# create Hamiltonian and model
weight_one_hot = OneHotEncInteger("weight_one_hot", value_range=(1, max_weight), strength=lmd1)
Ha = Constraint((weight_one_hot - knapsack_weight)**2,
                "weight_constraint")
Hb = knapsack_value
H = lmd2*Ha - Hb
model = H.compile()
# use simulated annealing (SA) sampler of neal package
sampler = neal.SimulatedAnnealingSampler()
feasible_sols = []
# search the best parameters: lmd1 and lmd2
for lmd1_value in range(1, 10):
    for lmd2_value in range(1, 10):
        feed_dict = {'lmd1': lmd1_value, "lmd2": lmd2_value}
        qubo, offset = model.to_qubo(feed_dict=feed_dict)
        bqm = model.to_bqm(feed_dict=feed_dict)
        bqm.normalize()
        sample_set = sampler.sample(bqm, num_reads=10,
                                    sweeps=1000, beta_range=(1.0, 50.0))
        dec_samples = model.decode_sampleset(sample_set, feed_dict=feed_dict)
        best = min(dec_samples, key=lambda x: x.energy)

        # store the feasible solution
        if not best.constraints(only_broken=True):
            feasible_sols.append(best)
best_feasible = min(feasible_sols, key=lambda x: x.energy)
print(f"selection = {[best_feasible.sample[f'item[{i}]'] for i in range(n)]}")
print(f"sum of the values = {-best_feasible.energy}")

# [output]
# selection = [1, 0, 0, 1]
# sum of the values = 16.0