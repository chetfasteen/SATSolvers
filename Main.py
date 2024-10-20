# File: Main.py
# Description: Read and parse the cnf file. Run the solvers. Collect and display the data.

import os
import Solvers

CNF_Folder = 'CNF Formulas'
Hard_CNF_Folder = 'HARD CNF Formulas'
Sample_CNF_Folder = 'TEST CNF'

def parse(folder_path):
    all_files = os.listdir(folder_path)
    cnf_files = []

    for f in all_files:
        if f.endswith('.cnf'):
            cnf_files.append(f)

    cnf_file_paths = []
    for cnf_file in cnf_files:
        full_path = os.path.join(folder_path, cnf_file)
        cnf_file_paths.append(full_path)

    for cnf_path in cnf_file_paths:
        cnf_filename = os.path.basename(cnf_path)
        print(f"Processing file: {cnf_filename}")

        num_vars = 0
        num_clauses = 0
        clauses = []
        with open(cnf_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('c'):
                    continue
                elif line.startswith('p cnf'):
                    parts = line.split()
                    num_vars = int(parts[2])
                    num_clauses = int(parts[3])
                else:
                    clause = list(map(int, line.split()[:-1]))
                    clauses.append(clause)

        Solver = Solvers.Solvers(num_vars, num_clauses, clauses)

        print("Running GSAT...")
        result, assignment = Solver.G_SAT()
        if result:
            print(f"Result for {cnf_filename}: Satisfiable!")
            print(f"Assignment: {assignment}")
        else:
            print(f"Result for {cnf_filename}: Unsatisfiable.")

        print("-"*40)

        print("Running Simulated Annealing...")
        result, assignment = Solver.Simulated_Annealing()
        if result:
            print(f"Result for {cnf_filename}: Satisfiable!")
            print(f"Assignement: {assignment}")
        else:
            print(f"Result for {cnf_filename}: Unsatisfiable.")

    return

def main():
    parse(Sample_CNF_Folder)
   # parse(CNF_Folder)
    #parse(Hard_CNF_Folder)

if __name__ == "__main__":
    main()





