# File: Main.py
# Description: Read and parse the cnf file. Run the solvers. Collect and display the data.
import os
import Solvers

def process_cnf_files(folder_path):
    return

def parse(filename):
    clauses = []
    numVars = 0
    numClauses = 0
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('c'):
                continue
            if line.startswith('p cnf'):
                parts = line.split()
                numVars = int(parts[2])
                numClauses = int(parts[3])
                continue
            clause = []
            for literal in line.split():
                literal = int(literal)
                if literal == 0:
                    break
                clause.append(literal)
            if len(clause) > 0:
                clauses.append(clause)
    return numVars, numClauses, clauses


