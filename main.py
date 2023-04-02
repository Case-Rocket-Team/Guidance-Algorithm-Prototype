import numpy as np
import constants
from .rrt import start_RRT_return_formated_path, find_path

if __name__ == "__main__":
    start_coords = start_x, start_y = constants.ORIGIN_COORDS 
    initHeading = np.array([0, -1]) # in this case, rocket starts facing up

    goal_coords = goal_x, goal_y = constants.GOAL_COORDS

    path = start_RRT_return_formated_path(initHeading)