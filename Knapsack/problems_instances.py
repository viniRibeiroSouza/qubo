import numpy as np
import os
import sys

# problem_instances = [ 
#         {
#             "weights": [1, 3, 7, 9],
#             "values": [10, 2, 3, 6],
#             "max_weight": 10
#         },
#         {
#             "weights": [1, 3, 7, 9],
#             "values": [1, 2, 30, 30],
#             "max_weight": 10
#         },
#         {
#             "weights": [1, 3, 7, 9],
#             "values": [1, 2, 40, 30],
#             "max_weight": 10
#         }
#     ]

def knapsack_read_file(filename):
    filename = os.path.join(sys.path[0], filename)
    print(filename)
    my_file = open(filename, "r")
    lines = my_file.readlines()
    instances = []
    i = 0
    while i < len(lines):
        name = lines[i]
        i += 1
        l = lines[i].strip().split(' ')
        size = int(l[1])
        i += 1
        l = lines[i].strip().split(' ')
        cap = float(l[1])
        i += 1
        l = lines[i].strip().split(' ')
        opt_z = float(l[1])
        i += 1
        l = lines[i].strip().split(' ')
        time = float(l[1])
        i += 1
        values = np.zeros((size))
        weights = np.zeros((size))
        sol = np.zeros((size))
        j = 0
        while j < size:
            l = lines[i].strip().split(',')
            index = int(l[0]) - 1
            values[index] = float(l[1])
            weights[index] = float(l[2])
            sol[index] = int(l[3])
            i += 1
            j += 1
        i += 2
        instances.append({
            "name": name, 
            "size": size, 
            "max_weight": cap, 
            "opt_z": opt_z, 
            "time": time, 
            "values": values, 
            "weights": weights, 
            "solution" : sol
            })
    print(instances)
    return instances

problem_instances = knapsack_read_file("Knapsack/knapPI_11_20_1000.csv")
