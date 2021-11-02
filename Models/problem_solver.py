from abc import abstractmethod


from abc import ABC, abstractmethod

class ProblemSolver(ABC):
    @abstractmethod
    def solve_problem(self):
        pass
