class Connection():
    def __init__(self, s1, s2, time):
        self.s1 = s1
        self.s2 = s2
        self.time = time
        self.visited = False
        self.times_visited = 0

    def is_visited(self):
        """Check if the current connection is visited"""
        return self.visited

    def visit(self):
        """Set current connection as visited
        """
        self.visited = True
        self.times_visited += 1
    
    def unvisit(self):
        self.times_visited -= 1
        if self.times_visited == 0:
            self.visited = False
        elif self.times_visited < 0:
            raise ValueError("cannot visit connection negative times")

    def get_other_station(self, station):
        """ Gets the other station that is connected to the other station via this connection

        Args:
            station (Station): a Station instance

        Returns:
            Station or bool: if the inputted station is connected via this connection,
                                it returns the other station in the connection,  otherwise False.
        """
        if station == self.s1:
            return self.s2
        elif station == self.s2:
            return self.s1
        else:
            return False
    # 
    def __repr__(self):
        return f"{self.s1} & {self.s2}"
    #     return f"verbinding tussen {self.s1} en {self.s2} in {self.time} minuten"
