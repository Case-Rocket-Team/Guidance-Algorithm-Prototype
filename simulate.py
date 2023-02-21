import numpy as np
import constants
from rrt import RRT
from progressbar import printProgressBar
import csv

row_list = [['id', 'indepID', 'LANDING_MARGIN', 'ORIGIN_COORDS_X', 'ORIGIN_COORDS_Y', 'GOAL_COORDS_X', 'GOAL_COORDS_Y', 'SCREEN_DIM_X', 'SCREEN_DIM_Y', 'MAX_CURVE', 'NUM_POINTS', 'MAX_ITERATIONS', 'MAX_SEARCH_RAD', 'avg_length', 'avg_points', 'num_reached_goal']]

simulation_id = 0
for i in range(100):
    print('Starting Simulation ', i)
    # Save old const values of LANDING_MARGIN, ORIGIN_COORDS, GOAL_COORDS, SCREEN_DIM
    old_vals_independent = constants.LANDING_MARGIN, constants.ORIGIN_COORDS, constants.GOAL_COORDS, constants.SCREEN_DIM

    # Generate 4 random independent vars
    LANDING_MARGIN = int(np.random.uniform(1, 30))
    SCREEN_DIM = int(np.random.uniform(1, 600)), int(np.random.uniform(1, 600))
    ORIGIN_COORDS = int(np.random.uniform(1, SCREEN_DIM[0])), int(np.random.uniform(1, SCREEN_DIM[1]))  
    GOAL_COORDS = int(np.random.uniform(1, SCREEN_DIM[0])), int(np.random.uniform(1, SCREEN_DIM[1]))

    # Set new const vals
    constants.LANDING_MARGIN = LANDING_MARGIN
    constants.ORIGIN_COORDS = ORIGIN_COORDS
    constants.GOAL_COORDS = GOAL_COORDS
    constants.SCREEN_DIM = SCREEN_DIM

    for j in range(100):
        print(f'Starting Simulation {i}x{j}',  j)

        # save old const vals
        old_vals = constants.MAX_CURVE, constants.NUM_POINTS, constants.MAX_ITERATIONS, constants.MAX_SEARCH_RAD

        # Generate random 4 outputs
        MAX_CURVE = int(np.random.uniform(20, 200))
        NUM_POINTS = int(np.random.uniform(1, 20))
        MAX_ITERATIONS = int(np.random.uniform(1, 50))
        SEARCH_RADIUS = int(np.random.uniform(25, 300))

        # Set new const vals
        constants.MAX_CURVE = MAX_CURVE
        constants.NUM_POINTS = NUM_POINTS
        constants.MAX_ITERATIONS = MAX_ITERATIONS
        constants.MAX_SEARCH_RAD = SEARCH_RADIUS

        lengths = []
        num_points = []
        num_reached_goal = 0

        # Run simulation w/ new contsants
        for k in range(20):
            print(str(k) + ', ', end = '')
            reachedGoal, final_node, tree_length = RRT(
                (None, constants.ORIGIN_COORDS[0], constants.ORIGIN_COORDS[1], np.array([0, -1]), 0), 
                constants.GOAL_COORDS, 
                constants.MAX_ITERATIONS, 
                0,
                None
            )

            _, x, y, __, tot_length = final_node

            lengths.append(tot_length)
            num_points.append(tree_length)

            if reachedGoal:
                num_reached_goal += 1

            printProgressBar(k, 20, prefix = 'Simulation Progress:', suffix = 'Complete')

        printProgressBar(20, 20, prefix = 'Simulation Progress:', suffix = 'Complete')

        avg_length = int(sum(lengths) / len(lengths))
        avg_points = int(sum(num_points) / len(num_points))

        # Add to csv rows
        row_list.append([simulation_id, i, LANDING_MARGIN, ORIGIN_COORDS[0], ORIGIN_COORDS[1], GOAL_COORDS[0], GOAL_COORDS[1], SCREEN_DIM[0], SCREEN_DIM[1], MAX_CURVE, NUM_POINTS, MAX_ITERATIONS, SEARCH_RADIUS, avg_length, avg_points, num_reached_goal])

        constants.MAX_CURVE = old_vals[0]
        constants.NUM_POINTS = old_vals[1]
        constants.MAX_ITERATIONS = old_vals[2]
        constants.MAX_SEARCH_RAD = old_vals[3]
        simulation_id += 1

    # Now that simulation is done, reset constants
    constants.LANDING_MARGIN = old_vals_independent[0]
    constants.ORIGIN_COORDS = old_vals_independent[1]
    constants.GOAL_COORDS = old_vals_independent[2]
    constants.SCREEN_DIM = old_vals_independent[3]

# Write to csv
with open('simulation_results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(row_list)