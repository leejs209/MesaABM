from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from MesaABM.model import SchoolModel


def agent_portrayal(agent):
    """portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    """

    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if agent.status == "S":
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
    elif agent.status == "I":
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    elif agent.status == "E":
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    return portrayal


s_chart = ChartModule([{"Label": "Susceptible", "Color": "Blue"},
                       {"Label": "Exposed", "Color": "Yellow"},
                       {"Label": "Infected", "Color": "Red"},
                       {"Label": "Recovered", "Color": "Green"}
                       ],
                      data_collector_name='datacollector')

# CanvasGrid(portrayal_method, grid_width, grid_height, canvas_width=500(px), canvas_height=500(px) )
grid = CanvasGrid(agent_portrayal, 140, 61, 1400, 610)
