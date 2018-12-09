from math import pi, sin
from os import listdir
from re import search

from mesa.space import ContinuousSpace
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from pp.agents.herbivore import Herbivore
from pp.agents.predator import Predator
from pp.agents.plant import Plant
from pp.agents.ecosystems import PlantEcosystem
from pp.input import mock_input


def sin_cycle(base, interval):
    def cycle(step):
        return int((sin(2*pi*step/interval)*4+5) * base)
    return cycle


def collect_agents_sum(agent_type):
    def collect(model):
        return len([
            agent
            for agent in model.schedule.agents
            if isinstance(agent, agent_type)
        ])
    return collect


def collect_predators_sum(model):
    return collect_agents_sum(Predator)(model)


def collect_herbivores_sum(model):
    return collect_agents_sum(Herbivore)(model)


def collect_plants_sum(model):
    return collect_agents_sum(Plant)(model)


class PredatorPreyModel(Model):
    def __init__(self, width, height, starting_agents):
        super().__init__()
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.data_collector = DataCollector(
            model_reporters={
                "Herbivores": collect_herbivores_sum,
                "Predators": collect_predators_sum,
                "Plants": collect_plants_sum
             }
        )
        self.records_file_name = self.next_record_file_name()
        with open(self.records_file_name + '_attributes.csv', 'w') as file:
            self.record_model_data(file)

        for agent_template in starting_agents:
            if isinstance(agent_template, tuple):
                agent = agent_template[0](self.next_id(), self)
                self.add_agent(agent, agent_template[1])
            else:
                agent = agent_template(self.next_id(), self)
                self.add_agent(agent)
        self.data_collector.collect(self)
        self.plant_ecosystem = PlantEcosystem(sin_cycle(5, 200))

    def step(self):
        self.schedule.step()
        self.data_collector.collect(self)
        self.plant_ecosystem.regulate(self)
        with open(self.records_file_name + '.csv', 'a') as file:
            self.record(file)

    def remove_agent(self, agent):
        self.space.remove_agent(agent)
        self.schedule.remove(agent)

    def add_agent(self, agent, pos=None):
        if pos is None:
            pos = self.random_pos()
        self.schedule.add(agent)
        self.space.place_agent(agent, pos)

    def agents_with_type(self, agent_type):
        return [
            agent for agent
            in self.schedule.agents
            if isinstance(agent, agent_type)
        ]

    def random_pos(self):
        return self.random.randrange(self.space.width),\
               self.random.randrange(self.space.height)

    @staticmethod
    def next_record_file_name():
        found_ids = [
            int(found.group(1)) for found in
            [search('recorded_(\d+).csv', file) for file in listdir('.')]
            if found
        ]
        if not found_ids:
            return 'recorded_1'
        return "recorded_{}".format(max(found_ids)+1)

    def record(self, file):
        herbivores_count = len(self.agents_with_type(Herbivore))
        predators_count = len(self.agents_with_type(Predator))
        plants_count = len(self.agents_with_type(Plant))
        file.write(
            "{},{},{}\n".format(
                herbivores_count, predators_count, plants_count
            )
        )

    def record_model_data(self, file):
        file.write(
            "Herbivore[{}]\n".format(self.animal_attributes(Herbivore)) +
            "Predator[{}]\n".format(self.animal_attributes(Predator))
        )

    @staticmethod
    def animal_attributes(animal):
        template = '{}={}'
        attributes = [
            template.format('chance_of_survival', animal.chance_of_survival),
            template.format('sight_range', animal.sight_range),
            template.format('action_range', animal.action_range),
            template.format('speed', animal.speed),
            template.format('energy_consumption', animal.energy_consumption),
            template.format('breeding_cost', animal.breeding_cost),
            template.format('breeding_interval', animal.breeding_interval),
            template.format('breeding_age', animal.breeding_age)
        ]
        return ','.join(attributes)


if __name__ == "__main__":
    for _ in range(0, 10):
        model = PredatorPreyModel(100, 100, mock_input())
        for _ in range(0, 1000):
            model.step()
