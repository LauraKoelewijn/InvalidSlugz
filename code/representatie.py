class Station():
    def __init__(self, name: str) -> None:
        self.name = name
        self.connect = {}
        self.visited = False
        self.coord = []

    def add_conn(self, location, time):
        self.connect[location] = time

    def add_coord(self, x, y):
        self.coord = [x, y]

    def been(self):
        self.visited = True

    def is_visited(self):
        return self.visited

    def __repr__(self):
        return f"{self.name} at {self.coord} with {self.connect}." 

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