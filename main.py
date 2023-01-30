from program.algorithm import run, write_to_csv
from program.analysis_visualisation.visualisation import visualize
from program.analysis_visualisation.background_map import make_map
from program.analysis_visualisation.baseline import hist
from program.algorithms.hillclimber import climb_hill, random_restart
from program.analysis_visualisation.boxplot import boxplot_eind, lineplot, boxplot_time, boxplot_connections

# run()
# create a network and run the algorithm
# you can fill in 'nl' if you want to calculate trajectory for the whole netherlands
# you can fill in 'min_con' if you want to start the trajectories at stations with minimal connections
data_tuple = run('nl')

# save data from the run
n = data_tuple[0]
trains = data_tuple[1]

# visualize the data
# if background map is needed plot it here
# make_map()
visualize(n, trains, 'nl')

# hill = climb_hill(False, 50, 'connect_with')
# print(hill.calc_k())

# random_restart(100, 50, 'greedy_conn', 'nl', 'min_con')
# hist(1000)

# boxplot_eind(10)
# lineplot()

# boxplot_time(100)
#boxplot_connections(1000)
