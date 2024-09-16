from abc import abstractmethod, abstractproperty


from abc import ABC, abstractmethod
from typing import Dict

class ProblemSolver(ABC):
    @property
    @abstractmethod
    def problem_instances(self):
        return {}

    @abstractmethod
    def solve_problem(self):
        raise NotImplementedError()
    
    def _type(self):
        return self.__class__.__name__
