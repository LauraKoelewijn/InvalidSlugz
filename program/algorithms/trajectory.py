from .connection_node import Connection
import random
import copy
from typing import List

class Train():
    """A class representation of a trajectory.
    Holds the information about the trajectory.
    Can choose the first station of a trajectory and then connect it to
    a next station by using one of our four algorithm functions. Also keeps
    track of the time of a trajectory."""
    def __init__(self, name: str, network: "Network", which_region: str = 'holland', start: str = 'random') -> None:
        self.which_region = which_region
        self.stations = network
        self.name = name
        self.trajectory: List[str] = []
        self.object_traj: List["Station"] = []
        self.object_conns: List["Connection"] = []
        self.current_station: "Station" = self.choose_first_station(start)
        self.stop: bool = False
        self.time: float = 0
        self.station_counter: int = 0

    def choose_first_station(self, start: str) -> "Station":
        """Chooses the first station randomly from the list of
        unvisited connections.

        Args:
            start (str): random or min_con

        Returns:
            first_station: a Station object.
        """
        available_stations: List["Station"] = []
        for station in self.stations.stations.values():
            if not station.visited:
                available_stations.append(station)

        if start == 'min_con':
            min_con: int = len(self.stations.stations.values())
            if len(available_stations) > 0:
                for choose_station in available_stations:
                    con_count: int = len(choose_station.connect)

                    if con_count < min_con:
                        min_con: int = con_count
                        first_station: "Station" = choose_station
            else:
                first_station = random.choice(list(self.stations.stations.values()))

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

    def connect(self) -> None:
        """Chooses a random connection from a list of possible and unvisited
        connections. Moves the current train over these connections
        until all possible connections are visited. Stops when all connections
        are visited."""
        while self.stop == False:
            # initiate empty list to put unvisited connection
            choices: List["Connection"] = []
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
                next: "Connection" = random.choice(choices)
                # if the connection has been visited before, remove from the list
                self.check_time(next)

        self.current_station.visit()

    def connect_with_used(self) -> None:
        """Chooses a random connection from a list of possible and unvisited
        connections. Moves the current train over these connections
        until all possible connections are visited. When all connections are
        visited, it chooses a random connection out of all connections,
        whether visited or not."""
        while self.stop == False:
            # initiate empty list to put unvisited connection
            choices: List["Connection"] = []

            # loop though all connections
            for connection in self.current_station.connect:
                # if the connection hasn't been visited before, add to the list
                if not connection.is_visited():
                    choices.append(connection)
            # if there are no unvisited connections available
            if len(choices) == 0:
                # choose a random connection
                all_conns: List["Connection"] = self.current_station.connect
                next: "Connection" = random.choice(all_conns)
                self.check_time(next)
            else:
                # choose next station randomly from the possible connections
                next = random.choice(choices)
                # if the connection has been visited before, remove from the list
                self.check_time(next)
        self.current_station.visit()

    def greedy_time(self, time: str) -> None:
        """Moves current train to nearest possible stations by choosing
        the connection with the lowest or highest time depending on the
        'short' or 'long' time arg.
        Stops when time is up. If there are no unvisited connections, it
        chooses a random connection.

        Args:
            time (str): 'short' or 'long' depending on which algorithm
            to use; connecting with the shortest or longest connections.

        """
        while self.stop == False:
            # initiate empty list to put unvisited connections
            choices: List["Connection"] = []

            # loop though all connections
            for connection in self.current_station.connect:
                # if the connection hasn't been visited before, add to the list
                if not connection.is_visited():
                    choices.append(connection)

            # if there are no unvisited connections available
            if len(choices) == 0:
                # choose a random connection
                all_conns: List["Connection"] = self.current_station.connect
                next: "Connection" = random.choice(all_conns)
                self.check_time(next)
            else:
                if time == 'short':
                    # sort choices list from least amount of minute to the most
                    choices.sort(key=lambda x: x.time, reverse=False)
                    # return new sorted list
                    sorted_choices = sorted(choices, key=lambda x: x.time, reverse=False)
                elif time == 'long':
                    # sort choices list from most amount of minute to the least
                    choices.sort(key=lambda x: x.time, reverse=True)
                    # return new sorted list
                    sorted_choices = sorted(choices, key=lambda x: x.time, reverse=True)
                # pick first connection of the list, which is the shortest
                next = sorted_choices[0]
                # if the connection has been visited before, remove from the list
                self.check_time(next)


        self.current_station.visit()

    def greedy_conns(self, amount: str) -> None:
        """Moves current train to next possible station by choosing
        the station that holds the least or the most amount of connections,
        depending on the 'min' or 'max' amount arg, until all
        possible connections are visited. If there are no unvisited connections,
        it uses lookahead to look at connections of next possible stations.
        If there are still unvisited connections, it moves train to the
        corresponding station with the least amount of unvisited connections.

        Args:
            amount (str): 'min' or 'max' depending on which algorithm
            to use; connecting with the max or min amount of connections.

        """
        while self.stop == False:
            # initiate empty list to put unvisited connections
            choices: List["Connection"] = []

            # loop though all connections
            for connection in self.current_station.connect:
                # if the connection hasn't been visited before, add to the list
                if not connection.is_visited():
                    choices.append(connection)

            # if there are no unvisited connections available
            if len(choices) == 0:
                # get all connections of current station
                all_conns: List["Connection"] = self.current_station.connect
                # set default min length to length of all connections
                min_unvis_len: int = len(self.stations.stations.values())
                # set default max length to low number
                max_unvis_len: int = 0
                # set counter to check for unvisited connections
                unvis_counter: int = 0
                # initiate empty list
                unvis: List = []
                # save best current connection which is None
                best_conn = None
                # loop through all possible connections
                for conn in all_conns:
                    # get the next station of the connection
                    next: "Station" = conn.get_other_station(self.current_station)
                    # get all connections of next station
                    all_conns_next: List["Connection"] = next.connect

                    # loop through conns of next station
                    for next_conn in all_conns_next:
                        # if connection is not visited, add 1 to counter
                        # and add the connection to the unvis list
                        if not next_conn.is_visited():
                            unvis.append(next_conn)
                            unvis_counter += 1

                    # if parameter == 'min':
                    if amount == 'min':
                        # save length of list with least amount of connections
                        # and save the connection itself as the best connection
                        if 0 < len(unvis) < min_unvis_len:
                            min_unvis_len = len(unvis)
                            best_conn = conn

                    # if parameter == 'max':
                    if amount == 'max':
                        # save length of list with most amount of connections
                        # and save the connection itself as the best connection
                        if 0 < len(unvis) > max_unvis_len:
                            max_unvis_len = len(unvis)
                            best_conn = conn

                # if counter is 0, stop trajectory
                if unvis_counter == 0:
                    self.stop == True
                    # break out of while-loop
                    break
                # else, choose best_conn as next connection
                else:
                    next = best_conn

                self.check_time(next)

            else:
                # current station is set as station with best amount of connections
                best_con = None
                # empty list
                equals: List["Connection"] = []
                # loop through list with stations
                for connection in choices:
                    # get the station that is connected with each connection
                    station = connection.get_other_station(self.current_station)
                    # save the connection count of every station
                    con_count = len(station.connect)

                    # if there is no best_con yet, current con_count is set as best_con
                    if best_con == None:
                        best_con = con_count
                        equals.append(connection)
                    # save min amount of connections if parameter == 'min'
                    elif amount == 'min' and con_count < best_con:
                        best_con = con_count
                        # empty the list
                        equals = []
                        equals.append(connection)
                    # save max amount of connections if parameter == 'max'
                    elif amount == 'max' and con_count > best_con:
                        best_con = con_count
                        # empty the list
                        equals = []
                        equals.append(connection)

                    # if con_count of current station is equal to current
                    # best_con, append to list
                    elif con_count == best_con:
                        equals.append(connection)

                # choose next station randomly from list
                next = random.choice(equals)
                self.check_time(next)

        self.current_station.visit()

    def check_time(self, connection: "Connection") -> None:
        """Checks if requested map is of North- and South-Holland or of the
        Netherlands. Changes the amount of minutes the train may ride
        accordingly.
        Keeps track of the total time of the trajectory.

        Args:
            connections (Connection): a connection object.

        """
        if self.which_region == 'nl':
            max_time: int = 180
        elif self.which_region == 'holland':
            max_time: int = 120

        # keep track of the total time of the trajectory
        time: float = connection.time
        if self.time + time <= max_time:
            self.time = self.time + time
            self.add_station(connection)
        else:
            self.stop = True

    def add_station(self, connection: "Connection") -> None:
        """Follows the chosen connection and adds the next
        station to the trajectory.

        Args:
            connections (Connection): a connection object.

        """
        # get the next station
        other_station: "Station" = connection.get_other_station(self.current_station)

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
