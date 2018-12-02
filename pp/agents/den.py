from mesa import Agent
from pp.agents.breeding import FemaleBreeding, MaleBreeding


def is_male(denizen):
    return isinstance(denizen.breeding, MaleBreeding) \
           and denizen.breeding.can_breed()


def is_female_and_ready_to_breed(denizen):
    return isinstance(denizen.breeding, FemaleBreeding) \
           and denizen.breeding.can_breed()


class Den(Agent):
    range = 2

    def __init__(self, unique_id, model, species):
        super().__init__(unique_id, model)
        self.species = species

    def step(self):
        def right_species(denizen):
            return isinstance(denizen, self.species)

        denizens = self.neighbours(self.range, right_species)
        self.breed_denizens(denizens)

    def breed_denizens(self, denizens):
        closest_males = self.closest_in_neighbours(self.species, denizens,
                                                  is_male)
        closest_females = self.closest_in_neighbours(self.species,denizens,
                                                    is_female_and_ready_to_breed)

        if not closest_males or not closest_females:
            return
        closest_males[0].breeding.breed()
        closest_females[0].breeding.breed()
        child = self.species(self.model.next_id(), self.model)
        self.model.add_agent(child, self.pos)

    def how_to_draw(self):
        return {"Shape": "circle", "r": 4, "Filled": "true", "Color": "Black"}
