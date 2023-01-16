from .connection_node import Connection
from typing import Dict, Tuple, List

class Station():
    def __init__(self, name: str, x, y) -> None:
        self.name: str = name
        self.connect: List["Connection"] = []
        self.visited: bool = False
        self.coord: Tuple[float] = [x, y]

    # adding connections to neighboring stations with time it takes to get there
    def add_conn(self, connection: "Connection") -> None:
        self.connect.append(connection)

    # change bool showing that the station is visited
    def visit(self):
        self.visited = True

    # check the status of the station if it is visited
    def is_visited(self):
        return self.visited

    # representation of the class in string form
    def __repr__(self):
        return f"{self.name} with {self.distances}\n."
