from pp.agents.animal import Animal
from pp.agents.herbivore import Herbivore
from pp.agents.den import Den


def predators_den(unique_id, model):
    return Den(unique_id, model, Predator)


class Predator(Animal):
    sight_range = 30
    action_range = 4
    speed = 3
    energy_consumption = 2.5

    breeding_cost = 10
    breeding_interval = 5
    breeding_age = 5

    def __init__(self, unique_id, model, breeding=None):
        super().__init__(unique_id, model, breeding)

    def feeds_on(self):
        return Herbivore

    def how_to_draw(self):
        return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Red"}
