from mesa.visualization.ModularVisualization import ModularServer
from .model import RiverTrips
from .SimpleContinuousModule import SimpleCanvas
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import TextElement

def virus_draw(agent):
    if (agent.name == 'Camp'):
        return {"Shape": "circle", "r": agent.size, "Filled": "true", "Color": agent.color, "Label": agent.label}
    if (agent.name == 'Trip'):
        return {"Shape": "circle", "r": agent.radius, "Filled": "true", "Color": agent.color, "Label": agent.label}
    return {"Shape": "circle", "r": 2, "Filled": "true", "Color": agent.color, "Label": agent.label}

virus_canvas = SimpleCanvas(virus_draw, 2000, 2000)

model_params = {"hualapai": UserSettableParameter('checkbox', 'Hualapai Camps', False),
                "commercial": UserSettableParameter('slider', 'Commercial Trips per Day', 0, 0, 5),
                "commercial_trip_length": UserSettableParameter('slider', 'Commercial Trip Length', 5, 5, 14),
                "private": UserSettableParameter('slider', 'Private Trips per Day', 3, 0, 5),
                "private_trip_length": UserSettableParameter('slider', 'Private Trip Length', 21, 5, 30),
                "max_iterations": UserSettableParameter('slider', 'Maximum Iterations', 60, 30, 120)}

chart_element1 = ChartModule([{"Label": "Trip Contacts", "Color": "Blue"},
                              {"Label": "Private Contacts", "Color": "Green"},
                              {"Label": "Commercial Contacts", "Color": "Orange"}])

server = ModularServer(RiverTrips, [virus_canvas, chart_element1], "River Trips Simulator", model_params)
