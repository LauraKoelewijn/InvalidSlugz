from program.algorithm import run
from program.visualisation import visualize
from program.baseline import hist

# create a network and run the algorithm
data_tuple = run()

# save data from the run
n = data_tuple[0]
trains = data_tuple[1]

# visualize the data
visualize(n, trains)

hist(1000)
