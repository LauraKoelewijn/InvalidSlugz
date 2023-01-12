from representatie import Station

def load_coords():
    connecties = "../data/StationsHolland.csv"
    station_list = []

    # open the ConnectiesHolland file
    with open(connecties) as f:
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

            station = splitline[0]
            y = float(splitline[1])
            x = float(splitline[2])

            new_station = Station(station)
            new_station.add_coord(x, y)
            station_list.append(new_station)

    return station_list


def load_conns(station_list):
    """Function that loads the 'ConnectiesHolland' file into a list of stations

    Returns:
        List: list of stations in the file
    """

    connecties = "../data/ConnectiesHolland.csv"

    # open the ConnectiesHolland file
    with open(connecties) as f:
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

            station1 = splitline[0]
            station2 = splitline[1]
            distance = int(splitline[2])
            
            for place in station_list:
                if station1 == place.name:
                    place.add_conn(station2, distance)

                if station2 == place.name:
                    place.add_conn(station1, distance)
            
    return station_list

def load_all():
    return load_conns(load_coords())