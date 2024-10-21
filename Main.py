# File: Main.py
# Description: Read and parse the cnf file. Run the solvers. Collect and display the data.
import os
import time
import matplotlib.pyplot as plt
import Solvers

CNF_Folder = 'CNF Formulas'
Hard_CNF_Folder = 'HARD CNF Formulas'
Sample_CNF_Folder = 'Sample'
   
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
                elif line.startswith("%") or line.startswith("0"):
                    break
                else:
                    clause = list(map(int, line.split()[:-1]))
                    clauses.append(clause)

        Solver = Solvers.Solvers(num_vars, num_clauses, clauses)

        print(" ")
        print(" ")
        print(" ")

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

        print("-"*40)

        print("Running DPLL...")
        result, assignment = Solver.DPLL()
        if result:
            print(f"Result for {cnf_filename}: Satisfiable!")
            print(f"Assignment: {assignment}")
        else:
            print(f"Result for {cnf_filename}: Unsatisfiable.")

Test1_Path = 'Sample/Test1.cnf'
Test2_Path = 'Sample/Test2.cnf'
CNF1_Path = 'CNF Formulas/uf20-0165.cnf'
CNF2_Path = 'CNF Formulas/uf20-0162.cnf'

def graph_parse(file):
    """Parse a CNF file and generate the corresponding graph."""
    cnf_filename = os.path.basename(file)
    num_vars, num_clauses, clauses = 0, 0, []

    # Read and parse the CNF file
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('c'):
                continue
            elif line.startswith('p cnf'):
                parts = line.split()
                num_vars = int(parts[2])
                num_clauses = int(parts[3])
            elif line.startswith('%') or line.startswith('0'):
                break
            else:
                clause = list(map(int, line.split()[:-1]))
                clauses.append(clause)

    # Initialize the solver with the parsed CNF data
    Solver = Solvers.Solvers(num_vars, num_clauses, clauses)

    # Run the algorithms and collect data
    run_algorithms(Solver, cnf_filename)


def run_algorithms(Solver, cnf_filename):
    """Run the solvers and collect data."""
    print(f"\nRunning algorithms for {cnf_filename}...\n")

    # Data collection
    gsat_results = []
    sim_annealing_results = []
    dpll_results = []

    # Run GSAT 10 times
    for i in range(10):
        start_time = time.time()
        result, assignment = Solver.G_SAT(maxFlips=10000)
        elapsed_time = time.time() - start_time
        satisfied_clauses = count_satisfied_clauses(Solver.clauses, assignment) if result else 0
        gsat_results.append((elapsed_time, satisfied_clauses))

    # Run Simulated Annealing 10 times
    for i in range(10):
        start_time = time.time()
        result, assignment = Solver.Simulated_Annealing(maxIters=100000)
        elapsed_time = time.time() - start_time
        satisfied_clauses = count_satisfied_clauses(Solver.clauses, assignment) if result else 0
        sim_annealing_results.append((elapsed_time, satisfied_clauses))

    # Run DPLL once
    start_time = time.time()
    result, assignment = Solver.DPLL()
    elapsed_time = time.time() - start_time
    dpll_results.append((elapsed_time, result))

    # Print the results
    print(f"GSAT Results (10 runs): {gsat_results}")
    print(f"Simulated Annealing Results (10 runs): {sim_annealing_results}")
    print(f"DPLL Results: {dpll_results}")

    # Plot the results
    plot_results(cnf_filename, gsat_results, sim_annealing_results, dpll_results)


def count_satisfied_clauses(clauses, assignment):
    """Count the number of satisfied clauses given the assignment."""
    satisfied_count = 0
    for clause in clauses:
        for literal in clause:
            var = abs(literal) - 1
            if (literal > 0 and assignment[var]) or (literal < 0 and not assignment[var]):
                satisfied_count += 1
                break
    return satisfied_count


def plot_results(cnf_filename, gsat_results, sim_annealing_results, dpll_results):
    """Plot the results as required."""
    # Extract data for GSAT and Simulated Annealing
    gsat_times, gsat_satisfied = zip(*gsat_results)
    sa_times, sa_satisfied = zip(*sim_annealing_results)
    dpll_time, _ = dpll_results[0]

    # Combined Plot for CPU Time vs Clauses Satisfied and Average CPU Time
    plt.figure(figsize=(10, 6))

    # Scatter Plot - CPU Time vs Clauses Satisfied
    plt.subplot(2, 1, 1)
    plt.scatter(gsat_times, gsat_satisfied, color='blue', label='GSAT (Hill Climbing)')
    plt.scatter(sa_times, sa_satisfied, color='green', label='Simulated Annealing')
    plt.xlabel("CPU Time (seconds)")
    plt.ylabel("Clauses Satisfied")
    plt.title(f"CPU Time vs Clauses Satisfied for {cnf_filename}")
    plt.legend()

    # Bar Plot - Average CPU Time
    plt.subplot(2, 1, 2)
    plt.bar(['GSAT (Avg)', 'Simulated Annealing (Avg)', 'DPLL'], [sum(gsat_times) / 10, sum(sa_times) / 10, dpll_time],
            color=['blue', 'green', 'red'])
    plt.ylabel("CPU Time (seconds)")
    plt.title(f"Formula {cnf_filename} - Average CPU Time per Algorithm")

    # Save the figure
    plt.tight_layout()
    plt.savefig(f"combined_results_{cnf_filename}.png")
    plt.close()
def main():



    # CNF Formulas
    graph_parse(Test1_Path)
    graph_parse(Test2_Path)

    graph_parse(CNF1_Path)
    graph_parse(CNF2_Path)

    print("Sample")
    parse(Sample_CNF_Folder)
    print("Standard")
    parse(CNF_Folder)
    print("Hard")
    parse(Hard_CNF_Folder)

if __name__ == "__main__":
    main()




