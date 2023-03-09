import numpy as np
import simulation_consts
import constants
from rrt import RRT
# from progressbar import printProgressBar
# import csv

"""
Class for simulating pairs of input, output constants and grading the performance of each
Usage: can use methods independently as needed or use the run_simulations() method to get a list of results,
with stats about all of the simulations and the cost of each simulation (see line 109 as example)
"""
class Simulation:
    """
    Simulates num_trials iterations of RRT algorithms with the given input_consts and output_consts
    input_consts = (LANDING_MARGIN, ORIGIN_COORDS, GOAL_COORDS, SCREEN_DIM)
    output_consts = (MAX_CURVE, NUM_POINTS, MAX_ITERATIONS, MAX_SEARCH_RAD)
    returns tuple of (avg_length, avg_points, percent_reached_goal) of all num_trials iterations
    """
    def simulate_in_out_pair(input_consts, output_consts, num_trials):
        # Set constants in simulation_consts.py
        simulation_consts.LANDING_MARGIN = input_consts[0]
        simulation_consts.ORIGIN_COORDS = input_consts[1]
        simulation_consts.GOAL_COORDS = input_consts[2]
        simulation_consts.SCREEN_DIM = input_consts[3]
        simulation_consts.MAX_CURVE = output_consts[0]
        simulation_consts.NUM_POINTS = output_consts[1]
        simulation_consts.MAX_ITERATIONS = output_consts[2]
        simulation_consts.MAX_SEARCH_RAD = output_consts[3]

        lengths = []
        num_points = []
        num_reached_goal = 0

        for i in range(num_trials):
            print('Simulation ', i)
            # printProgressBar(i, num_trials, prefix = 'Simulation Progress:', suffix = 'Complete')

            reachedGoal, final_node, tree_length = RRT(
                (None, simulation_consts.ORIGIN_COORDS[0], simulation_consts.ORIGIN_COORDS[1], np.array([0, -1]), 0), 
                simulation_consts.GOAL_COORDS, 
                simulation_consts.MAX_ITERATIONS, 
                0,
                simulation_consts,
                pygameScreen = None
            )

            _, x, y, __, tot_length = final_node

            lengths.append(tot_length)
            num_points.append(tree_length)

            if reachedGoal:
                num_reached_goal += 1

        # printProgressBar(num_trials, num_trials, prefix = 'Simulation Progress:', suffix = 'Complete')
        print()

        avg_length = int(sum(lengths) / len(lengths))
        avg_points = int(sum(num_points) / len(num_points))
        percent_reached_goal = num_reached_goal / num_trials

        print('Simulation chunk done')
        print('Results:')
        print(f'{avg_length}, {avg_points}, {percent_reached_goal}')
        print('Output consts: ', output_consts)
        print('============================================')
        print()
        
        return (avg_length, avg_points, percent_reached_goal)

    def gen_random_inputs():
        LANDING_MARGIN = int(np.random.uniform(1, 30))
        SCREEN_DIM = int(np.random.uniform(1, 600)), int(np.random.uniform(1, 600))
        ORIGIN_COORDS = int(np.random.uniform(1, SCREEN_DIM[0])), int(np.random.uniform(1, SCREEN_DIM[1]))  
        GOAL_COORDS = int(np.random.uniform(1, SCREEN_DIM[0])), int(np.random.uniform(1, SCREEN_DIM[1]))

        return (LANDING_MARGIN, ORIGIN_COORDS, GOAL_COORDS, SCREEN_DIM)

    def gen_random_outputs():
        MAX_CURVE = int(np.random.uniform(200, 800))
        NUM_POINTS = int(np.random.uniform(10, 30))
        MAX_ITERATIONS = int(np.random.uniform(100, 800))
        MAX_SEARCH_RAD = int(np.random.uniform(100, 400))

        return (MAX_CURVE, NUM_POINTS, MAX_ITERATIONS, MAX_SEARCH_RAD)

    """
    Grades the (avg_length, avg_points, percent_reached_goal) tuple from a simulation session
    lower number better person
    """
    def cost_func(result):
        avg_length, avg_points, percent_reached_goal = result

        pts_cost = avg_points ** 2
        length_cost = (avg_length - constants.GOAL_L) ** 2
        percent_reached_multiplier = 11 - (10 * percent_reached_goal)

        return percent_reached_multiplier * (pts_cost + length_cost)

    def run_simulations(num_independent_trials, num_dependent_trials, num_simulation_trials):
        results = []

        for i in range(num_independent_trials):
            # input_consts = Simulation.gen_random_inputs()
            input_consts = (50, (800, 800), (300, 300), (350, 350))

            for j in range(num_dependent_trials):
                output_consts = Simulation.gen_random_outputs()

                result = Simulation.simulate_in_out_pair(input_consts, output_consts, num_simulation_trials)
                cost = Simulation.cost_func(result)
                results.append([result, cost, input_consts, output_consts])
        
        return results

results = Simulation.run_simulations(1, 50, 5)
print('Done simulating')

print('Results which had >= 0 percent of points reach goal:') 
for result in results:
    if result[0][2] > 0:
        print(result)

# DEPRECATED BUT COMMENTED OUT BECAUSE IM LAZY
# row_list = [['id', 'indepID', 'LANDING_MARGIN', 'ORIGIN_COORDS_X', 'ORIGIN_COORDS_Y', 'GOAL_COORDS_X', 'GOAL_COORDS_Y', 'SCREEN_DIM_X', 'SCREEN_DIM_Y', 'MAX_CURVE', 'NUM_POINTS', 'MAX_ITERATIONS', 'MAX_SEARCH_RAD', 'avg_length', 'avg_points', 'num_reached_goal']]
# for i in range(0):
#     print('Starting Simulation ', i)

#     # Generate 4 random independent vars
#     LANDING_MARGIN = int(np.random.uniform(1, 30))
#     SCREEN_DIM = int(np.random.uniform(1, 600)), int(np.random.uniform(1, 600))
#     ORIGIN_COORDS = int(np.random.uniform(1, SCREEN_DIM[0])), int(np.random.uniform(1, SCREEN_DIM[1]))  
#     GOAL_COORDS = int(np.random.uniform(1, SCREEN_DIM[0])), int(np.random.uniform(1, SCREEN_DIM[1]))

#     # Set new const vals
#     consts.LANDING_MARGIN = LANDING_MARGIN
#     consts.ORIGIN_COORDS = ORIGIN_COORDS
#     consts.GOAL_COORDS = GOAL_COORDS
#     consts.SCREEN_DIM = SCREEN_DIM

#     for j in range(NUM_DEPENDENT_TRIALS):
#         print(f'Starting Simulation {i}x{j}',  j)

#         # Generate random 4 outputs
#         MAX_CURVE = int(np.random.uniform(20, 200))
#         NUM_POINTS = int(np.random.uniform(1, 20))
#         MAX_ITERATIONS = int(np.random.uniform(1, 50))
#         SEARCH_RADIUS = int(np.random.uniform(25, 300))

#         # Set new const vals
#         consts.MAX_CURVE = MAX_CURVE
#         consts.NUM_POINTS = NUM_POINTS
#         consts.MAX_ITERATIONS = MAX_ITERATIONS
#         consts.MAX_SEARCH_RAD = SEARCH_RADIUS

#         lengths = []
#         num_points = []
#         num_reached_goal = 0

#         # Run simulation w/ new contsants
#         for k in range(NUM_SIMULATION_PER_COMB):
#             reachedGoal, final_node, tree_length = RRT(
#                 (None, consts.ORIGIN_COORDS[0], consts.ORIGIN_COORDS[1], np.array([0, -1]), 0), 
#                 consts.GOAL_COORDS, 
#                 consts.MAX_ITERATIONS, 
#                 0,
#                 pygameScreen = None,
#                 constants = consts
#             )

#             _, x, y, __, tot_length = final_node

#             lengths.append(tot_length)
#             num_points.append(tree_length)

#             if reachedGoal:
#                 num_reached_goal += 1

#             printProgressBar(k, NUM_SIMULATION_PER_COMB, prefix = 'Simulation Progress:', suffix = 'Complete')

#         printProgressBar(NUM_SIMULATION_PER_COMB, NUM_SIMULATION_PER_COMB, prefix = 'Simulation Progress:', suffix = 'Complete')

#         avg_length = int(sum(lengths) / len(lengths))
#         avg_points = int(sum(num_points) / len(num_points))

#         # Add to csv rows
#         row_list.append([simulation_id, i, LANDING_MARGIN, ORIGIN_COORDS[0], ORIGIN_COORDS[1], GOAL_COORDS[0], GOAL_COORDS[1], SCREEN_DIM[0], SCREEN_DIM[1], MAX_CURVE, NUM_POINTS, MAX_ITERATIONS, SEARCH_RADIUS, avg_length, avg_points, num_reached_goal])

#         simulation_id += 1

# # Write to csv
# with open('simulation_results.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(row_list)