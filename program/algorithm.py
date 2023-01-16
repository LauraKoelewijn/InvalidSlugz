from .network_graph import Network
from .trajectory import Train
import csv

def csv_file():
    with open('output/output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        header = ["train", "stations"]
        writer.writerow(header)

        n = Network('data/StationsHolland.csv', 'data/ConnectiesHolland.csv')

        p_counter = 0
        min = 0

        # amek three trains/trajectories
        for traj in range(3):
            t = Train(f'train_{traj + 1}', n)
            t.connect()

            # make good string representatioon without quotation marks
            str_repr = f'[%s]' % ', '.join(map(str, t.trajectory))

            #write the name and stations of the train to the output file
            writer.writerow([t.name, str_repr])
            p_counter += t.station_counter
            min += t.time

        # calculate parameters for objective function
        p = p_counter/28
        t = traj + 1

        # put objective function into output file
        k = p*10000 - (t*100 + min)
        writer.writerow(["score", k])
