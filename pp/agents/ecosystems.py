from operator import attrgetter
from random import sample

from pp.agents.plant import Plant


class PlantEcosystem:
    def __init__(self, cycle) -> None:
        super().__init__()
        self.cycle = cycle

    def regulate(self, model):
        all_plants = model.agents_with_type(Plant)
        plants = sorted(
            sample(all_plants, k=len(all_plants)),
            key=attrgetter('feeders'),
            reverse=True
        )
        current_count = len(plants)
        current_value = self.cycle(model.schedule.time)
        if current_count > current_value:
            self.remove_plants(model, current_count - current_value, plants)
            return
        if current_count < current_value:
            self.add_plants(model, current_value - current_count)

    def remove_plants(self, model, count, plants):
        for index in range(0, count):
            model.remove_agent(plants[index])

    def add_plants(self, model, count):
        for plant in [Plant(model.next_id(), model) for _ in range(0, count)]:
            model.add_agent(plant)
