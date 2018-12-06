def random_breeding(animal, random):
    return random.choice([MaleBreeding, FemaleBreeding])(animal)


class MaleBreeding:

    def __init__(self, animal) -> None:
        self.animal = animal
        self.age = 0

    def get_old(self):
        self.age += 1

    def can_breed(self):
        return self.animal.breeding_age() <= self.age

    def breed(self):
        self.animal.energy -= 15


class FemaleBreeding:

    def __init__(self, animal) -> None:
        self.animal = animal
        self.time_to_next_breeding = animal.breeding_interval()
        self.age = 0

    def get_old(self):
        self.time_to_next_breeding = max(0, self.time_to_next_breeding - 1)
        self.age += 1

    def can_breed(self):
        return self.time_to_next_breeding <= 0\
               and self.animal.breeding_age() <= self.age

    def breed(self):
        self.animal.energy -= 20
        self.time_to_next_breeding = self.animal.breeding_interval()
