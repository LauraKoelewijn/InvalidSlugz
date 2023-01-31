# import functions
from program.algorithm import write_to_csv
from program.analysis_visualisation.visualisation import visualize
from program.analysis_visualisation.background_map import make_map
from program.analysis_visualisation.baseline import hist
from program.algorithms.hillclimber import climb_hill, random_restart
from program.analysis_visualisation.boxplot import boxplot_eind, lineplot, boxplot_time, boxplot_connections

# COMMENT OUT THE PARTS YOU DON'T WANT TO RUN

# --- experiments ---

# make a boxplot showing the greedy algorithm, which is
#   greedy for the least or most amount of connections
#   and showing either starting at a random station 
#   or a station with the least amount of connections
boxplot_connections(iteration = 1000)

# make a boxplot showing the greedy algorithm wich is
#   greedy for the longest or shortest connection
boxplot_time(iteration = 1000)

# make a boxplot which shows all the algorithms
boxplot_eind(iteration = 100, which_regions='nl')

# --- find and save a (the best we'll find) solution ---
sol = random_restart(1000, 50, 'connect_with', tell_me = True)[0]
write_to_csv(sol)
visualize(sol, 'nl')




