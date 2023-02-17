import numpy as np
import constants
from rrt import RRT
import csv

row_list = [['id', 'MAX_CURVE', 'NUM_POINTS', 'MAX_ITERATIONS', 'MAX_SEARCH_RAD', 'avg_length', 'avg_points', 'num_reached_goal']]

idddd = 0
for i in range(100):
    print('Starting new simulation ',  i)

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
    print(f'Simulation {i} trying for new RRT ', end = '')
    for j in range(20):
        print(str(j) + ', ', end = '')
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

    avg_length = int(sum(lengths) / len(lengths))
    avg_points = int(sum(num_points) / len(num_points))

    print('')
    # print(f'Average length: {avg_length}')
    # print(f'Average points: {avg_points}')
    # print('Number of times we reached the goal: ', num_reached_goal)

    # Add to csv rows
    row_list.append([idddd, MAX_CURVE, NUM_POINTS, MAX_ITERATIONS, SEARCH_RADIUS, avg_length, avg_points, num_reached_goal])

    constants.MAX_CURVE = old_vals[0]
    constants.NUM_POINTS = old_vals[1]
    constants.MAX_ITERATIONS = old_vals[2]
    constants.MAX_SEARCH_RAD = old_vals[3]
    idddd += 1

# Write to csv
with open('simulation_results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(row_list)