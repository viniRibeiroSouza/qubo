import csv
import time

from Knapsack.PyquboAndSA.pyqubo_onehotenc_solver import PyQuboOneHotEncSolver
from Knapsack.PyquboAndSA.pyqubo_logenc_solver import PyQuboLogEncSolver
from Knapsack.QUBO.qubo import KnapsackQUBOSolver
from timeit import default_timer as timer

fieldnames = ['solver', 'solution', 'energy', 'is_feasible', 'time_elapsed']

problems = {
    "Knapsack": [PyQuboOneHotEncSolver(), KnapsackQUBOSolver(), PyQuboLogEncSolver()],
    "TSP": [],
    "Cacheiro Mochileiro": []
}

if __name__ == "__main__":
    for problem, solvers in problems.items():
        print(f"================ {problem.upper()} PROBLEM ================")

        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open(f'{problem.lower()}-{timestr}.csv', mode='w') as csv_file:
            result_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            result_writer.writeheader()

            for solver in solvers:
                print(f"=========== {solver.__class__.__name__.upper()} ===========")
                for count, instance in enumerate(solver.problem_instances(), start=1):
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
                        print(f"sol: {best_feasible}")
                        result_writer.writerow({
                            'solver': solver._type(),
                            'solution': best_feasible[0],
                            'energy': best_feasible[1], 
                            'is_feasible': best_feasible[2], 
                            'time_elapsed': time_elapsed
                        })

    print(f"==================================================")
