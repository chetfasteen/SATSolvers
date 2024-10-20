# File: Solvers.py
# Description: Define the 3 SAT Solvers
import random
import math

class Solvers:
    def __init__(self, num_vars, num_clauses, clauses):
        self.numVars = num_vars
        self.numClauses = num_clauses
        self.clauses = clauses

    def G_SAT(self, maxFlips = 10000):
        assignment = []
        for _ in range(self.numVars):
            randVal = random.choice([True, False])
            assignment.append(randVal)

        for _ in range(maxFlips):
            if self.is_satisfied(assignment):
                return True, assignment

            bestFlip = None
            maxSatisfied = 0
            for i in range(self.numVars):
                assignment[i] = not assignment[i]
                satisfiedClauses = 0

                for clause in self.clauses:
                    if self.is_satisfied_clause(clause, assignment):
                        satisfiedClauses += 1

                if satisfiedClauses > maxSatisfied:
                    maxSatisfied = satisfiedClauses
                    bestFlip = i

                assignment[i] = not assignment[i]

                if bestFlip is not None:
                    assignment[bestFlip] = not assignment[bestFlip]

        return False, None

    def Simulated_Annealing(self, maxIters = 10000, temp = 1.0, coolingRate = 0.99):
        assignment = []
        for i in range(self.numVars):
            randVal = random.choice([True, False])
            assignment.append(randVal)

        for j in range(maxIters):
            if self.is_satisfied(assignment):
                return True, assignment

            flipVar = random.randint(0, self.numVars - 1)
            assignment[flipVar] = not assignment[flipVar]
            numUnsatisfied = 0

            for clasue in self.clauses:
                if not self.is_satisfied_clause(clasue, assignment):
                    numUnsatisfied += 1

            if numUnsatisfied == 0:
                return True, assignment

            delta = numUnsatisfied

            if delta > 0:
                acceptanceProb = math.exp(-delta/temp)
            else:
                acceptanceProb = 1.0

            if random.random() > acceptanceProb:
                assignment[flipVar] = not assignment[flipVar]

            temp*= coolingRate

        return False, None

    def DPLL(self):
        return

    def is_satisfied(self, assignment):
        for clause in self.clauses:
            if not self.is_satisfied_clause(clause, assignment):
                return False

        return True

    def is_satisfied_clause(self, clause, assignment):
        for literal in clause:
            varIdx = abs(literal) - 1
            if (literal > 0 and assignment[varIdx]) or (literal < 0 and not assignment[varIdx]):
                return True

        return False
