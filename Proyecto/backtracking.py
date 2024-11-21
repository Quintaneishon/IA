from simulated_annealing import init_plan


def backtracking(schedule, iteration_limit=100000):
    best_plan = None
    best_cost = float('inf')
    best_penalties = None
    iteration_count = 0

    def assign_roles(day, current_plan):
        nonlocal best_plan, best_cost, best_penalties, iteration_count

        if iteration_count >= iteration_limit:
            raise Exception("Limit reached")

        if day > schedule.n_days:
            current_cost, current_penalties = schedule.calculate_cost(current_plan)
            if current_cost < best_cost:
                best_plan = current_plan
                best_cost = current_cost
                best_penalties = current_penalties
            return

        if current_plan is None:
            current_plan = {d: {role: None for role in schedule.roles} for d in range(1, schedule.n_days + 1)}

        assigned_persons = set()
        for role in schedule.roles:
            for person in range(schedule.persons):
                if person in assigned_persons:
                    continue  # Skip assigning the same person to multiple roles on the same day

                current_plan[day][role] = person
                iteration_count += 1

                # Recursively assign roles for next day
                assign_roles(day + 1, current_plan)

                # Backtracking step
                current_plan[day][role] = None

    # Start the backtracking algorithm from day 1

    assign_roles(1, init_plan(schedule))

    return best_plan, best_cost, best_penalties
