from .representation.network_graph import Network
from .algorithms.trajectory import Train
from .algorithms.hillclimber import climb_hill, random_restart
import csv

def write_to_csv(network):
    # open a new csv file to write the solution in
    with open('output/solution.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')

        # write the header
        header = ["train", "stations"]
        writer.writerow(header)
        
        # loop through the trajectories saved in the network
        for train in network.trajectories:
            # make good string representation without quotation marks
            str_repr = f'[%s]' % ', '.join(map(str, train.trajectory))

            # write the name and stations of the train to the output file
            writer.writerow([train.name, str_repr])

        # calculate and add k-value
        k = network.calc_k()
        writer.writerow(["score", k])


def run(which_regions = 'holland', start = 'random'):
    trains = []

    if which_regions == 'nl':
        traj_num = 20
        data_stations = 'data/case_data/StationsNationaal.csv'
        data_connections = 'data/case_data/ConnectiesNationaal.csv'
    elif which_regions == 'holland':
        traj_num = 7
        data_stations = 'data/case_data/StationsHolland.csv'
        data_connections = 'data/case_data/ConnectiesHolland.csv'

    with open('output/output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        header = ["train", "stations"]
        writer.writerow(header)

        n = Network(data_stations, data_connections)

        # p_counter = 0
        # min = 0
        max_min = 0

        # make the trains/trajectories
        train_number = 1
        while len(n.check_stations()) > 0 and train_number <= traj_num:
            t = Train(f'train_{train_number}', n, which_regions, start)
            # choose which algorithm to use
            # t.greedy_time('short') # choose between 'long' or 'short'
            t.greedy_conns('min') # choose between 'min' or 'max'
            # t.connect_with_used()
            # t.connect()
            trains.append(t.trajectory)
            #print(t.object_traj)
            n.add_trajectory(t)

            # make good string representation without quotation marks
            str_repr = f'[%s]' % ', '.join(map(str, t.trajectory))

            # write the name and stations of the train to the output file
            writer.writerow([t.name, str_repr])
            # p_counter += t.station_counter
            # min += t.time
            train_number += 1
            if t.time > max_min:
                max_min = t.time

        print(max_min)

        # # calculate parameters for objective function
        # total_connections = len(n.connections)
        # visited_connections = total_connections - len(n.check_connections())
        # p = visited_connections/total_connections
        # t = train_number - 1

        # # put objective function into output file
        # k = p*10000 - (t*100 + min)
        k = n.calc_k()
        writer.writerow(["score", k])

    #climb_hill(n, 1000, which_regions, start)
    # random_restart(n, 1500, which_regions, start)

    return n, trains
