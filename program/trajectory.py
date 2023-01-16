from .connection_node import Connection
import random

class Train():
    """Representation of a trajectory"""
    def __init__(self, name, network, choices):
        self.stations = network
        self.name = name
        self.stop = False
        self.time = 0
        self.current_station = self.choose_first_station(choices)
        self.trajectory = []
        self.station_counter = 0
    
    def choose_first_station(self, choices):
        """Chooses the first station randomly from the list of unvisited connections"""
        rand_connections = random.choice(choices)
        rand_station = random.choice([rand_connections.s1, rand_connections.s2])

        # add first station to trajectory list and set as visited
        self.trajectory.append(self.current_station.name)
        self.current_station.visit()
        return rand_station

    def connect(self):
        """Moves the current train to new possible connections 
            until all possible connections are visited"""
        while self.stop == False:
            # set choices as all connections from the current station
            choices = self.current_station.connect

            # if all connections have been visited
            if len(choices) == 0:
                # end the trajectory
                self.stop = True
            else:
                # choose next station randomly from the possible connections
                next = random.choice(choices)
                # if the connection has been visited before, remove from the list
                if next.is_visited() == True:
                    choices.remove(next)
                # else, choose this connection
                else:
                    self.add_station(next)


    def add_station(self, connection: "Connection"):
        """Follows the chosen connection and adds the next station to the trajectory"""
        # get the next station
        other_station = connection.get_other_station(self.current_station)

        # add the next station to the trajectory list
        self.trajectory.append(other_station.name)

        # keep track of the total time of the trajectory
        time = connection.time
        self.time = self.time + time

        # set the current station and connection as visited
        self.current_station.visit()
        connection.visit()

        # move to the next station
        self.current_station = other_station
        self.station_counter += 1

    def __repr__(self):
        return f"{self.name} visits {self.trajectory} in {self.time} minutes."
