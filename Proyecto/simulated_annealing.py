import math
import random

# Parámetros del recocido simulado
INIT_TEMP = 10000
COOLING = 0.9999
MIN_TEMP = 1


# Inicializar un horario aleatorio
def init_plan(schedule):
    plan = {
        day: {role: random.randint(0, schedule.persons - 1) for role in schedule.roles}
        for day in range(1, schedule.n_days + 1)
    }
    return plan


# Generar un neighbor del horario actual
def generate_neighbor(schedule, plan):
    new_plan = {day: roles_day.copy() for day, roles_day in plan.items()}
    day = random.randint(1, schedule.n_days)
    role = random.choice(list(schedule.roles.keys()))
    person = random.randint(0, schedule.persons - 1)
    new_plan[day][role] = person
    return new_plan


# Algoritmo de recocido simulado
def simulated_annealing(schedule):
    actual_plan = init_plan(schedule)
    actual_cost, _ = schedule.calculate_cost(actual_plan)
    temp = INIT_TEMP

    best_plan = actual_plan
    best_cost = actual_cost
    best_penalties = None

    while temp > MIN_TEMP:
        neighbor = generate_neighbor(schedule, actual_plan)
        neighbor_cost, neighbor_penalties = schedule.calculate_cost(neighbor)

        delta = neighbor_cost - actual_cost
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temp):
            actual_plan = neighbor
            actual_cost = neighbor_cost

        if actual_cost < best_cost:
            best_plan = actual_plan
            best_cost = actual_cost
            best_penalties = neighbor_penalties

        temp *= COOLING

    return best_plan, best_cost, best_penalties
