import matplotlib.pyplot as plt
from typing import List

from ..representation.network_graph import Network

def visualize(network, trains, which_region = 'holland'):

    # check if wanted map is of holland of nl and change save option
    if which_region == 'nl':
        save_plot = 'output/nl_plot_con.png'
    elif which_region == 'holland':
        save_plot = 'output/holland_plot_con.png'
    
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
            plt.plot(x_line, y_line, color = 'black', linestyle='--', dashes=(5, 2))
    
    #hide axes
    ax = plt.gca()
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    # PLOT TRAJECTORIES
    # loop through all the trajectories
    for traj in trains:
        # initiate empty lists for the coordinates
        x_traj: List[float] = []
        y_traj: List[float] = []

        # loop through the trajectory
        for station_name in traj:
            # save coordinates of every station in the trajectory
            station_node = network.stations[station_name]
            station_coords = station_node.coord
            x_traj.append(station_coords[0])
            y_traj.append(station_coords[1])
        # plot the trajectory
        plt.plot(x_traj, y_traj)

    # unzip the tuples and plot them
    x,y = zip(*coords)
    plt.scatter(x, y, zorder=10)
        
    # # add names of the stations to the points
    # for index, label in enumerate(names):
    #     plt.annotate(label,(x[index], y[index]))
        
    # save plot
    plt.savefig(save_plot, dpi = 500)

    # show the whole plot
    plt.show()
