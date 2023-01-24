from .connection_node import Connection
import random
import copy

class Train():
    """Representation of a trajectory"""
    def __init__(self, name, network, which_region = 'holland', start = 'random'):
        self.which_region = which_region
        self.stations = network
        self.name = name
        self.trajectory = []
        self.object_traj = []
        self.object_conns = []
        self.current_station = self.choose_first_station(start)
        self.stop = False
        self.time = 0
        self.station_counter = 0

    def choose_first_station(self, start):
        """Chooses the first station randomly from the list of unvisited connections"""
        available_stations = []
        for station in self.stations.stations.values():
            if not station.visited:
                available_stations.append(station)
        
        if start == 'min_con':
            min_con = None
            for choose_station in available_stations:
                con_count = len(choose_station.connect)

                if min_con == None:
                    min_con = con_count
                    first_station = choose_station
                elif con_count < min_con:
                    min_con = con_count
                    first_station = choose_station
        elif start == 'random':
            try:
                first_station = random.choice(available_stations)
            except:
                first_station = random.choice(list(self.stations.stations.values()))

        # add first station to trajectory list and set as visited
        self.trajectory.append(first_station.name)
        self.object_traj.append(first_station)
        first_station.visit()
        return first_station

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
    
    def greedy_conns(self):
        """Moves current train to next possible stations by choosing
        the station that holds the least amount of connections, until all
        possible connections are visited. If there are no unvisited connections,
        it chooses a random connection."""
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
                # current station is set as station with minimal connections
                min_con = None
                # loop through list with stations
                for connection in choices:
                    # get the station that is connected with each connection
                    station = connection.get_other_station(self.current_station)
                    # save the connection count of every station
                    con_count = len(station.connect)

                    if min_con == None:
                        min_con = con_count
                        next = connection
                    # if the connection count is less than the connection count of current station
                    # with minimal connections, set new connection as next
                    elif con_count < min_con:
                        min_con = con_count
                        next = connection

                    # probleem voor later, bias kiest de middelste optie het vaakst
                    elif con_count == min_con:
                        random_choice = [next, connection]
                        next = random.choice(random_choice)
        
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
        self.object_traj.append(other_station)
        self.object_conns.append(connection)

        # set the current station and connection as visited
        self.current_station.visit()
        connection.visit()

        # move to the next station
        self.current_station = other_station
        self.station_counter += 1

    def __repr__(self):
        return f"{self.name} visits {self.trajectory} in {self.time} minutes."
