from mesa.visualization.modules import CanvasGrid


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
    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1

    return portrayal


# CanvasGrid(portrayal_method, grid_width, grid_height, canvas_width=500(px), canvas_height=500(px) )
grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)