from .connection_node import Connection
from typing import Dict, Tuple, List

class Station():
    def __init__(self, name: str, x, y) -> None:
        self.name: str = name
        self.connect: List["Connection"] = []
        self.visited: bool = False
        self.times_visited = 0
        self.coord: Tuple[float] = [x, y]

    # adding connections to neighboring stations with time it takes to get there
    def add_conn(self, connection: "Connection") -> None:
        self.connect.append(connection)

    # change bool showing that the station is visited
    def visit(self):
        self.visited = True
        self.times_visited += 1
    
    def unvisit(self):
        self.times_visited -= 1
        if self.times_visited == 0:
            self.visited = False
        elif self.times_visited < 0:
            raise ValueError("cannot visit station negative times")

    # check the status of the station if it is visited
    def is_visited(self):
        return self.visited

    # representation of the class in string form
    def __repr__(self):
        return f"Station {self.name}\n."
