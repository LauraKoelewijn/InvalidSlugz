from .network_graph import Network
from .trajectory import Train
import csv

def run():
    trains = []

    with open('output/output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        header = ["train", "stations"]
        writer.writerow(header)

        n = Network('data/StationsHolland.csv', 'data/ConnectiesHolland.csv')

        p_counter = 0
        min = 0
        max_min = 0

        # make three trains/trajectories
        train_number = 1
        while len(n.check_stations()) > 0 and train_number <= 7:
            t = Train(f'train_{train_number}', n)
            # choose which baseline to use
            # t.connect_with_used()
            t.connect()
            trains.append(t.trajectory)

            # make good string representation without quotation marks
            str_repr = f'[%s]' % ', '.join(map(str, t.trajectory))

            # write the name and stations of the train to the output file
            writer.writerow([t.name, str_repr])
            p_counter += t.station_counter
            min += t.time
            train_number += 1
            if t.time > max_min:
                max_min = t.time

        print(max_min)

        # calculate parameters for objective function
        total_connections = len(n.connections)
        visited_connections = total_connections - len(n.check_connections())
        p = visited_connections/total_connections
        t = train_number - 1

        # put objective function into output file
        k = p*10000 - (t*100 + min)
        writer.writerow(["score", k])

    return n, trains
