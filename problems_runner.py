from Knapsack.Dwave.dwave import KnapsackDwaveSolver
from Knapsack.SampleSolver.sample_solver import KnapsackSampleSolver
from timeit import default_timer as timer
problems = {
    "Knapsack": [KnapsackSampleSolver()]
}

if __name__ == "__main__":
    for problem, solvers in problems.items():
        print(f"================ {problem.upper()} PROBLEM ================")

        for solver in solvers:
            print(f"=========== {solver.__class__.__name__.upper()} ===========")
            for count, instance in enumerate(solver.problem_instances(), start=1):
                print(f"======== INSTANCE {count} ========")

                best_feasible = None
                retry = 0
                while not best_feasible and retry < 4:
                    start = timer()
                    best_feasible = solver.solve_problem(instance)
                    end = timer()

                    print(f"time elapsed: {end - start}")
                    if not best_feasible:
                        print("Could not found the best solution \n --------")
                        retry += 1
                        
                if best_feasible:
                    print(f"selection = {[best_feasible.sample[f'item[{i}]'] for i in range(len(instance['values']))]}")
                    print(f"sum of the values = {-best_feasible.energy}")

    print(f"==================================================")
    