from station_node import Station
import random

class Train():
    def __init__(self, name, network):
        self.stations = network
        self.name = name
        self.stop = False
        self.time = 0
        self.current_station = random.choice(list(self.stations.stations.values()))
        self.trajectory = [self.current_station.name]

    def connect(self):        
        while self.stop == False:
            choices = list(self.current_station.connect.values())
            visit_count = 0
            for item in choices:
                if item.is_visited():
                    visit_count += 1
            
            if visit_count == len(choices):
                self.stop = True

            next = random.choice(choices)
            if next.is_visited() == True:
                choices.remove(next)
            else:
                self.add_station(next)

                
    def add_station(self, station: "Station"):
        print(f"current: {self.current_station}")
        print(f"next: {station}")

        self.trajectory.append(station.name)
        time = self.current_station.distances[station.name]
        self.time = self.time + time
        self.current_station.visit()
        self.current_station = station
    
    # def get_traj(self):
    #     return self.trajectory

    def __repr__(self):
        return f"{self.name} visits {self.trajectory} in {self.time} minutes."

# n = Network('../data/StationsHolland.csv', '../data/ConnectiesHolland.csv')
# t = Train('train_1', n)
# t.connect()
# print(t)