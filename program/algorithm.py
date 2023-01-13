from .network_graph import Network
from .trajectory import Train
import csv

def csv_file():
    with open('output/output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        header = ["train", "stations"]
        writer.writerow(header)

        n = Network('data/StationsHolland.csv', 'data/ConnectiesHolland.csv')
    
        for traj in range(3):
            t = Train(f'train_{traj+1}', n)
            t.connect()

            writer.writerow([t.name, t.trajectory])
