from mesa.space import ContinuousSpace
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from pp.agents.herbivore import Herbivore
from pp.agents.predator import Predator


def collect_predators_sum(model):
    return len([
            agent
            for agent in model.schedule.agents
            if isinstance(agent, Predator)
        ])


def collect_herbivores_sum(model):
    return int(len([
            agent
            for agent in model.schedule.agents
            if isinstance(agent, Herbivore)
        ]))


class PredatorPreyModel(Model):
    def __init__(self, width, height, starting_agents):
        super().__init__()
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.data_collector = DataCollector(
            model_reporters={
                "Herbivores": collect_herbivores_sum,
                "Predators": collect_predators_sum
             }
        )

        for type_of_agent in starting_agents:
            agent = type_of_agent(self.next_id(), self)
            self.add_agent(agent)
        self.data_collector.collect(self)

    def step(self):
        self.schedule.step()
        self.data_collector.collect(self)

    def remove_agent(self, agent):
        self.space.remove_agent(agent)
        self.schedule.remove(agent)

    def add_agent(self, agent, pos=None):
        if pos is None:
            pos = self.random_pos()
        self.schedule.add(agent)
        self.space.place_agent(agent, pos)

    def random_pos(self):
        return  self.random.randrange(self.space.width),\
                self.random.randrange(self.space.height)
