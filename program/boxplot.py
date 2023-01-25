from .network_graph import Network
from .trajectory import Train
from .hillclimber import climb_hill
from statistics import mean

import matplotlib.pyplot as plt

def boxplot(iteration, which_regions = 'holland', start = 'random'):
    """Create a histogram of the baseline algorithm,
        showing only the viable outputs"""

    # initialise list for viable solutions
    solutions = []
    solutions1 = []
    solutions2 = []
    solutions3 = []

    # initialise counter of number of succesful runs
    succes = 0
    succes1 = 0
    succes2 = 0
    succes3 = 0

    # run the random algorithm x number of times
    for i in range(iteration):
        # k = run('greedy_time', which_regions, start)
        # k1 = run('greedy_conn', which_regions, start)
        # k2 = run('greedy_time', which_regions, start = 'min_con')
        k1 = run('greedy_conn', which_regions, start = 'min_con')

        # k = run('connect', which_regions, start)
        # k1 = run('connect_with', which_regions, start)
        # k2 = run('connect', which_regions, start = 'min_con')
        k = run('connect_with', which_regions, start = 'min_con')

        k2 = run('hillclimber', which_regions, start)
        # k1 = run('hillclimber', which_regions, start = 'min_con')

        # check if the output of the run is viable then append to initialised list
        if k != False:
            solutions.append(k)
            succes += 1
        
        if k1 != False:
            solutions1.append(k1)
            succes1 += 1
        
        # check if the output of the run is viable then append to initialised list
        if k2 != False:
            solutions2.append(k2)
            succes2 += 1
        
        # # check if the output of the run is viable then append to initialised list
        # if k3 != False:
        #     solutions3.append(k3)
        #     succes3 += 1
        
    # calculate the percentage of viable outputted solutions
    percentage_succes = (succes/iteration) * 100
    percentage_succes1 = (succes1/iteration) * 100
    percentage_succes2 = (succes2/iteration) * 100
    # percentage_succes3 = (succes3/iteration) * 100

    data = [solutions, solutions1, solutions2]

    # Creating plot
    plt.boxplot(data, showmeans=True)

    # set title and axis descriptions
    plt.title(f"Difference in objective function of Random, Greedy and Hillclimber algorithms, for {iteration} runs")
    plt.xlabel("Type algorithm")
    plt.ylabel("K values (objective function output)")
    plt.xticks([1, 2, 3], [f'Random +\nStart with min con\n(valid solutions: {percentage_succes}%)', f'Greedy +\nStart with min con\n(valid solutions: {percentage_succes1}%)', f'Hillclimber +\nStart with random station\n(valid solutions: {percentage_succes2}%)'])

    # save and show the histogram
    plt.savefig('output/boxplot_difference_nl.png')
    plt.show()

def run(algorithm, which_regions = 'holland', start = 'random'):
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
        
        if algorithm == 'connect':
            t.connect()
        elif algorithm == 'connect_with' or algorithm == 'hillclimber':
            t.connect_with_used()
        elif algorithm == 'greedy_time':
            t.greedy_time()
        elif algorithm == 'greedy_conn':
            t.greedy_conns()
        
        trains.append(t.trajectory)
        n.add_trajectory(t)

        if not algorithm == 'hillclimber':
            # calculate values for the objective function
            p_counter += t.station_counter
            min += t.time
            train_number += 1
            if t.time > max_min:
                max_min = t.time

    if algorithm == 'hillclimber':
        k = climb_hill(n, 100, which_regions, start)

    # check if the solution is valid (if all stations have been visited)
    if len(n.check_stations()) != 0:
        return False

    if not algorithm == 'hillclimber':
        # calculate parameters for objective function
        total_connections = len(n.connections)
        visited_connections = total_connections - len(n.check_connections())
        p = visited_connections/total_connections
        t = train_number - 1

        # calculate objective function and return its outcome
        k = p*10000 - (t*100 + min)
    
    return k
