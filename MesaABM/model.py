from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid, ContinuousSpace
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
    """ A Student that moves depending on the time, space, and other studnets"""

    def __init__(self, unique_id, group_no, status, infection_duration, model):
        super().__init__(unique_id, model)
        self.group_no = group_no
        # the speed of agent
        self.dx = 0
        self.dy = 0
        self.status = status
        self.infected_timeleft = infection_duration
        self.infection_duration = infection_duration

    def step(self):

        # x, y = self.pos
        # self.dx = random.randint(-1, 1)
        # self.dy = random.randint(-1, 1)
        # new_pos = x + self.dx, y + self.dy

        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=1)
        new_pos = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_pos)

        if self.status == "I":
            self.spread_infection()
            if self.infected_timeleft > 0:
                self.infected_timeleft -= 1
            else:
                self.status = "R"
                self.infected_timeleft = self.infection_duration

    def spread_infection(self):
        """ This function is called if agent is Infected """
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            if other.status == "S":
                other.status = "I"


class SchoolModel(Model):
    def __init__(self, N, group_N, width, height, initial_num_infected, infection_duration, *args, **kwargs):
        """ Constructor Function - Takes the number of population(N), and the number of classes(group_N)."""
        super().__init__()
        self.num_agents = N
        self.group_N = group_N
        self.infection_duration = infection_duration
        # self.grid = ContinuousSpace(width, height, True)
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        for t in range(self.num_agents):
            # Student(N, group_N, status, infection_duration)
            a = Student(t, t % group_N, "S", self.infection_duration, self)
            if initial_num_infected > 0:
                a.status = "I"
                initial_num_infected -= 1

            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters={"Susceptible": s_count, "Infected": i_count, "Recovered": r_count},
            agent_reporters={}
        )

    def step(self):
        """ Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()
