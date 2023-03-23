import numpy as np
from . import constants
from .rrt import start_RRT_return_formated_path, find_path

start_coords = start_x, start_y = constants.ORIGIN_COORDS 
initHeading = np.array([0, -1]) # in this case, rocket starts facing up

goal_coords = goal_x, goal_y = constants.GOAL_COORDS

printMe = True

# Generate tree
final_node, final_length = find_path(
    (None, start_x, start_y, np.array([0, -1]), 0), 
    goal_coords, 
    15000 * 6.5,
    None
)

print('Final path found, length is ', final_length)