from .network_graph import Network
from .trajectory import Train
from statistics import mean

import matplotlib.pyplot as plt

def hist(iteration, which_regions = 'holland', start = 'random'):
    """Create a histogram of the baseline algorithm,
        showing only the viable outputs"""

    # initialise list for viable solutions
    solutions = []

    # initialise counter of number of succesful runs
    succes = 0

    # run the random algorithm x number of times
    for i in range(iteration):
        k = run(which_regions, start)

        # check if the output of the run is viable then append to initialised list
        if k != False:
            solutions.append(k)
            succes += 1

    # calculate the percentage of viable outputted solutions
    percentage_succes = (succes/iteration) * 100

    # plot a histogram of the data devided in 10 bins
    plt.style.use('ggplot')
    plt.hist(solutions, bins=10)

    # set title and axis descriptions
    plt.title(f"Baseline functionality (valid solutions: {percentage_succes} %), {iteration} runs")
    plt.xlabel("K values (objective function output)")
    plt.ylabel("Frequency")

    plt.axvline(mean(solutions), color = 'k', linestyle = 'dashed')
    min_ylim, max_ylim = plt.ylim()
    plt.text(mean(solutions) * 1.01, max_ylim * 0.9, 'Mean: {:.2f}'.format(mean(solutions)))

    # save and show the histogram
    plt.savefig('output/baseline_hist_no_bias.png')
    plt.show()

def run(which_regions = 'holland', start = 'random'):
    """run the random algorithm and return a objective function output
            or a bool, showing that it is not a viable output"""

    if which_regions == 'nl':
        traj_num = 20
        data_stations = 'data/StationsNationaal.csv'
        data_connections = 'data/ConnectiesNationaal.csv'
    elif which_regions == 'holland':
        traj_num = 7
        data_stations = 'data/StationsHolland.csv'
        data_connections = 'data/ConnectiesHolland.csv'

    # initialise an empty list of trajectories
    trains = []

    # create a network
    n = Network(data_stations, data_connections)

    p_counter = 0
    min = 0
    max_min = 0

    # make trains/trajectories until all stations have been visited
    # and no more than 7 trains have been initialised
    train_number = 1
    while len(n.check_stations()) > 0 and train_number <= traj_num:
        t = Train(f'train_{train_number}', n, which_regions, start)
        t.connect()
        trains.append(t.trajectory)

        # calculate values for the objective function
        p_counter += t.station_counter
        min += t.time
        train_number += 1
        if t.time > max_min:
            max_min = t.time

    # check if the solution is valid (if all stations have been visited)
    if len(n.check_stations()) != 0:
        return False

    # calculate parameters for objective function
    total_connections = len(n.connections)
    visited_connections = total_connections - len(n.check_connections())
    p = visited_connections/total_connections
    t = train_number - 1

    # calculate objective function and return its outcome
    k = p*10000 - (t*100 + min)
    return k
