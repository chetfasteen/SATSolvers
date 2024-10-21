# File: Solvers.py
import random
import math

class Solvers:
    def __init__(self, num_vars, num_clauses, clauses):
        self.numVars = num_vars
        self.numClauses = num_clauses
        self.clauses = clauses

    def G_SAT(self, maxFlips=10000):
        assignment = [random.choice([True, False]) for _ in range(self.numVars)]
        for _ in range(maxFlips):
            if self.is_satisfied(assignment):
                return True, assignment

            bestFlip = None
            maxSatisfied = 0

            for i in range(self.numVars):
                assignment[i] = not assignment[i]
                satisfiedClauses = sum(1 for clause in self.clauses if self.is_satisfied_clause(clause, assignment))

                if satisfiedClauses > maxSatisfied:
                    maxSatisfied = satisfiedClauses
                    bestFlip = i

                assignment[i] = not assignment[i]

            if bestFlip is not None:
                assignment[bestFlip] = not assignment[bestFlip]

        return False, None

    def Simulated_Annealing(self, maxIters=10000, temp=1.0, coolingRate=0.99):
        assignment = [random.choice([True, False]) for _ in range(self.numVars)]
        for j in range(maxIters):
            if self.is_satisfied(assignment):
                return True, assignment

            flipVar = random.randint(0, self.numVars - 1)
            currentSatisfied = sum(1 for clause in self.clauses if self.is_satisfied_clause(clause, assignment))

            assignment[flipVar] = not assignment[flipVar]
            newSatisfied = sum(1 for clause in self.clauses if self.is_satisfied_clause(clause, assignment))

            delta = newSatisfied - currentSatisfied

            if delta < 0:  # Worse solution
                acceptanceProb = math.exp(delta / temp)
            else:
                acceptanceProb = 1.0

            if random.random() > acceptanceProb:
                assignment[flipVar] = not assignment[flipVar]

            temp *= coolingRate

        return False, None

    def is_satisfied(self, assignment):
        return all(self.is_satisfied_clause(clause, assignment) for clause in self.clauses)

    def is_satisfied_clause(self, clause, assignment):
        return any((literal > 0 and assignment[abs(literal) - 1]) or
                   (literal < 0 and not assignment[abs(literal) - 1]) for literal in clause)

    def DPLL(self):
        clauses = self.clauses
        assignment = [False] * self.numVars

        return self.dpll(clauses, assignment)

        # For DPLL

    def unit_propogate(self, clauses, assignment):
        unit_clauses = [c for c in clauses if len(c) == 1]

        while unit_clauses:
            unit = unit_clauses[0]
            lit = unit[0]
            var = abs(lit) - 1
            assignment[var] = lit > 0

            clauses = [c for c in clauses if lit not in c]

            for clause in clauses:
                if -lit in clause:
                    clause.remove(-lit)

            unit_clauses = [c for c in clauses if len(c) == 1]

        return clauses, assignment

        # For DPLL

    def pure_literal_elim(self, clauses, assignment):

        literals = set(lit for clause in clauses for lit in clause)
        pure_literals = [lit for lit in literals if -lit not in literals]

        for lit in pure_literals:
            var = abs(lit) - 1
            assignment[var] = lit > 0
            clauses = [c for c in clauses if lit not in c]

        return clauses, assignment

    def dpll(self, clauses, assignment):
        # Base Cases
        if not clauses:
            return True, assignment

        if any([len(c) == 0 for c in clauses]):
            return False, assignment

        clauses, assignment = self.unit_propogate(clauses, assignment)

        clauses, assignment = self.pure_literal_elim(clauses, assignment)

        if not clauses:
            return True, assignment

        if any([len(c) == 0 for c in clauses]):
            return False, assignment

        for clause in clauses:
            for lit in clause:
                var = abs(lit) - 1
                # Just choose the first variable that hasn't been set differently during unit propagation or pure literal elimination
                if assignment[var] == False:  # Assume unassigned means False in the initial pass
                    break  # Break from inner loop when a variable is found
            if assignment[var] == False:
                break  # Now break from outer loop once an unassigned variable is found

        new_assignment = assignment.copy()
        new_assignment[var] = True
        new_clauses = [c for c in clauses if var + 1 not in c]
        for clause in new_clauses:
            if -(var + 1) in clause:
                clause.remove(-(var + 1))

        satisfiable, final_assignment = self.dpll(new_clauses, new_assignment)

        if satisfiable:
            return True, final_assignment

        new_assignment = assignment.copy()
        new_assignment[var] = False
        new_clauses = [c for c in clauses if -(var + 1) not in c]
        for clause in new_clauses:
            if var in clause:
                clause.remove(var)

        return self.dpll(new_clauses, new_assignment)
