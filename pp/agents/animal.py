from mesa import Agent
from pp.agents.breeding import random_breeding
from pp.agents.den import Den


def is_far_from_its_den(animal):
    if not isinstance(animal, Animal):
        return False
    def den_of_this_species(target):
        return isinstance(target, Den) and target.species is type(animal)
    return not animal.neighbours(animal.action_range, den_of_this_species)


class Animal(Agent):
    is_renewable = False
    sight_range = None
    action_range = None
    speed = None
    energy_consumption = None

    def __init__(self, unique_id, model, breeding=None):
        super().__init__(unique_id, model)
        self.energy = 600
        if breeding is None:
            self.breeding = random_breeding(type(self), model.random)
        else:
            self.breeding = breeding

    def move(self, seen_neighbours):
        target, condition = self.target_for_move()
        closest_targets = self.closest_in_neighbours(target, seen_neighbours, condition)
        if closest_targets:
            new_position = self.new_position_in_direction_of(closest_targets[0])
        else:
            new_position = self.new_random_position()
        self.model.space.move_agent(self, new_position)

    def eat(self, close_neighbours):
        if self.energy > 600:
            return

        prey_in_range = self.closest_in_neighbours(self.feeds_on(), close_neighbours, is_far_from_its_den)
        if not prey_in_range:
            return
        victim = prey_in_range[0]
        if not victim.is_renewable:
            self.model.remove_agent(victim)
        self.energy = 1000

    def get_old(self):
        self.energy -= 1
        if self.energy <= 0:
            self.model.remove_agent(self)

    def step(self):
        seen_neighbours = self.neighbours(self.sight_range)
        close_neighbours = self.neighbours(self.action_range)
        self.move(seen_neighbours)
        self.eat(close_neighbours)
        self.get_old()
        self.breeding.get_old()

    def new_random_position(self):
        current_x = self.pos[0]
        current_y = self.pos[1]
        random_move_x = self.model.random.random() * 2 * self.speed - self.speed
        random_move_y = self.model.random.random() * 2 * self.speed - self.speed
        return current_x + random_move_x, current_y + random_move_y

    def new_position_in_direction_of(self, destination):
        current_x = self.pos[0]
        current_y = self.pos[1]
        destination_x = destination.pos[0]
        destination_y = destination.pos[1]
        x_distance = destination_x - current_x
        y_distance = destination_y - current_y
        x_direction = -1 if current_x > destination_x else 1
        y_direction = -1 if current_y > destination_y else 1
        random_move_x = x_direction * self.model.random.random() * self.speed
        random_move_y = y_direction * self.model.random.random() * self.speed
        delta_x = max(min(x_distance, 1), random_move_x)
        delta_y = max(min(y_distance, 1), random_move_y)
        return current_x + delta_x, current_y + delta_y

    def feeds_on(self):
        raise NotImplementedError('Abstract function')

    def target_for_move(self):
        if self.energy < 500:
            return self.feeds_on(), None

        def den_of_this_species(target):
            return isinstance(target, Den) and target.species is type(self)
        return Den, den_of_this_species

    def how_to_draw(self):
        raise NotImplementedError('Abstract function')
