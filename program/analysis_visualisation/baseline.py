#   algorithm.py
#
#   Minor programmeren - Algoritmen en Heuristieken
#   RailNL case
#   Meike Klunder, Laura Koelewijn & Sacha Gijsbers
#
#   Holds functions that create a histogram for our baseline using our
#   random algorithm, and calculates the K-value and returns it if the solution
#   is valid.
 
# import
from ..representation.network_graph import Network # type: ignore
from ..algorithms.trajectory import Train # type: ignore
from statistics import mean # type: ignore

import matplotlib.pyplot as plt # type: ignore
from typing import List, Union

def hist(iteration: int, which_regions: str = 'holland', start: str = 'random') -> None:
    """Functions that creates a histogram of the baseline algorithm,
    showing only the viable outputs

    Args:
        iteration (int): how many times you want to run the program
        which_regions (str): 'holland' or 'nl' depending on which region you want
        start (str): random or min_con
    """

    # initialise list for viable solutions
    solutions: List[float] = []

    # initialise counter of number of succesful runs
    succes: int = 0

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

def run(which_regions: str = 'holland', start: str = 'random') -> Union[float, bool]:
    """Runs the random algorithm and return a objective function output
    or a bool, showing that it is not a viable output.

    Args:
        which_regions (str): 'holland' or 'nl' depending on which region you want
        start (str): random or min_con


    Returns:
        k, or False (Union[float, bool]): returns the K-value if the solution
        is valid, else returns False.
    """

    if which_regions == 'nl':
        traj_num = 20
        data_stations = 'data/case_data/StationsNationaal.csv'
        data_connections = 'data/case_data/ConnectiesNationaal.csv'
    elif which_regions == 'holland':
        traj_num = 7
        data_stations = 'data/case_data/StationsHolland.csv'
        data_connections = 'data/case_data/ConnectiesHolland.csv'

    # initialise an empty list of trajectories
    trains: List[List[str]] = []

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
