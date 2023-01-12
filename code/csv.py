from representatie import Station, Train
from load import load_all
import csv
import random

def make_trajectory():
    train = Train()
    stations = load_all()

    station1 = random.choice(stations)
    train.add_station(station1)

    # TO DO: choose between stations' connections to make a trajectory
    # load trajectory into the csv file to make output

def csv_file(train: str, stations: str):
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, deliminator = ',')
        header = ["train", "station"]
        writer.writerow(header)





