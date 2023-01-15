import numpy as np
import math

from mesa import Agent

class RiverMile(Agent):
    def __init__(self, unique_id, model, pos, label):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.color = "Blue"
        self.name = "RiverMile"
        self.label = label

    def step(self):
      pass

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class Camp(Agent):
    def __init__(self, unique_id, model, pos, camp):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.color = "BurlyWood"
        self.name = "Camp"
        size = camp['size']
        if size == 'Very Small':
          self.size = 1
        elif size == 'Small':
          self.size = 2
        elif size == 'Medium':
          self.size = 3
        else:
          self.size = 4
        self.label = camp['name']
        self.mile = camp['mile']
        self.latitude = camp['latitude']
        self.longitude = camp['longitude']
        self.notes = camp['notes']
        self.trips = []

    def step(self):
      pass

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class Rapid(Agent):
    def __init__(self, unique_id, model, pos, label):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.color = "Purple"
        self.name = "Rapid"
        self.label = label

    def step(self):
        pass

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class Landmark(Agent):
    def __init__(self, unique_id, model, pos, label):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.color = "black"
        self.name = "Landmark"
        self.label = label

    def step(self):
        pass

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class Trip(Agent):
    def __init__(self, unique_id, model, pos, itinerary, size):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.color = "green"
        self.name = "Trip"
        self.itinerary = itinerary
        self.label = "Lees Ferry"
        self.current = 0
        self.size = size
        if size > 16:
            self.radius = 4
        else:
            self.radius = 2
        self.prev = self.model.launch
        self.camp = self.model.launch
        self.contacts = []

    def step(self):
        self.prev = self.camp
        self.current = self.current + 1
        if self.itinerary[self.current] <= self.prev:
            # Layover since ahead of schedule.
            return
        # Leave camp.
        self.model.schedule._agents[self.prev].trips.clear()
        key = self.itinerary[self.current]
        while key <= self.model.diamond_creek:
            goal = self.model.schedule._agents[key]
            if self.size > 8 and goal.size == "Very Small":
                key = key + 1
                continue
            if self.size > 16 and goal.size == "Small":
                key = key + 1
                continue
            if not self.model.hualapai and goal.notes == "Hualapai":
                key = key + 1
                continue
            if key == self.model.diamond_creek:
                break
            if len(goal.trips) == 0:
                # Camp is available.
                break
            print(goal.label)
            self.contacts.append(goal.trips[0])
            self.model.schedule._agents[goal.trips[0]].contacts.append(self.unique_id)
            key = key + 1
        if key != self.itinerary[self.current]:
            print('-> ' + goal.label)
        goal.trips.append(self.unique_id)
        x = (goal.longitude - self.model.map.min_x)/(self.model.map.max_x - self.model.map.min_x) * self.model.space.x_max
        y = self.model.space.y_max - (goal.latitude - self.model.map.min_y)/(self.model.map.max_y - self.model.map.min_y) * self.model.space.y_max
        new_pos = np.array((x, y))
        self.label = goal.label
        self.camp = key
        self.model.space.move_agent(self, new_pos)
           
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

