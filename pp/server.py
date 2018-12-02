from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule

from pp.model import PredatorPreyModel
from pp.input import mock_input


def how_to_draw(agent):
    return agent.how_to_draw()


class Canvas(VisualizationElement):
    local_includes = ["canvas.js"]
    portrayal_method = None

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = ("new Simple_Continuous_Module({}, {})".
                       format(self.canvas_width, self.canvas_height))
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        space_state = []
        for obj in model.schedule.agents:
            portrayal = self.portrayal_method(obj)
            x, y = obj.pos
            x = ((x - model.space.x_min) /
                 (model.space.x_max - model.space.x_min))
            y = ((y - model.space.y_min) /
                 (model.space.y_max - model.space.y_min))
            portrayal["x"] = x
            portrayal["y"] = y
            space_state.append(portrayal)
        return space_state


chart = ChartModule(
    [
        {"Label": "Herbivores", "Color": "Green"},
        {"Label": "Predators", "Color": "Red"}
    ],
    data_collector_name='data_collector'
)

canvas = Canvas(how_to_draw, 500, 500)
server = ModularServer(PredatorPreyModel, [canvas, chart], "Hey", {"width": 100, "height":100, "starting_agents":mock_input()})

if __name__ == "__main__":
    server.launch()
