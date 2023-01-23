def greedy_conns(self):
    """Moves current train to next possible stations by choosing
    the station that holds the least amount of connections, until all
    possible connections are visited. If there are no unvisited connections,
    it chooses a random connection."""
    while self.stop == False:
        # initiate empty list to put unvisited connection
        choices = []

        # loop though all connections
        for connection in self.current_station.connect:
            # if the connection hasn't been visited before, add to the list
            if not connection.is_visited():
                choices.append(connection)

        # if there are no unvisited connections available
        if len(choices) == 0:
            # choose a random connection
            all_conns = self.current_station.connect
            next = random.choice(all_conns)
            self.check_time(next)
        else:
            # current station is set as station with minimal connections
            min_con = self.current_station
            # loop through list with stations
            for station in choices:
                # save the connection count of every station
                con_count = len(station.connect)
                # if the connection count is less than the count of current station
                # with minimal connections, set new station as min_con
                if con_count < min_con:
                    min_con = con_count
                    next = station

        # add station to trajectory list and set as visited
        # if the connection has been visited before, remove from the list
        # WAAR MOET DE CHECK TIME??
        # self.check_time(next)
        self.trajectory.append(next.name)
        next.visit()
