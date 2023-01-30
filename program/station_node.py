# import classes
from .connection_node import Connection

# import type hints
from typing import Dict, Tuple, List

class Station():
    """ A class that holds the information for a station object:
        - name
        - the connections it has
        - coordinates
        - if it's been visited
    """
    def __init__(self, name: str, x: float, y: float) -> None:
        self.name: str = name
        self.connect: List["Connection"] = []
        self.visited: bool = False
        self.coord: Tuple[float] = [x, y]
        self.times_visited: int = 0
        
    def add_conn(self, connection: "Connection") -> None:
        """ Adds the given connection to this station.

        Args:
            connection (Connection): a connection between this and another station
        """
        self.connect.append(connection)

    # change bool showing that the station is visited
    def visit(self):
        """ Keeps track if and how many times this station has been visited
        """
        self.visited = True
        self.times_visited += 1
    
    def unvisit(self):
        """ Undoes the visit() function

        Raises:
            ValueError: The times_visited cannot get negative
        """
        self.times_visited -= 1
        if self.times_visited == 0:
            self.visited = False
        elif self.times_visited < 0:
            raise ValueError("Cannot visit station negative times")

    # check the status of the station if it is visited
    def is_visited(self) -> bool:
        """ Checks if the station has been visited before

        Returns:
            bool: whether the station has been visited
        """
        return self.visited

    def __repr__(self) -> str:
        """ Gives the string representation of the station

        Returns:
            str: the name of the station
        """
        return f"Station {self.name}\n."