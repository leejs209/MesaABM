from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


def s_count(model):
    cnt = 0
    for agent in model.schedule.agents:
        if agent.status == "S":
            cnt += 1
    return cnt


def i_count(model):
    cnt = 0
    for agent in model.schedule.agents:
        if agent.status == "I":
            cnt += 1
    return cnt


def r_count(model):
    cnt = 0
    for agent in model.schedule.agents:
        if agent.status == "R":
            cnt += 1
    return cnt


class Student(Agent):
    """ A Student that moves depending on the time, space, and other students"""

    def __init__(self, unique_id, group_no, status, infection_duration, model):
        super().__init__(unique_id, model)
        self.group_no = group_no
        self.status = status
        self.infected_timeleft = infection_duration
        self.infection_duration = infection_duration

    def move_to_group(self, group_no):
        x1 = ((group_no - 1) % 14) * 10 + 1
        x2 = x1 + 8

        y1 = ((group_no - 1) // 14) * 10 + 1
        y2 = y1 + 8

        new_pos = (self.random.randint(x1, x2), self.random.randint(y1, y2))
        self.model.grid.move_agent(self, new_pos)

    def move_within_bound(self, group_no):
        x1 = ((group_no - 1) % 14) * 10 + 1
        x2 = x1 + 8

        y1 = ((group_no - 1) // 14) * 10 + 1
        y2 = y1 + 8

        #if not x1 <= self.pos[0] <= x2 or not y1 <= self.pos[1] <= y2:
        #    print("Agent is told to move in group's bound without being in it first.", x1, self.pos[0], x2, y1, self.pos[1], y2)

        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=1)

        bounded_steps = []
        for x in possible_steps:
            if x1 <= x[0] <= x2 and y1 <= x[1] <= y2:
                bounded_steps.append(x)


        new_pos = self.random.choice(bounded_steps)
        self.model.grid.move_agent(self, new_pos)

    def spread_infection(self):
        # Spread infection only when self is Infected
        if self.status != "I":
            return
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) <= 1:
            return
        for x in cellmates:
            if x.status == "S":
                if self.random.random() <= self.model.infection_prob_per_contact:
                    x.status = "I"

    def recovery_countdown(self):
        if self.status != "I":
            return
        if self.infected_timeleft > 0:
            self.infected_timeleft -= 1
        else:
            self.status = "R"
            self.infected_timeleft = self.infection_duration

    def step(self):
        self.move_within_bound(group_no=self.group_no)
        self.recovery_countdown()
        self.spread_infection()

class SchoolModel(Model):
    def __init__(self, N, N_per_group, width, height, initial_num_infected,
                 infection_duration, infection_prob_per_contact, restaurant_multiplier, visit_prob_per_person,
                 ):

        super().__init__()

        self.N = N
        self.N_per_group = N_per_group
        self.infection_duration = infection_duration
        self.infection_prob_per_contact = infection_prob_per_contact
        self.restaurant_multiplier = restaurant_multiplier
        self.visit_prob_per_person = visit_prob_per_person

        # self.grid = ContinuousSpace(width, height, True)
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)

        initial_infected = [self.random.randrange(0, self.N) for _ in range(initial_num_infected)]

        for t in range(0, self.N):
            # (self, unique_id, group_no, status, infection_duration, model)
            group_no = t // N_per_group + 1

            x1 = ((group_no - 1) % 14) * 10 + 1
            x2 = x1 + 8

            y1 = ((group_no - 1) // 14) * 10 + 1
            y2 = y1 + 8

            a = Student(t + 1, group_no, "S", self.infection_duration, self)

            if t in initial_infected:
                a.status = "I"

            self.schedule.add(a)

            self.grid.place_agent(a, (self.random.randint(x1, x2), self.random.randint(y1, y2)))

        self.datacollector = DataCollector(
            model_reporters={"Susceptible": s_count, "Infected": i_count, "Recovered": r_count},
            agent_reporters={}
        )

    def step(self):
        """ Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()
