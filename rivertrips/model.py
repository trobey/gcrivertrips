'''
Covid-19
=============================================================
A Mesa river trip simulation on a continuous space.
'''

import math
import numpy as np
import csv
import gpxpy
import gpxpy.gpx

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from .agents import RiverMile, Camp, Rapid, Landmark, Trip

class Map:
    pass

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class RiverTrips(Model):
    '''
    RiverTrips model class. Handles agent creation, placement and scheduling.
    '''

    def __init__(self,
                 width=2000,
                 height=2000,
                 hualapai=False,
                 max_iterations=60,
                 commercial=0,
                 commercial_trip_length=5,
                 private=3,
                 private_trip_length=21):
        '''
        Create a new river trip simulation.

        Args:
        '''

        gpx_file = open('GrandCanyonWaypoints.gpx', 'r')
        gpx = gpxpy.parse(gpx_file)

        min_latitude = 0.0
        max_latitude = 0.0
        min_longitude = 0.0
        max_longitude = 0.0
        for waypoint in gpx.waypoints:
            if min_latitude == 0.0 or waypoint.latitude < min_latitude:
                min_latitude = waypoint.latitude
            if max_latitude == 0.0 or waypoint.latitude > max_latitude:
                max_latitude = waypoint.latitude
            if min_longitude == 0.0 or waypoint.longitude < min_longitude:
                min_longitude = waypoint.longitude
            if max_longitude == 0.0 or waypoint.longitude > max_longitude:
                max_longitude = waypoint.longitude
        min_longitude = math.floor(min_longitude * 10.0) / 10.0
        max_longitude = math.ceil(max_longitude * 10.0) / 10.0

        self.map = Map()
        if (max_latitude - min_latitude)/height > (max_longitude - min_longitude)/width:
            self.map.delta = (max_latitude - min_latitude)/height
            self.map.min_y = min_latitude;
            self.map.max_y = max_latitude;
            middle = (min_longitude + max_longitude)/2
            self.map.min_x = middle - width * self.map.delta / 2
            self.map.max_x = middle + width * self.map.delta / 2
        else:
            self.map.delta = (max_longitude - min_longitude)/width
            self.map.min_x = min_longitude;
            self.map.max_x = max_longitude;
            self.map.max_y = math.ceil(max_latitude * 10.0) / 10.0
            self.map.min_y = max_latitude - height * self.map.delta


        self.current_id = 0;
        self.hualapai = hualapai
        self.max_iterations = max_iterations
        self.iteration = 0
        self.commercial = commercial
        self.commercial_trip_length = commercial_trip_length
        self.private = private
        self.private_trip_length = private_trip_length
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        with open('camps.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for row in reader:
                if row[4] == 'Latitude':
                    continue
                camp = {
                    "mile": float(row[0]),
                    "name": row[1],
                    "size": row[2],
                    "side": row[3],
                    "latitude": float(row[4]),
                    "longitude": float(row[5]),
                    "notes": row[6]
                }
                self.create_camp(camp)
        self.launch = 0
        agent_keys = list(self.schedule._agents.keys())
        for agent_key in agent_keys:
            if self.schedule._agents[agent_key].label == 'Lees Ferry':
                self.launch = agent_key
            if self.schedule._agents[agent_key].label == 'Diamond Creek':
                self.diamond_creek = agent_key
            if self.schedule._agents[agent_key].label == 'Upper 185 Mile':
                self.helipad = agent_key
        self.create_waypoints(gpx)
        self.create_trips()
        self.same_camps = 0;
        self.datacollector = DataCollector(model_reporters = {"Trip Contacts":self.collect_contacts, "Private Contacts": self.collect_private_contacts, "Commercial Contacts": self.collect_commercial_contacts})
        self.contacts = 0
        self.private_contacts = 0
        self.commercial_contacts = 0

        self.running = True

    def create_waypoints(self, gpx):
        for waypoint in gpx.waypoints:
            x = (waypoint.longitude - self.map.min_x)/(self.map.max_x - self.map.min_x) * self.space.x_max
            y = self.space.y_max - (waypoint.latitude - self.map.min_y)/(self.map.max_y - self.map.min_y) * self.space.y_max
            pos = np.array((x, y))
            if waypoint.name[0:2] == 'RM':
                mypoint = RiverMile(self.next_id(), self, pos, waypoint.description)
                self.space.place_agent(mypoint, pos)
                self.schedule.add(mypoint)
            elif waypoint.name[0:2] == 'C-':
                pass
            elif waypoint.name[0:2] == 'R-':
                mypoint = Rapid(self.next_id(), self, pos, waypoint.description)
                self.space.place_agent(mypoint, pos)
                self.schedule.add(mypoint)
            else:
                #mypoint = Landmark(self.next_id(), self, pos, waypoint.description)
                #self.space.place_agent(mypoint, pos)
                #self.schedule.add(mypoint)
                pass

    def create_camp(self, camp):
        latitude = camp["latitude"]
        longitude = camp["longitude"]
        x = (longitude - self.map.min_x)/(self.map.max_x - self.map.min_x) * self.space.x_max
        y = self.space.y_max - (latitude - self.map.min_y)/(self.map.max_y - self.map.min_y) * self.space.y_max
        pos = np.array((x, y))
        mypoint = Camp(self.next_id(), self, pos, camp)
        self.space.place_agent(mypoint, pos)
        self.schedule.add(mypoint)

    def create_trips(self):
        for i in range(self.private):
          if i == 2:
              size = 8
          else:
              size = 16
          itinerary = self.create_itinerary(size, self.private_trip_length)
          x = (-111.585646 - self.map.min_x)/(self.map.max_x - self.map.min_x) * self.space.x_max
          y = self.space.y_max - (36.866112 - self.map.min_y)/(self.map.max_y - self.map.min_y) * self.space.y_max
          pos = np.array((x, y))
          mypoint = Trip(self.next_id(), self, pos, itinerary, size)
          self.space.place_agent(mypoint, pos)
          self.schedule.add(mypoint)
        for i in range(self.commercial):
          size = 30
          itinerary = self.create_itinerary(size, self.commercial_trip_length)
          x = (-111.585646 - self.map.min_x)/(self.map.max_x - self.map.min_x) * self.space.x_max
          y = self.space.y_max - (36.866112 - self.map.min_y)/(self.map.max_y - self.map.min_y) * self.space.y_max
          pos = np.array((x, y))
          mypoint = Trip(self.next_id(), self, pos, itinerary, size)
          self.space.place_agent(mypoint, pos)
          self.schedule.add(mypoint)

    def collect_same_camps(self):
        return self.same_camps

    def collect_contacts(self):
        return self.contacts

    def collect_private_contacts(self):
        return self.private_contacts

    def collect_commercial_contacts(self):
        return self.commercial_contacts

    def step(self):
        agent_keys = list(self.schedule._agents.keys())
        for agent_key in agent_keys:
            if self.schedule._agents[agent_key].name == 'Trip':
                self.schedule._agents[agent_key].contacts.clear()
        self.iteration = self.iteration + 1
        self.schedule.step()
        # collect data
        for agent_key in agent_keys:
            if self.schedule._agents[agent_key].name == 'Trip':
                agent = self.schedule._agents[agent_key]
                for other_key in agent_keys:
                    if self.schedule._agents[other_key].name == 'Trip':
                        if other_key in agent.contacts:
                            continue
                        other = self.schedule._agents[other_key]
                        if agent.prev < other.prev and agent.camp > other.camp:
                            agent.contacts.append(other_key)
                            other.contacts.append(agent_key)
                        if agent.prev > other.prev and agent.camp < other.camp:
                            agent.contacts.append(other_key)
                            other.contacts.append(agent_key)
        num_trips = 0
        num_private_trips = 0
        num_commercial_trips = 0
        self.contacts = 0
        self.private_contacts = 0
        self.commercial_contacts = 0
        for agent_key in agent_keys:
            if self.schedule._agents[agent_key].name == 'Trip':
                num_trips = num_trips + 1
                self.contacts = self.contacts + len(self.schedule._agents[agent_key].contacts)
                if self.schedule._agents[agent_key].size > 16:
                    num_commercial_trips = num_commercial_trips + 1
                    self.commercial_contacts = self.commercial_contacts + len(self.schedule._agents[agent_key].contacts)
                else:
                    num_private_trips = num_private_trips + 1
                    self.private_contacts = self.private_contacts + len(self.schedule._agents[agent_key].contacts)
        self.contacts = self.contacts / num_trips
        if num_private_trips == 0:
            self.private_contacts = 0.0
        else:
            self.private_contacts = self.private_contacts / num_private_trips
        if num_commercial_trips == 0:
            self.commercial_contacts = 0.0
        else:
            self.commercial_contacts = self.commercial_contacts / num_commercial_trips
        self.datacollector.collect(self)
        if self.iteration == self.max_iterations:
            self.running = False
        for agent_key in agent_keys:
            if self.schedule._agents[agent_key].name == 'Trip':
                if self.schedule._agents[agent_key].label == "Diamond Creek":
                    agent = self.schedule._agents[agent_key]
                    self.space.remove_agent(agent)
                    self.schedule.remove(agent)
        self.create_trips()
        self.same_camps = 0;

    def create_itinerary(self, size, trip_length):
        if size > 16:
            end = 185.9
        else:
            end = 225.7
        current_key = self.launch
        current_camp = self.schedule._agents[self.launch]
        layover = False
        itinerary = []
        itinerary.append(self.launch)
        while current_camp.mile < end:
            left = trip_length - len(itinerary)
            remaining = end - current_camp.mile
            if left == 1:
                if size > 16:
                    # Camp above helipad.
                    itinerary.append(self.helipad)
                break;
            distance = 6.0 + 2.0 * ((remaining / left) - 6.0) * self.random.random()
            target = current_camp.mile + distance
         
            prev_key = current_key
            prev_camp = current_camp
            camp_keys = list(self.schedule._agents.keys())
            for camp_key in camp_keys:
                if self.schedule._agents[camp_key].name == 'Camp':
                    camp = self.schedule._agents[camp_key]
                    if camp.mile < current_camp.mile:
                        continue
                    if not self.hualapai and camp.notes == "Hualapai":
                        continue
                    if size > 8 and camp.size == "Very Small":
                        continue
                    if size > 16 and camp.size == "Small":
                        continue
                    mile = camp.mile
                    if mile > target:
                        if layover and mile - target > target - prev_camp.mile:
                            itinerary.append(prev_key)
                            current_key = prev_key
                            current_camp = prev_camp
                        else:
                            itinerary.append(camp_key)
                            current_key = camp_key
                            current_camp = camp
                            layover = True
                        break
                    prev_key = camp_key
                    prev_camp = camp
        itinerary.append(self.diamond_creek)
        return itinerary
