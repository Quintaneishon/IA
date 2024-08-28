import heapq


def graph_search(problem, heuristic):
    fringe = []  # Cola de prioridad
    closed = set()  # Set para estados explorados
    parent = {}  # Dictionario para guardar el padre de cada nodo
    heuristic_cost = {}  # Diccionario para llevar el costo de la heuristica

    # Empezamos con el estado inicial
    start_node = make_node(problem['initial_state'])
    start_state = state(start_node)

    # Inicializamos la cola de prioridad con el nodo inicial
    initial_priority = 0 if heuristic is None or not heuristic else heuristic[start_state]
    heapq.heappush(fringe, (initial_priority, start_node))  # (prioridad, nodo)
    parent[start_state] = None  # El estado inicial no tiene padre
    heuristic_cost[start_state] = 0  # el costo del estado inicial es 0

    while fringe:
        _, node = heapq.heappop(fringe)
        current_state = state(node)

        if goal_test(problem, current_state):
            return reconstruct_path(parent, current_state)

        if current_state not in closed:
            closed.add(current_state)

            for child_node, transition_cost in expand(current_state, problem):
                child_state = state(child_node)
                new_cost = heuristic_cost[current_state] + transition_cost

                if child_state not in closed and (
                        child_state not in heuristic_cost or new_cost < heuristic_cost[child_state]):
                    heuristic_cost[child_state] = new_cost
                    priority = new_cost if heuristic is None or not heuristic else new_cost + heuristic[child_state]
                    heapq.heappush(fringe, (priority, child_node))
                    parent[child_state] = current_state

    return None  # No solution found


def make_node(state):
    return {'state': state}


def state(node):
    return node['state']


def initial_state(problem):
    return problem['initial_state']


def goal_test(problem, state):
    return state == problem['goal_state']


def expand(state, problem):
    # Generar nodos hijos con sus respectivos costos de transición
    return [(make_node(s), cost) for s, cost in problem['transitions'].get(state, {}).items()]


def reconstruct_path(parent, goal_state):
    path = []
    current_state = goal_state
    while current_state is not None:
        path.append(current_state)
        current_state = parent.get(current_state)
    return path[::-1]  # Invertir para obtener el camino desde el inicio hasta el final


if __name__ == '__main__':
    # ejemplo basico
    problem = {
        'initial_state': 'A',
        'goal_state': 'E',
        'transitions': {
            'A': {'B': 2, 'C': 1},
            'C': {'A': 1, 'D': 5},
            'D': {'C': 5, 'E': 2, 'F': 1},
            'E': {'D': 2},
            'F': {'D': 1}
        }
    }

    heuristic = {}

    solution_path = graph_search(problem, heuristic)

    if solution_path:
        print(f"Solución encontrada: {solution_path}")
    else:
        print("No se encontró solución")

    # Arad a Bucarest
    problem = {
        'initial_state': 'arad',
        'goal_state': 'bucharest',
        'transitions': {
            'arad': {'zerind': 75, 'timisora': 118, 'sibiu': 140},
            'zerind': {'oradea': 71, 'arad': 75},
            'timisora': {'arad': 118, 'lugoj': 111},
            'sibiu': {'arad': 140, 'oradea': 151, 'rimnicu vilcea': 80, 'fagaras': 99},
            'oradea': {'zerind': 71, 'sibiu': 151},
            'lugoj': {'timisora': 111, 'mehadia': 70},
            'rimnicu vilcea': {'sibiu': 80, 'pitesti': 97, 'cralova': 138},
            'fagaras': {'sibiu': 99, 'bucharest': 211},
            'mehadia': {'lugoj': 70, 'dobreta': 75},
            'dobreta': {'mehadia': 75, 'cralova': 120},
            'cralova': {'rimnicu vilcea': 146, 'pitesti': 138},
            'pitesti': {'rimnicu vilcea': 97, 'cralova': 138, 'bucharest': 101},
            'bucharest': {'fagaras': 211, 'pitesti': 101, 'giurgiu': 90, 'urziceni': 85},
            'urziceni': {'bucharest': 85, 'vaslui': 142, 'hirsova': 98},
            'vaslui': {'lasi': 92, 'ursiceni': 142},
            'lasi': {'vasliu': 92, 'neamt': 87},
            'neamt': {'lasi': 87},
            'hirsova': {'urziceni': 98, 'eforie': 86},
            'eforie': {'hirsova': 86},
            'giurgiu': {'bucharest': 90},
        }
    }

    heuristic = {
        'arad': 366,
        'bucharest': 0,
        'cralova': 160,
        'dobreta': 242,
        'eforie': 161,
        'fagaras': 178,
        'giurgiu': 77,
        'hirsova': 151,
        'lasi': 226,
        'lugoj': 244,
        'mehadia': 241,
        'neamt': 234,
        'oradea': 380,
        'pitesti': 98,
        'rimnicu vilcea': 193,
        'sibiu': 253,
        'timisora': 329,
        'urziceni': 80,
        'vaslui': 199,
        'zerind': 374,
    }

    solution_path = graph_search(problem, heuristic)

    if solution_path:
        print(f"Solución encontrada: {solution_path}")
    else:
        print("No se encontró solución")
