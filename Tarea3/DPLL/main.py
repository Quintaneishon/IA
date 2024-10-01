import requests
import tarfile
import os

def load_dimacs(filename):
    clauses = []
    print(f"Filename received: {filename}")
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('c') or line.startswith('p'):
                continue
            clause = list(map(int, line.strip().split()))[:-1]  # Ignorar el 0 al final de cada línea porque es el delimitador
            clauses.append(clause)

    symbols = get_symbols_from_clauses(clauses)
    return clauses, symbols


def get_symbols_from_clauses(clauses):
    symbols = set()
    for clause in clauses:
        for literal in clause:
            symbols.add(abs(literal))  # El valor absoluto del literal
    return list(symbols)


def dpll(clauses, symbols, model):
    if all_clause_true(clauses, model):
        return True

    if any_clause_false(clauses, model):
        return False

    P, value = find_unit_clause(clauses, model)
    if P is not None:
        symbols.remove(P)
        model[P] = value
        return dpll(clauses, symbols[:], model)

    P = symbols.pop(0)

    model[P] = True
    if dpll(clauses, symbols[:], model):
        return True

    model[P] = False
    return dpll(clauses, symbols[:], model)


def all_clause_true(clauses, model):
    for clause in clauses:
        if not any(literal in model and model[literal] == True for literal in clause):
            return False
    return True


def any_clause_false(clauses, model):
    for clause in clauses:
        if all((literal in model and model[literal] == False) or (-literal in model and model[-literal] == False) for
               literal in clause):
            return True
    return False


def find_unit_clause(clauses, model):
    for clause in clauses:
        unassigned = [literal for literal in clause if literal not in model and -literal not in model]
        if len(unassigned) == 1:
            P = unassigned[0]
            value = True if P > 0 else False
            return abs(P), value
    return None, None


def dpll_satisfiable(clauses, symbols):
    model = {}
    return dpll(clauses, symbols, model)

def download_and_extract_tar(url, dest_dir):
    response = requests.get(url)
    tar_path = os.path.join(dest_dir, "CBS_k3_n100_m403_b10.tar.gz")

    with open(tar_path, 'wb') as f:
        f.write(response.content)

    with tarfile.open(tar_path, 'r:gz') as tar:
        tar.extractall(path=dest_dir)

    os.remove(tar_path)

    # Instancia 37
    target_file = "CBS_k3_n100_m403_b10_37.cnf"
    extracted_file_path = os.path.join(dest_dir, target_file)

    # Lógica para eliminar todos los archivos excepto CBS_k3_n100_m403_b10_37.cnf
    for file_name in os.listdir(dest_dir):
        file_path = os.path.join(dest_dir, file_name)
        if file_name != target_file and os.path.isfile(file_path) and file_name != "main.py":
            os.remove(file_path)

    return extracted_file_path

def load_dimacs_from_url(url, dest_dir):
    cnf_file = download_and_extract_tar(url, dest_dir)
    return load_dimacs(cnf_file)

if __name__ == '__main__':
    url = "https://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/CBS/CBS_k3_n100_m403_b10.tar.gz"

    clauses, symbols = load_dimacs_from_url(url, ".")
    if dpll_satisfiable(clauses, symbols):
        print("La fórmula es satisfiable.")
    else:
        print("La fórmula no es satisfiable.")
