class Station():
    def __init__(self) -> None:
        self.connect = {}
        self.visited = False
        self.coor = []

    def add_conn(self, location, time):
        self.connect[location] = time

    def add_coor(self, x, y):
        self.coor = [x, y]

    def been(self):
        self.visited = True

    def is_visited(self):
        return self.visited
