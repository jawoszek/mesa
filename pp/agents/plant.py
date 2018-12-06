from mesa.agent import Agent


class Plant(Agent):
    chance_of_survival = 0

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.feeders = 0

    def how_to_draw(self):
        return {"Shape": "circle", "r": 1, "Filled": "true", "Color": "Green"}

    def be_eaten(self):
        self.feeders += 1
        if self.feeders > 20:
            self.model.remove_agent(self)
