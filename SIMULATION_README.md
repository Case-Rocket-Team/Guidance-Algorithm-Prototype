# Instructions on Piping Algo into Simulation Code

## Files
Download / include files `rrt.py` and `constants.py` in the workspace. From `rrt.py`, import the function `start_RRT_return_formated_path`.
This is the main function that will be used to actually run the algorithm.

## Usage
`start_RRT_return_formated_path` accepts a single argument in the form of a numpy array for the starting heading of the rocket, in terms of the x and y components of the heading vector (normalized). **ALL OTHER CONSTANTS** come from `constants.py`, such as the starting coords, goal coords, etc. This can easily be changed to use dynamic parameters if necessary.

When the function is called, it will perform the path finding algorithm, and go through the resulting linked list of nodes and return a nice list for you to use. It is a list of nodes (tuples) which constitute the path, and is of the form `(x, y, heading, length, turning_radius)`. Nodes are placed in order, so that the first element of the list is the first in the path. 
