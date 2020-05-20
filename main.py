from mesa import Agent, Model
from mesa.time import RandomActivation

class Student(Agent):
    """ A Student that moves depending on the time, space, and other studnets"""

    def __init__(self, unique_id, group_no, model):
        # I don't really understand why this line exists => check later for debugging
        super().__init__(unique_id, model)
        self.group_no = group_no

    def step(self):
        print('[' + "{:02}".format(self.unique_id) + '] ' + "{:02}".format(self.group_no))


class SchoolModel(Model):
    def __init__(self, N, group_N):
        """ Constructor Function - Takes the number of population(N), and the number of classes(group_N)."""
        self.num_agents = N
        self.group_N = group_N
        self.schedule = RandomActivation(self)
        for x in range(self.num_agents):
            a = Student(x, x % group_N, self)
            self.schedule.add(a)

    def step(self):
        """ Advance the model by one step."""
        self.schedule.step()

a = SchoolModel(30,6)
a.step()