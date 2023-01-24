from program.algorithm import run
from program.visualisation import visualize
from program.baseline import hist
from program.boxplot import boxplot

from program.algorithm import run

run()
# create a network and run the algorithm
# you can fill in 'nl' if you want to calculate trajectory for the whole netherlands
# you can fill in 'min_con' if you want to start the trajectories at stations with minimal connections
data_tuple = run('nl', 'min_con')

# save data from the run
n = data_tuple[0]
trains = data_tuple[1]

# visualize the data
visualize(n, trains, 'nl')

# hist(1000)

<<<<<<< HEAD
#boxplot(100, 'nl')
=======
# boxplot(100, 'nl')
>>>>>>> 3efe5a78d08f1118ef2668cf60f6dc3ebd1bc583
