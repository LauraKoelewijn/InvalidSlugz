from typing import Dict, Tuple

class Station():
    def __init__(self, name: str, x, y) -> None:
        self.name: str = name
        self.connect: Dict[str, "Station"] = {}
        self.distances: Dict[str, int] = {}
        self.visited: bool = False
        self.coord: Tuple[float] = [x, y]

    # adding connections to neighboring stations with time it takes to get there
    def add_conn(self, name: str, location: "Station", time: int) -> None:
        self.connect[name] = location
        self.distances[name] = time

    # change bool showing that the station is visited
    def visit(self):
        self.visited = True

    # check the status of the station if it is visited
    def is_visited(self):
        return self.visited

    # representation of the class in string form
    def __repr__(self):
        return f"at {self.coord} with {self.distances}\n." 

class Train():
    def __init__(self, name):
        self.name = name
        self.trajectory = []
        self.time = 0

    def add_station(self, station: "Station", time: int):
        self.trajectory.append(station)
        self.time = self.time + time

    def __repr__(self):
        return f"{self.name} visits {self.trajectory} in {self.time} minutes."