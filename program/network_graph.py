from .station_node import Station

from typing import Dict

class Network():
    def __init__(self, source_file, source_file_neighbours):
        self.stations: Dict[str, "Station"] = self.load_stations(source_file)
        self.load_conns(source_file_neighbours)

    # make nodes for every station with coordinates
    def load_stations(self, source_file):

        # initiate dict to fill with station nodes
        station_dict = {}

        # open the ConnectiesHolland file
        with open(source_file, 'r') as f:
            # skip first line
            next(f)

            # read every line in the file until EOF
            while True:
                line = f.readline()
                if not line:
                    break

                # split the lines into the two stations and the time it takes between them
                splitline = line.split(",")
                splitline[-1] = splitline[-1].strip()

                # select needed information, name and coordinates of the station
                station = splitline[0]
                y = float(splitline[1])
                x = float(splitline[2])

                # create station node and add to dictionary
                station_dict[station] = Station(station, x, y)

        return station_dict


    def load_conns(self, source_file_neighbours):
        """Function that loads the 'ConnectiesHolland' file into a list of stations

        Returns:
            List: list of stations in the file
        """

        # open the ConnectiesHolland file
        with open(source_file_neighbours, 'r') as f:
            # skip first line
            next(f)

            # read every line in the file until EOF
            while True:
                line = f.readline()
                if not line:
                    break

                # split the lines into the two stations and the time it takes between them
                splitline = line.split(",")

                splitline[-1] = splitline[-1].strip()

                # string representations of the two stations and distance
                station1 = splitline[0]
                station2 = splitline[1]
                distance = int(splitline[2])

                # node representation of the two stations
                station_node1 = self.stations[station1]
                station_node2 = self.stations[station2]

                # adding connections to the created node stations
                station_node1.add_conn(station2, station_node2, distance)
                station_node2.add_conn(station1, station_node1, distance)

    # string representation of station names with connected information in station nodes
    def __repr__(self):
        return f"{self.stations}"
