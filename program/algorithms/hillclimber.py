#   hillclimber.py
#
#   Minor programmeren - Algoritmen en Heuristieken
#   RailNL case
#   Meike Klunder, Laura Koelewijn & Sacha Gijsbers
#
#   Implements a hillclimber algorithm, that:
#   - removes a trajectory from a solution
#   - makes a new trajectory ysing one of the other algorithms (random, greedy, etc)
#   - adds this trajectory to the solution
#   - if the k-value of this solution is better that the first, this one is kept
#
#   climb_hill can be used to:
#   - run one hillclimber and end up in a local optimum (just_hillclimb = True)
#   - run a random restart (just_hillclimb = False), which:
#       - runs the hillclimber until it doesn't find new solutions
#       - restarts the hillclimber at a random new solution
#       - gives the best solution from all restarts

from .trajectory import Train # type: ignore
from ..representation.network_graph import Network # type: ignore

import copy
import random
from typing import List, Tuple, Union

def climb_hill(just_hillclimb: bool, iter_or_condstop: int, algorithm: str, which_regions: str = 'nl', start: str  = 'random') -> Tuple[Network, List[float]]:
    """Funtion that executes the hillclimber algorithm.
        It generates a network and then:
            it randomly chooses a trajectory to delete
            it makes a new trajectory
            if the new solution is better then the last one, it is saved

    Args:
        just_hillclimb (bool): whether just one hillclimber is used or the random restart
        iter_or_condstop (int): how many iterations the algorithm should do
            or, when using random restart, after how many non-changes it should restart
        algorithm (str): which algorithm should be used for the making of the trajectories
            (connect, connect_whith, greedy_time_long/short, greedy_conn_min/max)
        which_regions (str): which region to analyse (nl or holland)
        start (str): which starting heuristic to use (random or min_con)

    Returns:
        Network: a the network with the best solution found
        List[float]: a list with the k-values of all intermediate solutions
    """
    # set the region
    if which_regions == 'nl':
        traj_num = 20
        data_stations = 'data/case_data/StationsNationaal.csv'
        data_connections = 'data/case_data/ConnectiesNationaal.csv'
    elif which_regions == 'holland':
        traj_num = 7
        data_stations = 'data/case_data/StationsHolland.csv'
        data_connections = 'data/case_data/ConnectiesHolland.csv'
    
    # make an empty network
    network = Network(data_stations, data_connections)

    # make the trains/trajectories
    train_number = 1
    while len(network.check_stations()) > 0 and train_number <= traj_num:
        t = Train(f'train_{train_number}', network, which_regions, start)
        # choose which algorithm to use
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
        else:
            raise ValueError('please choose a valid algorithm name')

        # add the trajectory to the solution
        network.add_trajectory(t)
        train_number += 1

    # set starting solution to first best solution
    best_solution = network

    # make list of hillclimber outcomes
    list_solutions: List[float] = [best_solution.calc_k()]

    # if only one hillclimber is ran
    if just_hillclimb:
        # go for given amount of iterations
        for i in range(iter_or_condstop):
            # find another solution
            outcome = hill_step(best_solution, algorithm, which_regions, start)

            # if the new solution is better than the best now
            if outcome.calc_k() > best_solution.calc_k():
                 # set the new one as the best
                best_solution = outcome
                list_solutions.append(best_solution.calc_k())
            else:
                list_solutions.append(best_solution.calc_k())
    # if the random restart is used
    else:
        # set counter for found solutions that were not better
        check_stop = 0
        go = True
        while go:
            # find another solution
            outcome = hill_step(best_solution, algorithm, which_regions, start)

            # if the new solution is better than the best now
            if outcome.calc_k() > best_solution.calc_k():
                # set the new one as the best
                best_solution = outcome
                list_solutions.append(best_solution.calc_k())
                check_stop = 0
            else:
                list_solutions.append(best_solution.calc_k())
                check_stop += 1

            # if no new solution has been found for the given condition, stop the hillclimb
            if check_stop >= iter_or_condstop:
                go = False

    # return k for best solution network
    return best_solution, list_solutions  

def hill_step(start_network: Network, algorithm: str, which_regions: str = 'nl', start: str = 'random') -> Network:
    """ Function that executes one step of the hillclimber algorithm
        by removing a trejectory from the given network,
        making a new trajectory and adding this to the network.

    Args:
        start_network (Network): a network with a solution
        algorithm (str): which algorithm to use for the new trajectory
            (connect, connect_whith, greedy_time_long/short, greedy_conn_min/max)
        which_regions (str): which region to use (nl or holland). Defaults to 'nl'.
        start (str, optional): which heuristic to use for the start place of the train. Defaults to 'random'.

    Returns:
        Network: a network with a changed trajectory
    """
    # copy the given network
    network_copy = copy.deepcopy(start_network)

    # choose random trajectory to change
    rand_traj = random.choice(network_copy.trajectories)
    stations = rand_traj.object_traj

    # unvisit all stations and connections in the chosen trajectory
    for connection in rand_traj.object_conns:
        connection.unvisit()
    for station in stations:
        station.unvisit()

    # delete chosen trajectory from the solution        
    network_copy.remove_trajectory(rand_traj)

    # make a new trajectory
    new_t = Train(rand_traj.name, network_copy, which_regions, start)
    # choose which algorithm to use
    if algorithm == 'connect':
        new_t.connect()
    elif algorithm == 'connect_with':
        new_t.connect_with_used()
    elif algorithm == 'greedy_time_long':
        new_t.greedy_time('long')
    elif algorithm == 'greedy_time_short':
        new_t.greedy_time('short')
    elif algorithm == 'greedy_conn_min':
        new_t.greedy_conns('min')
    elif algorithm == 'greedy_conn_max':
        new_t.greedy_conns('max')

    # add the new trajectory to the solution
    network_copy.add_trajectory(new_t)

    # return the new network
    return network_copy


def random_restart(iterations: int, stop_after: int, algorithm: str, which_regions: str = 'nl', start: str = 'random') -> Tuple[Network, List[float]]:
    """ Function that runs multiple hillclimbers after eachother 
            whith different starting conditions
            and returns the best solution out of all of them

    Args:
        iterations (int): how many times to restart
        stop_after (int): after how many non-better answers the hillclimber should stop
        algorithm (str): which algorithm to use for the trajectories
        which_regions (str, optional): which region to use (nl or holland). Defaults to 'nl'.
        start (str, optional): which starting heuristic to use (random or min_con). Defaults to 'random'.

    Returns:
        Network: the network worth trhe best found solution
        List[float]: a list of all intermediate solutions' k-values
    """
 
    # set region
    if which_regions == 'nl':
        data_stations = 'data/case_data/StationsNationaal.csv'
        data_connections = 'data/case_data/ConnectiesNationaal.csv'
    elif which_regions == 'holland':
        data_stations = 'data/case_data/StationsHolland.csv'
        data_connections = 'data/case_data/ConnectiesHolland.csv'

    # create an empty network
    best_sol = Network(data_stations, data_connections)

    # initiate empty list for intermediate k-values
    long_list: List[float] = []

    # run the restart algorithm
    for i in range(iterations):
        # let user know how far they are
        if i % 10 == 0:
            print(f"iteration {i} / {iterations}")

        # run a hillclimber
        new = climb_hill(False, stop_after, algorithm, which_regions, start)
        new_sol = new[0]

        # if the new found solution is better than the one now
        if new_sol.calc_k() > best_sol.calc_k():
            # set the new best
            best_sol = new_sol
        
        # add hillclimbers' k-values to the list
        list_hill = new[1]
        long_list = long_list + list_hill

    # return the best solution and the intermediate k-values
    return best_sol, long_list




    