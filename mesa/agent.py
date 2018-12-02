# -*- coding: utf-8 -*-
"""
The agent class for Mesa framework.

Core Objects: Agent

"""
import math


class Agent:
    """ Base class for a model agent. """
    def __init__(self, unique_id, model):
        """ Create a new agent. """
        self.unique_id = unique_id
        self.model = model

    def step(self):
        """ A single step of the agent. """
        pass

    def neighbours(self, range_to_search, condition=None):
        neighbours = self.model.space.get_neighbors(self.pos, range_to_search,
                                                    False)
        return [
            neighbour
            for neighbour in neighbours
            if condition is None or condition(neighbour)
        ]

    def closest_in_neighbours(self, searching_for, neighbours, condition=None):
        def distance(target):
            distance_in_x = self.pos[0]-target.pos[0]
            distance_in_y = self.pos[1]-target.pos[1]
            return math.sqrt(distance_in_x**2 + distance_in_y**2)

        return sorted(
            [neighbour
             for neighbour in neighbours
             if (condition is None or condition(neighbour))
             and isinstance(neighbour, searching_for)
             ],
            key=distance
        )

    @property
    def random(self):
        return self.model.random
