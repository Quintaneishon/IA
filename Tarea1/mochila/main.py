import heapq
import csv
from tqdm import tqdm


def graph_search(problem, heuristic=None):
    fringe = []  # Priority queue for A*
    closed = set()  # Set for explored states
    parent = {}  # Dictionary to track the parents of each node
    cost_so_far = {}  # Dictionary to track the cost so far (weight_so_far)

    # Start with the initial state
    start_node = make_node((0, 0, 0))  # (index, current_weight, current_value)
    start_state = state(start_node)

    # Initialize the priority queue with the start node
    initial_priority = heuristic(start_state, problem) if heuristic else 0
    heapq.heappush(fringe, (initial_priority, start_node))
    parent[start_state] = None  # The initial state has no parent
    cost_so_far[start_state] = 0  # Weight to reach the initial state is 0

    best_value = 0
    pbar = tqdm(total=problem['capacity'], desc="Mochila", unit="units")

    while fringe:
        _, node = heapq.heappop(fringe)
        current_state = state(node)
        index, current_weight, current_value = current_state

        # Update the progress bar
        pbar.n = current_weight  # Update the current progress
        pbar.refresh()

        if index == len(problem['values']):
            best_value = max(best_value, current_value)
            continue

        # Option 1: Don't take the current item
        next_state = (index + 1, current_weight, current_value)
        next_priority = -next_state[2] + (heuristic(next_state, problem) if heuristic else 0)
        heapq.heappush(fringe, (next_priority, make_node(next_state)))
        parent[next_state] = current_state

        # Option 2: Take the current item (if it doesn't exceed capacity)
        item_weight = problem['weights'][index]
        if current_weight + item_weight <= problem['capacity']:
            new_weight = current_weight + item_weight
            new_value = current_value + problem['values'][index]
            next_state = (index + 1, new_weight, new_value)
            next_priority = -next_state[2] + (heuristic(next_state, problem) if heuristic else 0)
            heapq.heappush(fringe, (next_priority, make_node(next_state)))
            parent[next_state] = current_state

            best_value = max(best_value, new_value)

    pbar.close()
    return best_value


def make_node(state):
    return {'state': state}


def state(node):
    return node['state']


def goal_test(problem, state):
    return state[1] <= problem['capacity']  # Ensure weight does not exceed capacity

def mochila_heuristica(state, problem):
    # Desempaquetar el estado actual
    index, current_weight, current_value = state

    # Calcular la capacidad restante
    remaining_capacity = problem['capacity'] - current_weight

    if remaining_capacity <= 0 or index == len(problem['values']):
        return 0

    # Obtener los elementos restantes
    remaining_items = [(problem['values'][i], problem['weights'][i])
                       for i in range(index, len(problem['values']))]

    # Ordenar los elementos restantes por su valor/peso en orden descendente
    remaining_items.sort(key=lambda x: x[0] / x[1], reverse=True)

    estimated_value = 0
    for value, weight in remaining_items:
        if weight <= remaining_capacity:
            # Si el artículo cabe completamente, añadir todo su valor
            estimated_value += value
            remaining_capacity -= weight
        else:
            # Si el artículo no cabe completamente, añadir la fracción que cabe
            estimated_value += value * (remaining_capacity / weight)
            break

    return estimated_value

def mochila_heuristica_optimizada(state, problem):
    # Desempaquetar el estado actual
    index, current_weight, current_value = state

    # Calcular la capacidad restante
    remaining_capacity = problem['capacity'] - current_weight

    if remaining_capacity <= 0 or index == len(problem['values']):
        return 0

    # Obtener los elementos restantes
    remaining_items = [(problem['values'][i], problem['weights'][i])
                       for i in range(index, len(problem['values']))]

    # Ordenar los elementos restantes por su valor/peso en orden descendente
    remaining_items.sort(key=lambda x: x[0] / x[1], reverse=True)

    estimated_value = current_value
    for value, weight in remaining_items:
        if weight <= remaining_capacity:
            # Si el artículo cabe completamente, añadir todo su valor
            estimated_value += value
            remaining_capacity -= weight
        else:
            # Si el artículo no cabe completamente, añadir la fracción que cabe
            estimated_value += value * (remaining_capacity / weight)
            break

    return estimated_value - current_value

if __name__ == '__main__':
    problem = {
        'values': [1945, 321, 2945, 4136, 1107, 1022, 1101, 2890, 962, 1060,
                   805, 689, 1513, 3878, 13504, 1865, 667, 1833, 16553],
        'weights': [4990, 1142, 7390, 10372, 3114, 2744, 3102, 7280, 2624, 3020,
                    2310, 2078, 3926, 9656, 32708, 4830, 2034, 4766, 40006],
        'capacity': 31181
    }

    max_value = graph_search(problem, heuristic=mochila_heuristica)

    print(f"Valor máximo posible en la mochila: {max_value}")

    # 1K
    with open('ks_10000_0.csv', 'r') as archivo:
        lector = csv.reader(archivo, delimiter=' ')

        filas = list(lector)[:]

    values = [int(fila[0]) for fila in filas]
    weights = [int(fila[1]) for fila in filas]

    problem = {
        'values': values,
        'weights': weights,
        'capacity': 1000000
    }

    max_value = graph_search(problem, heuristic=mochila_heuristica_optimizada)

    print(f"Valor máximo posible en la mochila: {max_value}")

