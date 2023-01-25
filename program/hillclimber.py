from .trajectory import Train
from .network_graph import Network

import copy
import random
 
def climb_hill(network: "Network", iterations: int, which_regions: str, start: str):
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

    # set starting colution to first best solution
    best_solution = network
    #print(f"starting at {best_solution.calc_k()}")

    # run hillclimber for given amount of iterations
    for i in range(iterations):
        #print(f"iteration {i}")
        # copy the solution network
        network_copy = copy.deepcopy(best_solution)

        #choose random trajectory to change
        rand_traj = random.choice(network_copy.trajectories)
        train_number = rand_traj.name.split('_')[1]
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
        # t.greedy_time()
        #t.greedy_conns()
        new_t.connect_with_used()
        # t.connect()
        network_copy.add_trajectory(new_t)

        # keep best solution 
        if network_copy.calc_k() > best_solution.calc_k():
            best_solution = network_copy
            #print('changed')

        # print current best solution 
        #print(f'BEST NOW: {best_solution.calc_k()}')
    
    # return k for best solution network
    return best_solution.calc_k()    
           
            




    