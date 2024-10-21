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

    def DPLL(self, clauses, assignment):
      return self.dpll(clauses, assignment)

    # For DPLL
    def unit_propogate(self, clauses, assignment):
      unit_clauses = [c for c in clauses if len(c) == 1]
    
      while unit_clauses:
        unit = unit_clauses[0]
        lit = unit[0]
        assignment[abs(lit)] = lit > 0

        clauses = [c for c in clauses if lit not in c]

        for clause in clauses:
          if -lit in clause:
            clause.remove(-lit)

        unit_clauses = [c for c in clauses if len(c) == 1]
    
      return clauses, assignment
  
    # For DPLL
    def pure_literal_elim(self, clauses, assignment):
      literals = set()
      for clause in clauses:
        for lit in clause:
          literals.add(lit)

      pure_literals = [lit for lit in literals if -lit not in literals]

      for lit in pure_literals:
        assignment[abs(lit)] = lit > 0
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
          var = abs(lit)
          break
        break

      new_assignment = assignment.copy()
      new_assignment[var] = True
      new_clauses = [c for c in clauses if var not in c]
      for claue in new_clauses:
        if -var in clause:
          clause.remove(-var)

      satisfiable, final_assignment = self.dpll(new_clauses, new_assignment)

      if satisfiable:
        return True, final_assignment
    
      new_assigment = assignment.copy()
      new_assignment[var] = False
      new_clauses = [c for c in clauses if -var not in c]
      for clause in new_clauses:
        if var in clause:
          clause.remove(var)

      return self.dpll(new_clauses, new_assigment)