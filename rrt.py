import numpy as np

# Samples numPts random points around the given x, y in a circle of radius r
def samplePointsAround(x, y, r, numPts):
    pts = np.zeros((numPts, 2))
    for i in range(numPts):
        # Generate a random angle
        theta = np.random.uniform(0, 2 * np.pi)

        # Generate a random radius
        dist = np.random.uniform(0, r)

        # Convert polar coordinates to cartesian
        ptX = x + dist * np.cos(theta)
        ptY = y + dist * np.sin(theta)
        pts[i] = np.array((ptX, ptY))

    return pts

"""
    Rapidly-exploring Random Tree for parafoil pathfinding
    This algorithm will begin at the start coordinate, and sample random points around the current position and goal position.
    It will then determine which of these points are viable given the turn radius and maximum distance travellable.
    Once viable points are found, it will connect them to the current point, and for each of these new points repeat this process until we reach the goal.
    startCoord: starting location, tuple of (x, y)
    goalCoord: goal location, tuple of (x, y)
    maxIterations: maximum number of iterations to run the algorithm
    maxDistTravellable: maximum distance that can be travelled in one iteration
"""
def RRT(startCoord, goalCoord, maxIterations, maxDistTravellable):
    startX, startY = startCoord
    startPoint = (None, startX, startY) # all points follow this structure of (parentPoint, x, y)
    randomPoints = samplePointsAround(startX, startY, maxDistTravellable, 20)

    # TODO: determine which of these points are viable

    tree = []

    for point in randomPoints:
        x, y = point
        newNode = (startPoint, x, y)
        tree.append(newNode)

    # TODO: finish
    return tree