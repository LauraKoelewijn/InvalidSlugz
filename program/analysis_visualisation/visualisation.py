#   visualisation.py
#
#   Minor programmeren - Algoritmen en Heuristieken
#   RailNL case
#   Meike Klunder, Laura Koelewijn & Sacha Gijsbers
#
#   Holds the visualize function which can plot all connections of Holland or
#   NL in black, and then plot the trajectories on top of it in alternating
#   colours.

# import libraries and classes
import matplotlib.pyplot as plt # type: ignore
from typing import List

import matplotlib.transforms as mtrans # type: ignore

def visualize(network: 'Network', which_region = 'holland') -> None:
    """Plots all connections in black and then plots trajectories on top of it.

    Args:
        network ('Network'): a Network object
        which_region (str): 'holland' or 'nl' depending on which region you
        want to use.
    """
    # check if wanted map is of holland of nl and change save option
    if which_region == 'nl':
        save_plot = 'output/nl/visualisations/nl_plot_con.png'
    elif which_region == 'holland':
        save_plot = 'output/holland/holland_plot_con.png'

    # intialize empty list of coordinates for plotting
    coords: List[List[float]] = []

    # load network_graph
    stations = network.stations.values()

    # load the map picture, choose which basemap to use
    img = plt.imread("data/background/map_nl.png")

    # initialise subplots
    fix, ax = plt.subplots()

    # set map as background plot of specific size
    ax.imshow(img, extent=[3.1, 7.4, 50.62, 53.73], aspect=1.7)

    cols = ['red', 'midnightblue', 'orange', 'yellow', 'hotpink', 'limegreen', 'darkgreen', 'purple', 'darksalmon', 'steelblue', 'dodgerblue', 'maroon', 'blue', 'indigo', 'darkviolet', 'magenta', 'olivedrab', 'saddlebrown', 'white', 'lawngreen']

    # PLOT ALL CONNECTIONS
    # loop through all stations in the network_graph
    for station in stations:
        # add station name and coordinates to the lists
        coords.append(station.coord)

        # load connections for this station
        connections = station.connect

        # loop though connections
        for con in connections:
            other = con.get_other_station(station)
            # save coordinates of all the connections
            x_line = [station.coord[0], other.coord[0]]
            y_line = [station.coord[1], other.coord[1]]

            # plot connections between all stations
            plt.plot(x_line, y_line, color = 'grey', linestyle='--')

    # hide axes
    ax = plt.gca()
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    # PLOT TRAJECTORIES
    # loop through all the trajectories
    for i, traj in enumerate(network.trajectories):
        # initiate empty lists for the coordinates
        x_traj: List[float] = []
        y_traj: List[float] = []

        # loop through the trajectory
        for station in traj.object_traj:
            # save coordinates of every station in the trajectory
            station_coords = station.coord
            x_traj.append(station_coords[0])
            y_traj.append(station_coords[1])
        # plot the trajectory
        plt.plot(x_traj, y_traj, color=cols[i], transform=mtrans.offset_copy(ax.transData, fig=fix, x=(i-3)*0.008, y=(i-3)*0.008))
        # plt.plot(x_traj, y_traj)

    # unzip the tuples and plot them
    x,y = zip(*coords)
    plt.scatter(x, y, zorder=10)

    # add names of the stations to the points
    # for index, label in enumerate(names):

    # save plot
    plt.savefig(save_plot, dpi = 500)

    # show the whole plot
    plt.show()
