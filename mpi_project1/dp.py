import time

def pure_literals(clauses):
    counter = {}
    for clause in clauses:
        for literal in clause:
            counter[literal] = counter.get(literal, 0) + 1
    return {lit for lit in counter if -lit not in counter}

def unit_propagate(clauses):
    unit_clauses = {next(iter(c)) for c in clauses if len(c) == 1}
    while unit_clauses:
        literal = unit_clauses.pop()
        new_clauses = set()
        for clause in clauses:
            if literal in clause:
                continue
            if -literal in clause:
                new_clause = set(clause)
                new_clause.remove(-literal)
                if not new_clause:
                    return None
                new_clauses.add(frozenset(new_clause))
            else:
                new_clauses.add(clause)
        clauses = new_clauses
        unit_clauses |= {next(iter(c)) for c in clauses if len(c) == 1}
    return clauses

def eliminate_pure_literals(clauses):
    pure = pure_literals(clauses)
    new_clauses = {clause for clause in clauses if not any(lit in pure for lit in clause)}
    return new_clauses

def resolve(ci, cj, literal):
    resolvent = (ci - {literal}) | (cj - {-literal})
    if any(lit in resolvent and -lit in resolvent for lit in resolvent):
        return None
    return frozenset(resolvent)

def dp_algorithm(clauses):
    clauses = set(frozenset(c) for c in clauses)
    resolved_pairs = set()

    while True:
        clauses = unit_propagate(clauses)
        if clauses is None:
            return False
        if not clauses:
            return True

        clauses = eliminate_pure_literals(clauses)
        if not clauses:
            return True

        some_clause = min(clauses, key=len)
        literal = next(iter(some_clause))

        pos_clauses = {c for c in clauses if literal in c}
        neg_clauses = {c for c in clauses if -literal in c}
        others = {c for c in clauses if literal not in c and -literal not in c}

        resolvents = set()
        for ci in pos_clauses:
            for cj in neg_clauses:
                pair_id = tuple(sorted([id(ci), id(cj)]))
                if pair_id in resolved_pairs:
                    continue
                resolved_pairs.add(pair_id)
                resolvent = resolve(ci, cj, literal)
                if resolvent is None:
                    continue
                if not resolvent:
                    return False
                resolvents.add(resolvent)

        if not resolvents:
            return True

        clauses = others.union(resolvents)

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
    result = dp_algorithm(clauses)
    end_time = time.time()

    print("Satisfiable?", result)
    print(f"Time taken: {end_time - start_time:.4f} seconds")


