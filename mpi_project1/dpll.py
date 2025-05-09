import time

def dpll(clauses, assignment=set()):
    clauses = set(clauses)

    clauses, assignment = unit_propagate(clauses, assignment)
    if clauses is None:
        return False, None
    if not clauses:
        return True, assignment

    clauses, assignment = eliminate_pure_literals(clauses, assignment)
    if not clauses:
        return True, assignment

    literal = choose_literal(clauses)

    new_clauses = simplify(clauses, literal)
    if new_clauses is not None:
        sat, new_assignment = dpll(new_clauses, assignment | {literal})
        if sat:
            return True, new_assignment

    new_clauses = simplify(clauses, -literal)
    if new_clauses is not None:
        sat, new_assignment = dpll(new_clauses, assignment | {-literal})
        if sat:
            return True, new_assignment

    return False, None

def choose_literal(clauses):
    smallest_clause = min(clauses, key=len)
    return next(iter(smallest_clause))

def simplify(clauses, literal):
    new_clauses = set()
    for clause in clauses:
        if literal in clause:
            continue
        if -literal in clause:
            new_clause = clause - {-literal}
            if not new_clause:
                return None
            new_clauses.add(new_clause)
        else:
            new_clauses.add(clause)
    return new_clauses

def unit_propagate(clauses, assignment):
    clauses = set(clauses)
    unit_clauses = {next(iter(c)) for c in clauses if len(c) == 1}

    while unit_clauses:
        literal = unit_clauses.pop()
        assignment |= {literal}
        new_clauses = set()
        for clause in clauses:
            if literal in clause:
                continue
            if -literal in clause:
                new_clause = clause - {-literal}
                if not new_clause:
                    return None, None
                new_clauses.add(new_clause)
            else:
                new_clauses.add(clause)
        clauses = new_clauses
        unit_clauses |= {next(iter(c)) for c in clauses if len(c) == 1}
    return clauses, assignment

def eliminate_pure_literals(clauses, assignment):
    literal_counts = {}
    for clause in clauses:
        for literal in clause:
            literal_counts[literal] = literal_counts.get(literal, 0) + 1

    pure_literals = {lit for lit in literal_counts if -lit not in literal_counts}
    if not pure_literals:
        return clauses, assignment

    assignment |= pure_literals
    new_clauses = {clause for clause in clauses if not any(lit in pure_literals for lit in clause)}
    return new_clauses, assignment

def parse_dimacs_cnf(file_path):
    clauses = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '' or line.startswith('c') or line.startswith('p'):
                continue
            literals = [int(x) for x in line.split() if x != '0']
            if literals:
                clauses.append(frozenset(literals))
    return clauses

if __name__ == "__main__":
    file_number = input("Enter the test case number (1-11): ")
    try:
        num = int(file_number)
        if 1 <= num <= 11:
            file_path = f"input{num}.cnf"
            clauses = parse_dimacs_cnf(file_path)
            # Now run your SAT solver here
        else:
            print("Please enter a number between 1 and 11.")
    except ValueError:
        print("Invalid input. Please enter a number.")

    start_time = time.time()
    sat, assignment = dpll(clauses)
    end_time = time.time()

    print("Satisfiable?", sat)
    if sat:
        print("Assignment (literals set to True):", assignment)
    print(f"Time taken: {end_time - start_time:.4f} seconds")

