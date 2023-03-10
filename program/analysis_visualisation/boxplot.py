from ..representation.network_graph import Network # type: ignore
from ..algorithms.trajectory import Train # type: ignore
from ..algorithms.hillclimber import climb_hill, random_restart # type: ignore
from statistics import mean

import matplotlib.pyplot as plt # type: ignore
from typing import Union, List

def boxplot_start(iteration: int) -> None:
    """ Function that creates a boxplot comparing
        - the random with random start 
        - the random with start at minimal connection

    Args:
        iteration (int): how many times each algorithm is run
    """

    # initialise list for viable solutions
    solutions: List[float] = []
    solutions1: List[float] = []

    # run the algorithms the given number of times
    for i in range(iteration):

        k_random_rand = run('connect_with')
        k_random_mincon = run('connect_with', 'nl', 'min_con')

        # check if the output of the run is viable then append to initialised list
        if k_random_rand != False:
            solutions.append(k_random_rand)
        
        if k_random_mincon != False:
            solutions1.append(k_random_mincon)
        
    # make dataframe
    data = [solutions, solutions1]

    # Creating plot
    plt.boxplot(data, showmeans=True)

    # set title and axis descriptions
    plt.title(f"Difference in objective function of Random time algorithms, for {iteration} runs")
    plt.xlabel("Type algorithm")
    plt.ylabel("K values (objective function output)")
    plt.xticks([1, 2], [f'Random\nwith a random start', f'Random\nwith a min con start'])

    # save and show the plot
    plt.savefig('output/NL/Boxplots/boxplot_random_start_nl.png')
    plt.show()

def boxplot_time(iteration: int) -> None:
    """ Function that creates a boxplot comparing
        - the random 
        - the greedy for least time 
        - the greedy for most time

    Args:
        iteration (int): how many times each algorithm is run
    """

    # initialise list for viable solutions
    solutions: List[float] = []
    solutions1: List[float] = []

    # run the algorithms the given number of times
    for i in range(iteration):

        k_greedy_time_long = run('greedy_time_long', 'nl', 'min_con')
        k_greedy_time_short = run('greedy_time_short', 'nl', 'min_con')

        # check if the output of the run is viable then append to initialised list
        if k_greedy_time_long != False:
            solutions.append(k_greedy_time_long)
        
        if k_greedy_time_short != False:
            solutions1.append(k_greedy_time_short)
        
    # make dataframe
    data = [solutions, solutions1]

    # Creating plot
    plt.boxplot(data, showmeans=True)

    # set title and axis descriptions
    plt.title(f"Difference in K values of Greedy time algorithms, for {iteration} runs")
    plt.xlabel("Type algorithm")
    plt.ylabel("K values (objective function output)")
    plt.xticks([1, 2], [f'Greedy Time (Long, min con)', f'Greedy Time (Short, min con)'])

    # save and show the plot
    plt.savefig('output/NL/Boxplots/boxplot_difference_greedytime_nl.png')
    plt.show()

def boxplot_connections(iteration: int) -> None:
    """Function that creates a boxplot comparing
        - the greedy for least connections, starting at random station
        - the greedy for least connections, starting at stations with min_con
        or
        - the greedy for most connections, starting at random station
        - the greedy for most connections, starting at stations with min_con
        or
        - the greedy for least connections, starting at stations with min_con
        - the greedy for most connections, starting at stations with min_con

    Args:
        iteration (int): how many times each algorithm is run
    """

    # initialise list for viable solutions
    solutions: List[float] = []
    solutions1: List[float] = []

    # run the algorithms the given number of times
    for i in range(iteration):

        # k_greedy_con_min = run('greedy_conn_min')
        # k_greedy_con_max = run('greedy_conn_max')
        k_greedy_con_min_start = run('greedy_conn_min', 'nl', 'min_con')
        k_greedy_con_max_start = run('greedy_conn_max','nl', 'min_con')

        # check if the output of the run is viable then append to initialised list
        # if k_greedy_con_min != False:
        #     solutions.append(k_greedy_con_min)
        
        # if k_greedy_con_max != False:
        #     solutions.append(k_greedy_con_max)
        
        if k_greedy_con_min_start != False:
            solutions.append(k_greedy_con_min_start)
        
        if k_greedy_con_max_start != False:
            solutions1.append(k_greedy_con_max_start)
    
    # make dataframe
    data = [solutions, solutions1]

    # Creating plot
    plt.boxplot(data, showmeans=True)

    # set title and axis descriptions
    plt.title(f"Difference in K values of Greedy Con algorithms, for {iteration} runs")
    plt.xlabel("Type algorithm")
    plt.ylabel("K values (objective function output)")
    plt.xticks([1, 2], [f'Greedy Connection (Min)\nStart with min con', f'Greedy Connection (Max)\nStart with min con'])

    # save and show the plot
    plt.savefig('output/NL/Boxplots/boxplot_difference_greedyconn_nl.png')
    plt.show()

def boxplot_greedy(iteration: int) -> None:
    """ Function that creates a boxplot comparing
        - the random 
        - the greedy for least time 
        - the greedy for most time

    Args:
        iteration (int): how many times each algorithm is run
    """

    # initialise list for viable solutions
    solutions: List[float] = []
    solutions1: List[float] = []
    solutions2: List[float] = []

    # run the algorithms the given number of times
    for i in range(iteration):

        k_random_mincon = run('connect_with', 'nl', 'min_con')
        k_greedy_time_short = run('greedy_time_short', 'nl', 'min_con')
        k_greedy_con_min_start = run('greedy_conn_min', 'nl', 'min_con')

        # check if the output of the run is viable then append to initialised list
        if k_random_mincon != False:
            solutions.append(k_random_mincon)

        if k_greedy_time_short != False:
            solutions1.append(k_greedy_time_short)
        
        if k_greedy_con_min_start != False:
            solutions2.append(k_greedy_con_min_start)
        
    # make dataframe
    data = [solutions, solutions1, solutions2]

    # Creating plot
    plt.boxplot(data, showmeans=True)

    # set title and axis descriptions
    plt.title(f"Difference in K values of Greedy algorithms, for {iteration} runs")
    plt.xlabel("Type algorithm")
    plt.ylabel("K values (objective function output)")
    plt.xticks([1, 2, 3], [f'Random (min con)', f'Greedy Time (Short, min con)', f'Greedy Con (Min, min con)'])

    # save and show the plot
    plt.savefig('output/NL/Boxplots/boxplot_difference_greedy_nl.png')
    plt.show()

def boxplot_hill(iteration: int) -> None:
    """ Function that creates a boxplot comparing
        - the random with min con
        - the hillclimber with random with min con
        - the hillclimber with greedy with min con

    Args:
        iteration (int): how many times each algorithm is run
    """

    # initialise list for viable solutions
    solutions: List[float] = []
    solutions1: List[float] = []
    solutions2: List[float] = []

    # run the algorithms the given number of times
    for i in range(iteration):

        k_random_mincon = run('connect_with', 'nl', 'min_con')
        hill = climb_hill(True, 100,'connect_with', 'nl', 'min_con')[0]
        k_hill_rand = hill.calc_k()
        hill1 = climb_hill(True, 100,'greedy_time_short', 'nl', 'min_con')[0]
        k_hill_greedy = hill1.calc_k()

        # check if the output of the run is viable then append to initialised list
        if k_random_mincon != False:
            solutions.append(k_random_mincon)

        if k_hill_rand != False:
            solutions1.append(k_hill_rand)
        
        if k_hill_greedy != False:
            solutions2.append(k_hill_greedy)
        
    # make dataframe
    data = [solutions, solutions1, solutions2]

    # Creating plot
    plt.boxplot(data, showmeans=True)

    # set title and axis descriptions
    plt.title(f"Difference in K values of Hillclimber algorithms, for {iteration} runs")
    plt.xlabel("Type algorithm")
    plt.ylabel("K values (objective function output)")
    plt.xticks([1, 2, 3], [f'Random\n(min con)', f'Hillclimber\n(Random, min con)', f'Hillclimber\n(greedy time (short), min con)'])

    # save and show the plot
    plt.savefig('output/NL/Boxplots/boxplot_difference_hillclimb_nl.png')
    plt.show()

def boxplot_restart(iteration: int) -> None:
    """ Function that creates a boxplot comparing
        - the random with min con
        - the hillclimber with greedy with min con
        - restart hillclimber with greedy with min con

    Args:
        iteration (int): how many times each algorithm is run
    """

    # initialise list for viable solutions
    solutions: List[float] = []
    solutions1: List[float] = []
    solutions2: List[float] = []

    # run the algorithms the given number of times
    for i in range(iteration):

        k_random_mincon = run('connect_with', 'nl', 'min_con')
        hill = climb_hill(True, 100,'greedy_time_short', 'nl', 'min_con')[0]
        k_hill_greedy = hill.calc_k()
        sol = random_restart(100, 100, 'greedy_time_short', 'nl', 'min_con', tell_me = True)[0]
        k_restart = sol.calc_k()

        # check if the output of the run is viable then append to initialised list
        if k_random_mincon != False:
            solutions.append(k_random_mincon)
        
        if k_hill_greedy != False:
            solutions1.append(k_hill_greedy)
        
        if k_restart != False:
            solutions2.append(k_restart)
        
    # make dataframe
    data = [solutions, solutions1, solutions2]

    # Creating plot
    plt.boxplot(data, showmeans=True)

    # set title and axis descriptions
    plt.title(f"Difference in K values of Restart Hillclimb algorithms, for {iteration} runs")
    plt.xlabel("Type algorithm")
    plt.ylabel("K values (objective function output)")
    plt.xticks([1, 2, 3], [f'Random\n(min con)', f'Hillclimber\n(greedy time (short), min con)', f'Hillclimber restart\n(greedy time (short), min con)'])

    # save and show the plot
    plt.savefig('output/NL/Boxplots/boxplot_difference_restart_nl.png')
    plt.show()

def boxplot_eind(iteration: int) -> None:
    """ Function that creates a boxplot that compares:
        - the baseline algorithm
        - the greedy for shortest time
        - the hillclimber
        - the random restart hillclimber

    Args:
        iteration (int): how many times each algorithm is run
    """

    # initialise list for viable solutions
    solutions: List[float] = []
    solutions1: List[float] = []
    solutions2: List[float] = []
    solutions3: List[float] = []

    # run every algorithm the given number of times
    for i in range(iteration):

        k_random = run('connect_with', 'nl', 'min_con')
        k_greedy_conn = run('greedy_time_short', 'nl', 'min_con')

        hill = climb_hill(True, 100, 'greedy_time_short', 'nl', 'min_con')[0]
        k_hill_greedy = hill.calc_k()
        
        sol = random_restart(100, 100, 'greedy_time_short', 'nl', 'min_con', tell_me = True)[0]
        k_restart = sol.calc_k()

        # check if the output of the run is viable then append to initialised list
        if k_random != False:
            solutions.append(k_random)
        
        if k_greedy_conn != False:
            solutions1.append(k_greedy_conn)
        
        if k_hill_greedy != False:
            solutions2.append(k_hill_greedy)
        
        if k_restart != False:
            solutions3.append(k_restart)

    # make dataframe with all lists
    data = [solutions, solutions1, solutions2, solutions3]

    # Creating plot
    plt.boxplot(data, showmeans=True)

    # set title and axis descriptions
    plt.title(f'Difference in objective function of Random, Greedy and Hillclimber algorithms, for {iteration} runs')
    plt.xlabel('Type algorithm')
    plt.ylabel('K values (objective function output)')
    plt.xticks([1, 2, 3, 4], [f'Random', f'Greedy Time\n(Short, min con)', f'Hillclimber Greedy Time\n(Short, min con)', f'Hillclimber Restart\nGreedy Time (Short, min con)'])

    # save and show the plot
    plt.savefig('output/boxplot_difference_nl.png')
    plt.show()

def lineplot() -> None:
    """ Function that creates a linepllot showing one hillclimber run using
        - the random algorithm
        - the greedy for least time algorithm
        - the greedy for most connections algorithm
    """
    # run every hillclimber once
    hill_random = climb_hill(True, 10000, 'connect_with')
    k_random = hill_random[1]

    hill_greedy_time = climb_hill(True, 10000, 'greedy_time_min')
    k_greedy_time = hill_greedy_time[1]

    hill_greedy_conn = climb_hill(True, 10000, 'greedy_conn_max')
    k_greedy_conn = hill_greedy_conn[1]  

    # plot the three lines
    fig, ax = plt.subplots()
    ax.plot(k_random, label = 'Random')
    ax.plot(k_greedy_time, label = 'Greedy Time')
    ax.plot(k_greedy_conn, label = 'Greedy Conn')

    # add legend
    ax.legend()

    # save and show the plot
    plt.savefig('output/lineplot_difference_nl.png')
    plt.show()

def line_random_restart(iters: int, stop_after: int):
    """ Function that makes a lineplot of one run of the random restart algorithm 
    """
    # run the random restart
    random = random_restart(iters, stop_after, 'greedy_conn_min', tell_me=True)[1]

    # plot the k-value for every iteration in the random restart
    plt.plot(random)
    plt.xlabel('iteraties')
    plt.ylabel('k-waarde')
    plt.savefig('output/nl/Lineplot/lineplot_random_restart_once.png')
    plt.show()
    

def run(algorithm: str, which_regions: str = 'nl', start: str = 'random') -> Union[float, bool]:
    """ Function that runs the given algorithm
        and retunrs the k-value for the end result if all stations have been visited 
        or false if not all stations have been visited.

    Args:
        algorithm (str): which algorothm to use
        which_regions (str, optional): which region to analyse. Defaults to 'nl'.
        start (str, optional): which starting condition to use. Defaults to 'random'.

    Returns:
        Union[float, bool]: the k-value for the resulting solution 
                            or false if the solution doesn't visit all stations
    """
    
    # set the right region
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

    # make trajectories until all stations have been visited
    # and no more than the max number of trains have been initialised
    train_number = 1
    while len(n.check_stations()) > 0 and train_number <= traj_num:
        t = Train(f'train_{train_number}', n, which_regions, start)
        
        if algorithm == 'connect':
            t.connect()
        elif algorithm == 'connect_with':
            t.connect_with_used()
        elif algorithm == 'greedy_time_long':
            t.greedy_time('long')
        elif algorithm == 'greedy_time_short':
            t.greedy_time('short')
        elif algorithm == 'greedy_conn_min':
            t.greedy_conns('min')
        elif algorithm == 'greedy_conn_max':
            t.greedy_conns('max')
        
        trains.append(t.trajectory)
        n.add_trajectory(t)

    # check if the solution is valid (if all stations have been visited)
    if len(n.check_stations()) != 0:
        return False

    #calculate objective function and return its outcome
    k = n.calc_k()
    return k
