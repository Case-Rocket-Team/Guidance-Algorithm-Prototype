import random
import pickle
from deap import creator, base, tools, algorithms
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import numpy as np

from main import Main

# Set the seed for reproducibility
seed_num = 42
num_params = 7
random.seed(seed_num)

# Define the fitness and individual classes
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # minimize both objectives
creator.create("Individual", list, fitness=creator.FitnessMin)

# Define how to generate an individual and population
def attr_float():
    rang = 10.0
    return  2 * rang * random.random() - rang

toolbox = base.Toolbox()
toolbox.register("attr_float", attr_float)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=7)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the evaluation function
def evaluate(individual):
    params = {
        'K1': 10**individual[0],
        'K2': 10**individual[1],
        'Kp': 10**individual[2],
        'Ki': 10**individual[3],
        'Kd': 10**individual[4],
        'error_limit': 10**individual[5],
        'integral_limit': 10**individual[6]
    }
    #print(individual)
    start = ( random.randint(0,500), random.randint(0,500))
    goal = ( random.randint(0,500), random.randint(0,500))
    tang = (0,0)
    while tang == (0,0):
        tang = ( random.randint(-5,5), random.randint(-5,5))
   
    gas = random.randint(600,1000)
    des_xs, des_ys, x, y = Main(plot=False, start=start, goal=goal, tang=tang, gas=gas, max_wind=0, input_params=params)

    des = np.array([des_xs, des_ys]).T
    path = np.array([x, y]).T

    diff_distance, path = fastdtw(des, path, dist=euclidean)
    diff_goal = np.sqrt((goal[0] - x[-1])**2 + (goal[1] - y[-1])**2)
    
    return (diff_goal,)


# Define the genetic operations
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.2)
toolbox.register("select", tools.selNSGA2)

# Generate initial population
pop = toolbox.population(n=20)

# Apply the genetic algorithm
result = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, verbose=True)

# Save the best individuals
best_individuals = tools.selBest(pop, k=2)  # select the top individual

param_names = ['K1', 'K2', 'Kp', 'Ki', 'Kd', 'error_limit', 'integral_limit']
# Create a list of dictionaries, each representing the parameters of a best individual
best_individuals_dicts = [{param_names[i]: individual[i] for i in range(num_params)} for individual in best_individuals]

# Save the list of dictionaries
with open('best_params.pkl', 'wb') as output_file:
    pickle.dump(best_individuals_dicts, output_file)