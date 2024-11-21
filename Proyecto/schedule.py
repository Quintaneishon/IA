import calendar
from datetime import datetime


class Schedule:
    def __init__(self, persons, max_month_days, max_week_days, rest_days, roles, year, month, custom_penalties=None):
        # número de personas disponibles
        self.persons = persons
        # Parámetros de restricciones personalizadas
        self.max_month_days = max_month_days
        self.max_week_days = max_week_days
        self.rest_days = rest_days
        # Datos del horario y restricciones de turnos
        self.roles = roles
        # Variables calculadas dependiendo el mes y año
        self.n_days = calendar.monthrange(year, month)[1]
        self.month_days = [datetime(2024, 10, day) for day in range(1, self.n_days + 1)]
        if custom_penalties is None:
            self.custom_penalties = {}
        else:
            self.custom_penalties = custom_penalties

    def calculate_cost(self, plan):
        cost = 0
        work_days = {person: 0 for person in range(self.persons)}
        last_assignation = {person: None for person in range(self.persons)}

        penalties = {
            'Exceso de días trabajados en el mes': 0,
            'Descanso insuficiente entre turnos y otros roles': 0,
            'Exceso de días trabajados en una semana': 0,
            'Doble rol en el mismo día': 0
        }
        for key in self.custom_penalties:
            penalties[key] = 0

        for day in range(1, self.n_days + 1):
            worked_week_days = {person: 0 for person in range(self.persons)}
            assigned_persons = set()

            for role, role_schedule in self.roles.items():
                person = plan[day][role]
                work_days[person] += 1
                worked_week_days[person] += 1

                # Penalizar si la person ya está asignada a otro role en el mismo día
                if person in assigned_persons:
                    cost += 15  # Penalización alta para evitar dobles asignaciones en el mismo día
                    penalties['Doble rol en el mismo día'] += 1
                assigned_persons.add(person)

                # Penalizar por cambio de turno sin descanso adecuado
                if last_assignation[person]:
                    days_after_last = (self.month_days[day - 1] - last_assignation[person]['fecha']).days
                    if last_assignation[person]['role'] == 'operador_noche' and role in ['auxiliar', 'operador_dia']:
                        if days_after_last < self.rest_days:
                            cost += 10
                            penalties['Descanso insuficiente entre turnos y otros roles'] += 1

                last_assignation[person] = {'fecha': self.month_days[day - 1], 'role': role}

            # Penalizar por exceder el máximo de días por semana
            for person, week_days in worked_week_days.items():
                if week_days > self.max_week_days:
                    cost += 5
                    penalties['Exceso de días trabajados en una semana'] += 1

            # Aplicar penalizaciones personalizadas
            cost, penalties = self.apply_custom_penalties(day, plan, cost, penalties)

        # Penalizar si una person excede los días de trabajo en el mes
        for person, work_days in work_days.items():
            if work_days > self.max_month_days:
                cost += (work_days - self.max_month_days) * 2
                penalties['Exceso de días trabajados en el mes'] += work_days - self.max_month_days

        return cost, penalties

    def apply_custom_penalties(self, day, plan, cost, penalties):
        for penalty_name, (penalty_cost, penalty_function) in self.custom_penalties.items():
            result = penalty_function(self, day, plan)  # Llamar a la función de penalización
            if result:  # Si la penalización se debe aplicar
                cost += penalty_cost
                penalties[penalty_name] += 1

        return cost, penalties
