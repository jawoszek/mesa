from math import pi, sin

from mesa.space import ContinuousSpace
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from pp.agents.herbivore import Herbivore
from pp.agents.predator import Predator
from pp.agents.plant import Plant
from pp.agents.ecosystems import PlantEcosystem


def sin_cycle(base, interval):
    def cycle(step):
        return int((sin(2*pi*step/interval)*2+3) * base)
    return cycle


def collect_agents_sum(type):
    def collect(model):
        return len([
            agent
            for agent in model.schedule.agents
            if isinstance(agent, type)
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

        for agent_template in starting_agents:
            if isinstance(agent_template, tuple):
                agent = agent_template[0](self.next_id(), self)
                self.add_agent(agent, agent_template[1])
            else:
                agent = agent_template(self.next_id(), self)
                self.add_agent(agent)
        self.data_collector.collect(self)
        self.plant_ecosystem = PlantEcosystem(sin_cycle(2, 100))

    def step(self):
        self.schedule.step()
        self.data_collector.collect(self)
        self.plant_ecosystem.regulate(self)

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
