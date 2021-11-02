from Knapsack.problems_instances import problem_instances
from Models.problem_solver import ProblemSolver

import numpy as np
import math
import gurobipy as gp
from gurobipy import GRB
import itertools
import copy
import numpy.random
import dimod, neal
from dwave.system import DWaveSampler

class KnapsackQUBOSolver(ProblemSolver):
    def problem_instances(self):
        return problem_instances

    def solve_problem(self, problem_instance: dict):
        w = np.array(problem_instance['weights'])
        c = np.array(problem_instance['values'])
        capacity = problem_instance['max_weight']

        assert c.size == w.size, "The number of values and weights must be equal"
        A = np.array([w])
        b = np.array([capacity])
        ineq_types = ["<="]
        problem_type = "max"
        return self._solve_knapsack_problem(
            c, A, b, ineq_types, problem_type
        )

    def _solve_knapsack_problem(self, c, A, b, ineq_types, problem_type):
        assert c.size == A.shape[1], "The size of A does not match the number of variables"
        assert A.shape[0] == b.shape[0], "The size of b does not match the number of inequalities in A"
        assert len(ineq_types) == b.shape[0], "The number of inequality types does not match the number of inequalities in A and b"
        orig_n = A.shape[1]
        if problem_type == "max":
            cc = np.copy(c)
        elif problem_type == "min":
            cc = -1.0 * np.copy(c)
        else:
            print("Problem type invalid. Must be max or min.")
            return
        AA = np.copy(A)
        bb = np.copy(b)
        ineq_typess = copy.copy(ineq_types)
        AA, bb, ineq_typess = self.correct_ineqs(AA, bb, ineq_typess)
        n, cc, AA, bb = self.equality_matrix(cc, AA, bb, ineq_typess)
        qubo_mat = self.make_qubo_matrix(cc, AA, bb)
        ## uncomment the lines below for pre-processing of the qubo matrix
        #q_mat, n_orig_var, n_red_var, fixed_variables, fixed_indices = preprocess_qubo(qubo_mat)
        #x = gurobi_solve_qubo(q_mat)
        #sol = expand_red_sol(x, n_orig_var, fixed_variables, fixed_indices)[:orig_n]
        sol = self.gurobi_solve_qubo(qubo_mat)[:orig_n]
        return sol, np.dot(sol, c), self.is_feasible(sol, A, b, ineq_types) # not returning value of slack variables

    def correct_ineqs(self, A, b, ineq_types):
        assert A.shape[0] == b.shape[0], "The size of b does not match the number of inequalities in A"
        m = A.shape[0]
        for i in range(m):
            rhs = b[i]
            if rhs < 0:
                if ineq_types[i] == "<=":
                    A[i, :] *= -1.0
                    b[i] *= -1.0
                    ineq_types[i] = ">="
                    print("less than")
                elif ineq_types[i] == ">=":
                    A[i, :] *= -1.0
                    b[i] *= -1.0
                    ineq_types[i] = "<="
                    print("greater than")
        return A, b, ineq_types
    
    def equality_matrix(self, c, A, b, ineq_types):
        assert c.size == A.shape[1], "The size of A does not match the number of variables"
        assert A.shape[0] == b.shape[0], "The size of b does not match the number of inequalities in A"
        n = A.shape[1]
        m = A.shape[0]
        for i in range(m):
            if ineq_types[i] == "<=":
                n, c, A, b = self.leq_to_eq(i, c, A, b)
            elif ineq_types[i] == ">=":
                n, c, A, b = self.geq_to_eq(i, c, A, b)
        return n, c, A, b

    def make_qubo_matrix(self, c, A, b):
        assert c.size == A.shape[1], "The size of A does not match the number of variables"
        assert A.shape[0] == b.shape[0], "The size of b does not match the number of inequalities in A"
        m, n = A.shape
        P = -1.0 * (sum(abs(v) for v in c) + 1)
        q_mat = np.zeros((n,n), dtype=float)
        for i in range(n):
            q_mat[i,i] += c[i]
            for k in range(m):
                q_mat[i,i] += P * ((A[k,i] ** 2) - (2 * b[k] * A[k,i]))
        for i in range(n):
            for j in range(n):
                if i != j:
                    for k in range(m):
                        q_mat[i,j] += P * A[k,i] * A[k,j]
        return q_mat

    def gurobi_solve_qubo(self, q_mat):
        assert q_mat.shape[0] == q_mat.shape[1]
        n = q_mat.shape[0]
        model = gp.Model()
        var = model.addVars(n, vtype=GRB.BINARY)
        model.setObjective(self.qubo_obj_func(q_mat,var), GRB.MAXIMIZE)
        model.optimize()
        return [var[i].X for i in range(n)]
    
    def is_feasible(self, x, A, b, ineq_types):
        assert A.shape[0] == b.shape[0], "The size of b does not match the number of inequalities in A"
        assert len(ineq_types) == b.shape[0], "The number of inequality types does not match the number of inequalities in A and b"
        m = A.shape[0]
        feasibility = True
        for i in range(m):
            s = np.dot(x, A[i,:])
            if ineq_types[i] == "<=" and s > b[i]:
                feasibility = False
            if ineq_types[i] == ">=" and s < b[i]:
                feasibility = False
            if ineq_types[i] == "==" and s != b[i]:
                feasibility = False
        return feasibility
    
    def qubo_obj_func(self, q, var):
        n = q.shape[0]
        s = 0
        for i in range(n):
            s += q[i,i] * var[i]
            for j in range(n):
                if i != j:
                    s += q[i,j] * var[i] * var[j]
        return s
    
    def leq_to_eq(self, row_index, c, A, b):
        assert b[row_index] >= 0, "The less than inequality must have a non-negative right-hand side"
        assert A.shape[0] == b.shape[0], "The size of b does not match the number of inequalities in A"
        num_rows = A.shape[0]
        rhs = b[row_index]
        row = A[row_index, :]
        new_row = np.copy(row)
        new_n = A.shape[1]
        neg_range = abs(sum(v for v in row if v < 0)) + rhs
        if neg_range > 0:
            neg_log = math.floor(math.log(neg_range, 2))
            k = neg_log + 1
            mat_part = mat_part = np.zeros((num_rows, k), dtype=float)
            mat_part[row_index] = np.array([2**i for i in range(0,neg_log+1)])
            A = np.hstack((A,mat_part))
            c_part = np.zeros((k), dtype=float)
            c = np.append(c, c_part)
            new_n += k
        return new_n, c, A, b

    def geq_to_eq(self, row_index, c, A, b):
        assert b[row_index] >= 0, "The less than inequality must have a non-negative right-hand side"
        assert A.shape[0] == b.shape[0], "The size of b does not match the number of inequalities in A"
        num_rows = A.shape[0]
        rhs = b[row_index]
        row = A[row_index, :]
        new_row = np.copy(row)
        new_n = A.shape[1]
        pos_range = sum(v for v in row if v > 0) - rhs
        if pos_range > 0:
            pos_log = math.floor(math.log(pos_range, 2))
            k = pos_log + 1
            mat_part = np.zeros((num_rows, k), dtype=float)
            mat_part[row_index] = np.array([-1.0 * (2**i) for i in range(0,pos_log + 1)])
            A = np.hstack((A, mat_part))
            c_part = np.zeros((k), dtype=float)
            c = np.append(c, c_part)
            new_n += k
        return new_n, c, A, b