import csv
import time
import os

from Knapsack.PyquboAndSA.pyqubo_onehotenc_solver import PyQuboOneHotEncSolver
from Knapsack.PyquboAndSA.pyqubo_logenc_solver import PyQuboLogEncSolver
from Knapsack.QUBO.qubo import KnapsackQUBOSolver
from timeit import default_timer as timer

path = "solution/"
fieldnames = ['solver', 'solution', 'energy', 'is_feasible', 'time_elapsed']

problems = {
    "Knapsack": [PyQuboOneHotEncSolver(), KnapsackQUBOSolver(), PyQuboLogEncSolver()],
    "TSP": [],
    "Cacheiro Mochileiro": []
}

def create_csv_file(problem):
    try:
        os.mkdir(path)
    except OSError as error:
        pass
    timestr = time.strftime("%Y%m%d-%H%M%S")
    csv_file = open(f'{path}{problem.lower()}-{timestr}.csv', mode='w')
    result_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    result_writer.writeheader()
    return result_writer


if __name__ == "__main__":
    for problem, solvers in problems.items():
        if not solvers:
            continue

        print(f"================ {problem.upper()} PROBLEM ================")
        problem_instances = solvers[0].problem_instances()
        result_writer = create_csv_file(problem)

        for solver in solvers:
            print(f"=========== {solver._type().upper()} ===========")
            for count, instance in enumerate(problem_instances, start=1):
                print(f"======== INSTANCE {count} ========")

                best_feasible = None
                time_elapsed = .0
                retry = 0
                while not best_feasible and retry < 4:
                    start = timer()
                    best_feasible = solver.solve_problem(instance)
                    end = timer()

                    time_elapsed = end - start
                    print(f"time elapsed: {time_elapsed}")
                    if not best_feasible[0]:
                        print("Could not found a good solution \n --------")
                        retry += 1
                        
                if best_feasible:
                    result_writer.writerow({
                        'solver': solver._type(),
                        'solution': best_feasible[0],
                        'energy': best_feasible[1], 
                        'is_feasible': best_feasible[2], 
                        'time_elapsed': time_elapsed
                    })

    print(f"==================================================")
