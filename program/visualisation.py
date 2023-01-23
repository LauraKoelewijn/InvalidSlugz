import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.pyplot import figure

from .network_graph import Network

def visualize(network, trains, which_region = 'holland'):

    if which_region == 'nl':
        geo_json_file = 'data/nl_regions.geojson'
        save_plot = 'output/holland_plot.png'
    elif which_region == 'holland':
        geo_json_file ='data/holland_regions.geojson'
        save_plot = 'output/holland_plot.png'
    
    # intialize empty lists for the plotting
    names = []
    coords = []

    # load network_graph
    stations = network.stations.values()

    img = plt.imread("data/map.png")
    fix, ax = plt.subplots()
    ax.imshow(img, extent=[3.1, 7.5, 50.6, 53.7], aspect=1.7)

    # loading file of boarders of Holland
    df_places = gpd.read_file(geo_json_file)

    # looping through regions in the data file and plotting them in a matplotlib graph
    for polygon in df_places['geometry']:
        x,y = polygon.exterior.xy
        plt.plot(x,y, color = 'grey')

    # PLOT ALL CONNECTIONS   
    # loop through all stations in the network_graph
    for station in stations:
        # add station name and coordinates to the lists
        names.append(station.name)
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
            plt.plot(x_line, y_line, color = 'black')
    
    #hide axes
    ax = plt.gca()
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    # PLOT TRAJECTORIES
    # loop through all the trajectories
    for traj in trains:
        # initiate empty lists for the coordinates
        x_traj = []
        y_traj = []
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
    plt.scatter(x, y)
        
    # add names of the stations to the points
    for index, label in enumerate(names):
        plt.annotate(label,(x[index], y[index]))
        
    # save plot
    plt.savefig(save_plot)

    # show the whole plot
    plt.show()
