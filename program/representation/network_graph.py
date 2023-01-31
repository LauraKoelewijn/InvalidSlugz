#   network_graph.py
#
#   Minor programmeren - Algoritmen en Heuristieken
#   RailNL case
#   Meike Klunder, Laura Koelewijn & Sacha Gijsbers
#
#   Implements the graph that holds all station and connection data
#   The class can give the unvisited stations and connections, 
#       trajectories can be added and removed
#       and the k_value can be calculated.

# import classes
from .station_node import Station # type: ignore
from .connection_node import Connection # type: ignore
from ..algorithms.trajectory import Train # type: ignore

# import type hints
from typing import Dict, List

class Network():
    """ A network class that holds the Graph with all connections and stations. 
        Also holds a solution trajecotry.
    """
    def __init__(self, source_file: str, source_file_neighbours: str) -> None:
        # take land data and load into the graph
        self.stations: Dict[str, Station] = self.load_stations(source_file)
        self.connections: List[Connection] = self.load_conns(source_file_neighbours)

        # Place to save solution trajectories
        self.trajectories: List[Train] = []
        self.total_minutes: float = 0

    # make nodes for every station with coordinates
    def load_stations(self, source_file: str) -> Dict[str, Station]:
        """ Loads the data from given file name into the self.stations dictionary. 

        Args:
            source_file (str): the name of the data file for the stations
                must be in data repository, so data/[source_file].csv.

        Returns:
            Dict[str, Station]: a dictionary with the 
                station names and station class instances
        """
        # initiate dict to fill with station nodes
        station_dict: Dict[str, Station] = {}

        # open the given file
        with open(source_file, 'r') as f:
            # skip first line
            next(f)

            # read every line in the file until EOF
            while True:
                line = f.readline()
                if not line:
                    break

                # split the line into station name and coordinate tuple
                splitline = line.split(",")
                splitline[-1] = splitline[-1].strip()

                # select needed information, name and coordinates of the station
                station = splitline[0]
                y = float(splitline[1])
                x = float(splitline[2])

                # create station node and add to dictionary
                station_dict[station] = Station(station, x, y)
        return station_dict

    def load_conns(self, source_file_neighbours: str) -> List[Connection]:
        """ Loads the data from given file name into the self.connections list

        Returns:
            List: list of stations in the file
        """
        # initiate list to fill with connection class instances
        conn_list: List[Connection] = []

        # open the ConnectiesHolland file
        with open(source_file_neighbours, 'r') as f:
            # skip first line
            next(f)

            # read every line in the file until EOF
            while True:
                line = f.readline()
                if not line:
                    break

                # split the lines into the two stations 
                # and the time it takes between them
                splitline = line.split(",")

                splitline[-1] = splitline[-1].strip()

                # string representations of the two stations and distance
                station1 = splitline[0]
                station2 = splitline[1]
                distance = float(splitline[2])

                # node representation of the two stations
                station_node1 = self.stations[station1]
                station_node2 = self.stations[station2]
                
                # make connection instance
                connection = Connection(station_node1, station_node2, distance)

                # adding connections to the created station nodes
                station_node1.add_conn(connection)
                station_node2.add_conn(connection)
                conn_list.append(connection)
        return conn_list

    def check_connections(self) -> List[Connection]:
        """ Checks for every connection in the network if it has been visited.

        Returns:
            List["Connection"]: a list with all the unvisited connections
        """
        # initialize empty list for unvisited connections
        unvis: List[Connection] = []

        # loop though all connections
        for conn in self.connections:
            # if the connection has not been visited yet, add to the list
            if not conn.is_visited():
                unvis.append(conn)
        return unvis

    def check_stations(self) -> List[Station]:
        """ Checks for every station in the network if it has been visited.

        Returns:
            List["Station"]: a list with all the unvisited connections
        """
        # initialize empty list for unvisited stations
        unvis: List[Station] = []

        # loop though all stations
        for station in self.stations.values():
            # if the station has not been visited yet, add to the list
            if not station.is_visited():
                unvis.append(station)
        return unvis

    def add_trajectory(self, train: Train, index: int = -1) -> None:
        """ Adds a given trajectory to the network
                at specific index, if given.
            Updates the trajectories list and the total minutes

        Args:
            train (Train): a train object to be added
            index (int): at what place in the list to add the train. Defaults to -1.
        """
        # if there's nothing in the list of the default -1 is used as index
        if len(self.trajectories) == 0 or index == -1:
            # just append the train to the list
            self.trajectories.append(train)
        else:
            # if a specific index is given, insert the train at that index
            self.trajectories.insert(index, train)

        # add trajectory's monutes to the total minutes
        self.total_minutes += train.time 

    def remove_trajectory(self, train: Train) -> None:
        """ Removes given trajectory from the network.
            Updates the trajectories list and total minutes

        Args:
            train (Train): a train object to be removed
        """
        # remove trajectory from the list
        self.trajectories.remove(train)

        # subtract trajectory's minutes from total minutes
        self.total_minutes -= train.time

    def calc_k(self) -> float:
        """ Calculates the k-value for the network's saved solution.

        Returns:
            float: the calculated k_value
        """
        # calculate fraction of visited connections
        total_connections = len(self.connections)
        visited_connections = total_connections - len(self.check_connections())
        p = visited_connections/total_connections

        # get amount of trajectories made
        t = len(self.trajectories)

        # calculate k
        k = p*10000 - (t*100 + self.total_minutes)
        return k
