
import time

def resolve(ci, cj):
    resolvents = set()
    for literal in ci:
        if -literal in cj:
            resolvent = (ci - {literal}) | (cj - {-literal})
            resolvents.add(frozenset(resolvent))
    return resolvents


def parse_dimacs_cnf(file_path):
    clauses = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '' or line.startswith('c') or line.startswith('p'):
                continue
            literals = [int(x) for x in line.split() if x != '0']
            if literals:
                clauses.append(set(literals))
    return clauses


def resolution_algorithm(clauses):
    clauses = set(frozenset(clause) for clause in clauses)
    new = set()
    processed_pairs = set()

    while True:
        for ci in clauses:
            for cj in clauses:
                if ci == cj:
                    continue
                pair = tuple(sorted([ci, cj], key=id))
                if pair in processed_pairs:
                    continue
                processed_pairs.add(pair)

                resolvents = resolve(ci, cj)
                if frozenset() in resolvents:
                    return False
                new |= resolvents

        if new.issubset(clauses):
            return True

        clauses |= new


if __name__ == "__main__":
    file_number = input("Enter the test case number (1-11): ")
    try:
        num = int(file_number)
        if 1 <= num <= 11:
            file_path = f"input{num}.cnf"
            clauses = parse_dimacs_cnf(file_path)
        else:
            print("Please enter a number between 1 and 11.")
    except ValueError:
        print("Invalid input. Please enter a number.")


    start_time = time.time()
    result = resolution_algorithm(clauses)
    end_time = time.time()

    print("Satisfiable?", result)
    print(f"Time taken: {end_time - start_time:.4f} seconds")
