def random_breeding(species, random):
    return random.choice([MaleBreeding, FemaleBreeding])(species)


class MaleBreeding:

    def __init__(self, species) -> None:
        self.species = species
        self.age = 0

    def get_old(self):
        self.age += 1

    def can_breed(self):
        return self.species.breeding_age() <= self.age

    def breed(self):
        pass


class FemaleBreeding:

    def __init__(self, species) -> None:
        self.species = species
        self.time_to_next_breeding = species.breeding_interval()
        self.age = 0

    def get_old(self):
        self.time_to_next_breeding = max(0, self.time_to_next_breeding - 1)
        self.age += 1

    def can_breed(self):
        return self.time_to_next_breeding <= 0\
               and self.species.breeding_age() <= self.age

    def breed(self):
        self.time_to_next_breeding = self.species.breeding_interval()
