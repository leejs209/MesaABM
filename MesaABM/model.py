from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid, ContinuousSpace
import math


class Student(Agent):
    """ A Student that moves depending on the time, space, and other studnets"""

    def __init__(self, unique_id, group_no, model):
        super().__init__(unique_id, model)
        self.group_no = group_no

        # the speed of agent
        self.dx = 0
        self.dy = 0

        # discrete step 만큼 이동아고 나서 나머지
        self.x_float = 0
        self.y_float = 0

    def step(self):
        print('[' + "{:02}".format(self.unique_id) + '] ' + "{:02}".format(self.group_no))
        x, y = self.pos

        # since it is a grid, make Students move in discrete steps depending on the accumulated size of dx and dy
        def actual_delta(var):
            var_sign = 1
            if var < 0:
                var_sign = -1
            return var_sign * math.floor(abs(var))

        new_pos = x + actual_delta(self.dx), y + var_sign(dy) * math.floor(abs(self.dy))
        self.x_float, self.y_float = dx - actual_delta(dx) + dy - actual_delta(dy)
        self.model.grid.move_agent(self, new_pos)


class SchoolModel(Model):
    def __init__(self, N, group_N, width, height, *args: Any, **kwargs: Any):
        """ Constructor Function - Takes the number of population(N), and the number of classes(group_N)."""
        super().__init__(*args, **kwargs)
        self.num_agents = N
        self.group_N = group_N
        # self.grid = ContinuousSpace(width, height, True)
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        for t in range(self.num_agents):
            a = Student(t, t % group_N, self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        """ Advance the model by one step."""
        self.schedule.step()
