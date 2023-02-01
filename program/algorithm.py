#   algorithm.py
#
#   Minor programmeren - Algoritmen en Heuristieken
#   RailNL case
#   Meike Klunder, Laura Koelewijn & Sacha Gijsbers
#
#   Holds function that writes produced data into the csv file format for a solution

# import 
from .representation.network_graph import Network
from .algorithms.trajectory import Train
from .algorithms.hillclimber import climb_hill, random_restart
import csv

def write_to_csv(network: Network):
    """ Function that writes the solution from the given network to a csv file

    Args:
        network (Network): a network with a solution
    """
    # open a new csv file to write the solution in
    with open('output/output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')

        # write the header
        header = ["train", "stations"]
        writer.writerow(header)
        
        # loop through the trajectories saved in the network
        for train in network.trajectories:
            # make good string representation without quotation marks
            str_repr: str = f'[%s]' % ', '.join(map(str, train.trajectory))

            # write the name and stations of the train to the output file
            writer.writerow([train.name, str_repr])

        # calculate and add k-value
        k: float = network.calc_k()
        writer.writerow(["score", k])
