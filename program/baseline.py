from .network_graph import Network
from .trajectory import Train

import matplotlib.pyplot as plt

def hist(iteration):
    """Create a histogram of the baseline algorithm, 
        showing only the viable outputs"""

    # initialise list for viable solutions
    solutions = []

    # initialise counter of number of succesful runs
    succes = 0

    # run the random algorithm x number of times
    for i in range(iteration):
        k = run()

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

    # save and show the histogram
    plt.savefig('output/baseline_hist.png')
    plt.show()


def run():
    """run the random algorithm and return a objective function output
            or a bool, showing that it is not a viable output"""

    # initialise an empty list of trajectories
    trains = []

    # create a network
    n = Network('data/StationsHolland.csv', 'data/ConnectiesHolland.csv')

    p_counter = 0
    min = 0
    max_min = 0

    # make trains/trajectories until all stations have been visited 
    # and no more than 7 trains have been initialised
    train_number = 1
    while len(n.check_stations()) > 0 and train_number <= 7:
        t = Train(f'train_{train_number}', n)
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
