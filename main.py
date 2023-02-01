# import functions
from program.write_solution import write_to_csv
from program.analysis_visualisation.visualisation import visualize
from program.analysis_visualisation.background_map import make_map
from program.analysis_visualisation.baseline import hist
from program.algorithms.hillclimber import climb_hill, random_restart
from program.analysis_visualisation.boxplot import boxplot_start, boxplot_greedy, boxplot_restart, boxplot_hill, boxplot_eind, lineplot, boxplot_time, boxplot_connections

# COMMENT OUT THE PARTS YOU DON'T WANT TO RUN

# baseline histogram without any bias, based on random algorithm
# hist(iteration = 1000)

# random algorithm boxplot 
#   looking at starting with random station or station with minimal connections
# boxplot_start(iteration = 1000)

# --- experiments ---

# make a boxplot showing the greedy algorithm, which is
#   greedy for the least or most amount of connections
#   and showing either starting at a random station 
#   or a station with the least amount of connections
# boxplot_connections(iteration = 1000)

# # make a boxplot showing the greedy algorithm wich is
# #   greedy for the longest or shortest connection
# boxplot_time(iteration = 1000)

# make a boxplot showing the greedy algorithm wich is
#   random, greedy for the shortest connection and minimal connections
# boxplot_greedy(iteration = 1000)

# make a boxplot showing the greedy algorithm wich is
#   random, hillclimber for random and hillclimber for greedy time
# boxplot_hill(iteration = 1000)

# make a boxplot showing the greedy algorithm wich is
#   random, hillclimber for greedy time and random restart
boxplot_restart(iteration = 1000)

# # make a boxplot which shows all the algorithms
# boxplot_eind(iteration = 100)

# --- find and save a (the best we'll find) solution ---
sol = random_restart(10, 50, 'connect_with', tell_me = True)[0]
#write_to_csv(sol)
visualize(sol, 'nl')





