import json
from backtracking import backtracking
from schedule import Schedule
from simulated_annealing import simulated_annealing


def load_config(file_path):
    print(f"loading {file_path}")
    with open(file_path, 'r') as file:
        return json.load(file)

# Mostrar el horario
def show_plan(schedule, best_plan, best_cost, best_penalties):
    for day in range(1, schedule.n_days + 1):
        date = schedule.month_days[day - 1].strftime('%d-%m-%Y')
        print(f"Día {date}:")
        for role, schedule_role in schedule.roles.items():
            person = best_plan[day][role]
            start, end = schedule_role
            print(f"  {role.capitalize()}: Persona {person + 1} (Horario: {start}:00 - {end}:00)")
        print()
    print(f"\nCosto total óptimo: {best_cost}")
    print("Detalle de penalizaciones:")
    for key, value in best_penalties.items():
        print(f"  - {key}: {value} penalización(es)")


def solve_schedule(config):
    num_personas = config['num_personas']
    max_dias_mes = config['max_dias_mes']
    max_dias_semana = config['max_dias_semana']
    dias_descanso_cambio_turno = config['dias_descanso_cambio_turno']
    roles = {k: tuple(v) for k, v in config['roles'].items()}
    mes = config['mes']
    ano = config['ano']

    s = Schedule(num_personas, max_dias_mes, max_dias_semana, dias_descanso_cambio_turno, roles, ano, mes)

    # If this configuration has specific animal feeding logic
    if 'alimentacion_animales' in config:
        alimentacion_animales = config['alimentacion_animales']

        def no_alimentar_animales(schedule, day, plan):
            for animal, horas in alimentacion_animales.items():
                for hora in horas:
                    if not any(hora in range(schedule.roles[rol][0], (schedule.roles[rol][1] or 24)) for rol in
                               schedule.roles):
                        return True
            return False

        custom_penalties = {
            'Animal no alimentado': [20, no_alimentar_animales]
        }
        s.custom_penalties = custom_penalties  # Add custom penalties to schedule

    try:
        print("Trying Backtracking")
        best_plan, best_cost, best_penalties = backtracking(s)
    except:
        print("Trying Simulated Annealing")
        best_plan, best_cost, best_penalties = simulated_annealing(s)

    show_plan(s, best_plan, best_cost, best_penalties)


if __name__ == '__main__':
    # Execute Energia case
    energia_config = load_config('energia_config.json')
    solve_schedule(energia_config)

    # Execute Granja case
    granja_config = load_config('granja_config.json')
    solve_schedule(granja_config)