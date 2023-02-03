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
    if maxIterations <= 0:
        return []
    
    startPoint, startX, startY, theta = startCoord
    randomPoints = samplePointsAround(startX, startY, maxDistTravellable, 20)

    # TODO: determine which of these points are viable
    # For now, arbitrarily say only allow points within pi / 6 radians of current heading
    viablePoints = []
    # for point in randomPoints:
    #     x, y = point
    #     angle = np.arctan2(y - startY, x - startX)
    #     if abs(angle - theta) < np.pi / 6:
    #         viablePoints.append((point, angle))

    # Actual test: points are valid only if they are outside of min turn radius R circles on either side of current position
    MIN_TURN_R = 50
    for point in randomPoints:
        x, y = point
        orthogonalRightAngle = theta + np.pi / 2
        orthogonalLeftAngle = theta - np.pi / 2
        rightCircCenter = (startX + MIN_TURN_R * np.cos(orthogonalRightAngle), startY + MIN_TURN_R * np.sin(orthogonalRightAngle))
        leftCircCenter = (startX + MIN_TURN_R * np.cos(orthogonalLeftAngle), startY + MIN_TURN_R * np.sin(orthogonalLeftAngle))

        diff = (x - rightCircCenter[0], y - rightCircCenter[1])
        diffX, diffY = diff
        dist = np.sqrt(diffX ** 2 + diffY ** 2)

        diff2 = (x - leftCircCenter[0], y - leftCircCenter[1])
        diffX2, diffY2 = diff2
        dist2 = np.sqrt(diffX2 ** 2 + diffY2 ** 2)

        if dist > MIN_TURN_R and dist2 > MIN_TURN_R:
            viablePoints.append((point, np.arctan2(y - startY, x - startX)))

    tree = [startCoord]

    for point, heading in viablePoints:
        x, y = point
        newNode = (startCoord, x, y, heading)
        treeFromHere = RRT(newNode, goalCoord, maxIterations - 1, maxDistTravellable)
        tree = tree + treeFromHere

    # TODO: finish
    return tree
