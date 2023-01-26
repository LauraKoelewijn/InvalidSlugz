from .trajectory import Train
from .network_graph import Network

import copy
import random
 
def climb_hill(just_hillclimb, iter_or_condstop: int, algorithm, which_regions: str = 'nl', start: str  = 'min_con'):
    """Funtion that executes the hillclimber algorithm.
        It takes a network with al already produced solution,
            it randomly chooses a trajectory to delete
            it makes a new trajectory
            if the new solution is better then the last one, it is saved

    Args:
        network (Network): a network graph, already with solution
        iterations (int): how many iterations the algorithm should do
        which_regions (str): nl or holland
        start (str): random or min_con

    Returns:
        Network: a the network with the best solution found
    """

    if which_regions == 'nl':
        traj_num = 20
        data_stations = 'data/StationsNationaal.csv'
        data_connections = 'data/ConnectiesNationaal.csv'
    elif which_regions == 'holland':
        traj_num = 7
        data_stations = 'data/StationsHolland.csv'
        data_connections = 'data/ConnectiesHolland.csv'
    
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
        elif algorithm == 'greedy_time':
            t.greedy_time()
        elif algorithm == 'greedy_conn':
            t.greedy_conns()

        network.add_trajectory(t)
        train_number += 1

    # set starting colution to first best solution
    best_solution = network
    #print(f"starting at {best_solution.calc_k()} for {which_regions}")

    #for i in range(iterations):
    if just_hillclimb:
        # print('hiero')
        for i in range(iter_or_condstop):
            outcome = hill_step(best_solution, algorithm, which_regions, start)
            if outcome != False:
                best_solution = outcome
    else:
        # print('random boi')
        check_stop = 0
        # run hillclimber for given amount of iterations
        go = True
        while go:
            outcome = hill_step(best_solution, algorithm, which_regions, start)
            if outcome != False:
                best_solution = outcome
                check_stop = 0
            else:
                check_stop += 1
            
            # print current best solution 
            # print(f'BEST NOW: {best_solution.calc_k()}')
            if check_stop >= iter_or_condstop:
                go = False
    
    # return k for best solution network
    return best_solution  

def hill_step(best_solution: "Network", algorithm, which_regions, start):
    # copy the solution network
    network_copy = copy.deepcopy(best_solution)

    #choose random trajectory to change
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
    # CHOOSE WHICH ALGORITHM TO USE
    if algorithm == 'connect':
        new_t.connect()
    elif algorithm == 'connect_with':
        new_t.connect_with_used()
    elif algorithm == 'greedy_time':
        new_t.greedy_time()
    elif algorithm == 'greedy_conn':
        new_t.greedy_conns()
    network_copy.add_trajectory(new_t)

    # keep best solution 
    if network_copy.calc_k() > best_solution.calc_k():
        best_solution = network_copy
        return best_solution
    else:
        return False

def random_restart(iterations: int, stop_after: int, algorithm: str, which_regions: str = 'nl', start: str = 'random'):
    # save best solution out of all restarts
    print(which_regions)

    if which_regions == 'nl':
        data_stations = 'data/StationsNationaal.csv'
        data_connections = 'data/ConnectiesNationaal.csv'
    elif which_regions == 'holland':
        data_stations = 'data/StationsHolland.csv'
        data_connections = 'data/ConnectiesHolland.csv'

    best_sol = Network(data_stations, data_connections)
    print(f'starting at: {best_sol.calc_k()}')

    for i in range(iterations):
        new_sol = climb_hill(False, stop_after, algorithm, which_regions, start)

        if new_sol.calc_k() > best_sol.calc_k():
            best_sol = new_sol
            print(best_sol.calc_k())

    return best_sol




    