from pp.agents.animal import Animal
from pp.agents.herbivore import Herbivore
from pp.agents.den import Den


def predators_den(unique_id, model):
    return Den(unique_id, model, Predator)


class Predator(Animal):
    sight_range = 15
    action_range = 1
    speed = 2
    energy_consumption = 2

    def __init__(self, unique_id, model, breeding=None):
        super().__init__(unique_id, model, breeding)

    def feeds_on(self):
        return Herbivore

    @classmethod
    def breeding_interval(cls):
        return 80

    @classmethod
    def breeding_age(cls):
        return 40

    def how_to_draw(self):
        return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Red"}
