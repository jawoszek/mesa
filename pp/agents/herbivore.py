from pp.agents.animal import Animal
from pp.agents.plant import Plant
from pp.agents.den import Den


def herbivores_den(unique_id, model):
    return Den(unique_id, model, Herbivore)


class Herbivore(Animal):
    chance_of_survival = 0.5

    sight_range = 10
    action_range = 2
    speed = 2
    energy_consumption = 0.3

    breeding_cost = 15
    breeding_interval = 3
    breeding_age = 5

    def __init__(self, unique_id, model, breeding=None):
        super().__init__(unique_id, model, breeding)

    def feeds_on(self):
        return Plant

    def how_to_draw(self):
        return {"Shape": "circle", "r": 1, "Filled": "true", "Color": "Blue"}
