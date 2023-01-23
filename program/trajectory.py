from .connection_node import Connection
import random
import copy

class Train():
    """Representation of a trajectory"""
    def __init__(self, name, network, which_region = 'holland'):
        self.which_region = which_region
        self.stations = network
        self.name = name
        self.trajectory = []
        self.current_station = self.choose_first_station()
        self.stop = False
        self.time = 0
        self.station_counter = 0

    def choose_first_station(self):
        """Chooses the first station randomly from the list of unvisited connections"""
        available_stations = []
        for station in self.stations.stations.values():
            if not station.visited:
                available_stations.append(station)

        rand_station = random.choice(available_stations)

        # add first station to trajectory list and set as visited
        self.trajectory.append(rand_station.name)
        rand_station.visit()
        return rand_station

    def connect(self):
        """Moves the current train to new possible connections
            until all possible connections are visited"""
        while self.stop == False:
            # initiate empty list to put unvisited connection
            choices = []
            # loop though all connections
            for connection in self.current_station.connect:
                # if the connection hasn't been visited before, add to the list
                if not connection.is_visited():
                    choices.append(connection)

            # if there are no unvisited connections available
            if len(choices) == 0:
                # end the trajectory
                self.stop = True
            else:
                # choose next station randomly from the possible connections
                next = random.choice(choices)
                # if the connection has been visited before, remove from the list
                self.check_time(next)

        self.current_station.visit()

    def greedy_time(self):
        """Moves current train to nearest possible stations by choosing
        the connection with the lowest time, until all possible connections
        are visited. If there are no unvisited connections, it chooses
        a random connection."""
        while self.stop == False:
            # initiate empty list to put unvisited connection
            choices = []

            # loop though all connections
            for connection in self.current_station.connect:
                # if the connection hasn't been visited before, add to the list
                if not connection.is_visited():
                    choices.append(connection)

            # if there are no unvisited connections available
            if len(choices) == 0:
                # choose a random connection
                all_conns = self.current_station.connect
                next = random.choice(all_conns)
                self.check_time(next)
            else:
                # sort choices list from least amount of minute to the most
                choices.sort(key=lambda x: x.time, reverse=False)
                # return new sorted list
                sorted_choices = sorted(choices, key=lambda x: x.time, reverse=False)
                # pick first connection of the list, which is the shortest
                next = sorted_choices[0]
                # if the connection has been visited before, remove from the list
                self.check_time(next)
        self.current_station.visit()

    def connect_with_used(self):
        while self.stop == False:
            # initiate empty list to put unvisited connection
            choices = []

            # loop though all connections
            for connection in self.current_station.connect:
                # if the connection hasn't been visited before, add to the list
                if not connection.is_visited():
                    choices.append(connection)
            # if there are no unvisited connections available
            if len(choices) == 0:
                # choose a random connection
                all_conns = self.current_station.connect
                next = random.choice(all_conns)
                self.check_time(next)
            else:
                # choose next station randomly from the possible connections
                next = random.choice(choices)
                # if the connection has been visited before, remove from the list
                self.check_time(next)
        self.current_station.visit()

    def check_time(self, connection: "Connection"):

        # check if requested map is of holland or the whole nl
        # and change the amount of minutes the train may ride accordingly
        if self.which_region == 'nl':
            max_time = 180
        elif self.which_region == 'holland':
            max_time = 120

        # keep track of the total time of the trajectory
        time = connection.time
        if self.time + time <= max_time:
            self.time = self.time + time
            self.add_station(connection)
        else:
            self.stop = True

    def add_station(self, connection: "Connection"):
        """Follows the chosen connection and adds the next station to the trajectory"""
        # get the next station
        other_station = connection.get_other_station(self.current_station)

        # add the next station to the trajectory list
        self.trajectory.append(other_station.name)

        # set the current station and connection as visited
        self.current_station.visit()
        connection.visit()

        # move to the next station
        self.current_station = other_station
        self.station_counter += 1

    def __repr__(self):
        return f"{self.name} visits {self.trajectory} in {self.time} minutes."
