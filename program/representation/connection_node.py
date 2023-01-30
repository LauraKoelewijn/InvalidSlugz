#   connection_node.py
#
#   Minor programmeren - Algoritmen en Heuristieken
#   RailNL case
#   Meike Klunder, Laura Koelewijn & Sacha Gijsbers
#
#   Implements the connection node that holds data for the connections between stations.
#   Connections can be (un)visited and
#       when one station is known, the other station at this connection can be requested
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .station_node import Station # type: ignore

class Connection():
    """ A class that holds the data for a connection:
        - two stations
        - the time between those stations
        - if it's been visited
    """
    def __init__(self, s1: 'Station', s2: 'Station', time: float):
        self.s1: 'Station' = s1
        self.s2: 'Station' = s2
        self.time: float = time
        self.visited: bool = False
        self.times_visited: int = 0

    def is_visited(self) -> bool:
        """ Checks whether the connection has been visited

        Returns:
            bool: whether the connection has been visited
        """
        return self.visited

    def visit(self):
        """Set current connection as visited"""
        self.visited = True
        self.times_visited += 1

    def unvisit(self):
        """ Undoes the visit() function

        Raises:
            ValueError: The times_visited cannot get negative
        """
        # update times_visited
        self.times_visited -= 1

        # update visited based on times_visited
        if self.times_visited == 0:
            self.visited = False
        elif self.times_visited < 0:
            raise ValueError("cannot visit connection negative times")

    def get_other_station(self, station: 'Station'):
        """ Gets the station that is connected to the given station
                via this connection

        Args:
            station (Station): a Station instance

        Returns:
            Station or bool: if the inputted station is connected via this connection,
                                it returns the other station in the connection, 
                                otherwise False.
        """
        if station == self.s1:
            return self.s2
        elif station == self.s2:
            return self.s1
        else:
            return False
