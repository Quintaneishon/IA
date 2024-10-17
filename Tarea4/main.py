from collections import defaultdict


class BayesNet:
    def __init__(self):
        self.vars = {}
        self.parents = {}
        self.probabilities = {}

    def add_variable(self, var, domain):
        self.vars[var] = Node(var, domain, {}, {})

    def add_probability(self, var, parents, probabilities):
        self.parents[var] = parents
        self.probabilities[var] = probabilities


class Node:
    def __init__(self, name, domain, parents, probabilities):
        self.name = name
        self.domain = domain
        self.parents = parents
        self.probabilities = probabilities


def load_bif(file_path):
    bn = BayesNet()
    with open(file_path, 'r') as f:
        lines = f.readlines()

    current_var = None
    reading_prob = False
    prob_parents = []
    prob_table = {}

    for line in lines:
        line = line.strip()
        if line.startswith("variable"):
            var_name = line.split()[1]
            current_var = var_name
        elif line.startswith("type discrete"):
            domain = line.split('{')[1].split('}')[0].split(',')
            domain = [d.strip() for d in domain]
            bn.add_variable(current_var, domain)
        elif line.startswith("probability"):
            parts = line.split('|')
            var_name = parts[0].split('(')[1].split(')')[0].strip()
            current_var = var_name
            if len(parts) > 1:
                prob_parents = parts[1].split(')')[0].strip().split(', ')
            else:
                prob_parents = []
            reading_prob = True
        elif reading_prob and line.endswith(';'):
            values = line.replace(';', '').replace('table', '').split(',')
            if '(' in line:
                key = tuple(map(lambda x: x, line.split(')')[0].replace('(', '').split(', ')))
                values = list(map(float, line.replace(";", "").split(')')[1].strip().split(', ')))
                prob_table[key] = {'True': values[0], 'False': values[1]}
            else:
                values = [v.strip() for v in values]
                values = list(map(float, values))
                prob_table[()] = {'True': values[0], 'False': values[1]}
            bn.add_probability(current_var, prob_parents, prob_table)
        elif line.startswith('}'):
            prob_table = {}
            reading_prob = False

    for var in bn.vars:
        bn.vars[var].parents = bn.parents[var]
        bn.vars[var].probabilities = bn.probabilities[var]

    return bn
def enumeration_ask(X, e, bn):
    Q = defaultdict(float)
    for xi in bn.vars[X].domain:
        Q[xi] = enumerate_all(list(bn.vars.keys()), extend(e, {X: xi}))
    return normalize(Q)


def enumerate_all(var_list, e):
    if not var_list:
        return 1.0
    Y = var_list[0]
    if Y in e:
        return P(Y, e) * enumerate_all(var_list[1:], e)
    else:
        return sum(P(Y, extend(e, {Y: y})) * enumerate_all(var_list[1:], extend(e, {Y: y})) for y in bn.vars[Y].domain)


def extend(e, changes):
    new_e = e.copy()
    new_e.update(changes)
    return new_e


def P(var, e):
    parent_values = tuple(e[parent] for parent in bn.parents[var])
    return bn.probabilities[var][parent_values][e[var]]


def normalize(Q):
    total = sum(Q.values())
    return {k: v / total for k, v in Q.items()}


def is_d_separated(bn, X, Y, evidence):
    def find_paths(node, goal, visited):
        if node == goal:
            return [[goal]]
        paths = []
        visited.add(node)
        for parent in bn.parents.get(node, []):
            if parent not in visited:
                subpaths = find_paths(parent, goal, visited)
                for path in subpaths:
                    paths.append([node] + path)
        for child in (child for child, parents in bn.parents.items() if node in parents):
            if child not in visited:
                subpaths = find_paths(child, goal, visited)
                for path in subpaths:
                    paths.append([node] + path)
        visited.remove(node)
        return paths

    def path_blocked(path, evidence):
        for i in range(len(path) - 1):
            node = path[i]
            next_node = path[i+1]
            if next_node in bn.parents.get(node, []):
                if node in evidence or any(p not in evidence for p in bn.parents.get(node, [])):
                    continue
            elif node in bn.parents.get(next_node, []):
                if next_node not in evidence and not any(p in evidence for p in bn.parents.get(next_node, [])):
                    continue
            else:
                return True
        return False

    paths = find_paths(X, Y, set())
    for path in paths:
        if not path_blocked(path, evidence):
            return False
    return True


if __name__ == '__main__':
    arch = input("Ingrese el nombre del archivo para construir la red bayesiana: ").strip()
    bn = load_bif(arch)
    while True:
        consulta = input("Ingrese su consulta (P para probabilidad, D-S para D-Separated): ").strip()
        if consulta.startswith("P"):
            parts = consulta.split("|")
            query_var = parts[0][2:].strip()
            evidence = {}
            if len(parts) > 1:
                evidence_parts = parts[1].replace(")", "").strip().split(",")
                for ep in evidence_parts:
                    var, val = ep.split("=")
                    evidence[var.strip()] = 'True' if val.strip() in ['true', 'TRUE', 'True'] else 'False'
            result = enumeration_ask(query_var, evidence, bn)
            print(f"Resultado de {consulta}: {result}")

            variables = parts[1].split(",")
            variables = [v.strip() for v in variables]
            for v in variables:
                d_separated = is_d_separated(bn, query_var, v, evidence)
                print(f"D-separated ({query_var} y {v} dado {evidence}): {d_separated}")
        else:
            print("Consulta no reconocida. Use 'P' para probabilidad o 'D-S' para D-Separated.")
