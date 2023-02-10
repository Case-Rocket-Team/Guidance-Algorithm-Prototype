import numpy as np
import pygame

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

def samplePointsInLine(x1, y1, x2, y2, numPts):
    length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    pts = np.zeros((numPts, 2))

    for i in range(numPts):
        r = np.random.uniform(0, length)
        theta = np.arctan2(y2 - y1, x2 - x1)
        x = x1 + r * np.cos(theta)
        y = y1 + r * np.sin(theta)
        pts[i] = np.array((x, y))
    
    return pts
"""
    POINT STRUCT
    (parent, x, y, heading, length, arcData)
    parent = POINT STRUCT
    x = x coordinate
    y = y coordinate
    heading = np.array([x, y]) - x & y coordinate of heading vector
    length = total length of the path up to this point
    arcData = (radius, arcLength, heading) - data for arc from parent to here
"""

def circle_from(p1,p2,tang):
    tang = tang / np.linalg.norm(tang) # normalize tangent vector
    pvec = (p2-p1) # find the difference between our two points
    pnorm = np.linalg.norm(pvec) # find the distance between them
    pvec_3 = np.array([pvec[0],pvec[1],0]) / pnorm # prepare the difference vector for crossing
    tang_3 = np.array([tang[0],tang[1],0]) # prepare the tangent vector for crossing
    sin_phi = np.cross(pvec_3,tang_3)[2] # taking the cross product, cross is the sin of the angle between tan,pvec
    radius = pnorm / (2*sin_phi)
    center = p1-np.array([-tang[1],tang[0]])*radius # moving from p_1 perpendicular to the tangentuntil we get to the cent
    
    arclen = radius*np.arcsin(sin_phi)
    pc = (center - p2) * np.sign(radius)
    head_new = np.array([-pc[1],pc[0]])
    return radius, arclen, head_new, center

GOAL_L = 750

def isPointValid(point, rocketPoint, heading, minR, goalX, goalY, maxDistTravellable):
    x, y = point
    rocketX, rocketY, currentLength = rocketPoint

    r, length, newHeading, arcCenter = circle_from(np.array([rocketX, rocketY]), np.array([x, y]), np.array([heading[0], heading[1]]))

    newLength = currentLength + length + np.sqrt((x - goalX) ** 2 + (y - goalY) ** 2)

    """
    CONDITIONS:
    - current length <= 650 +/- 100
    """

    return (not (x > 700 or x < 0 or y < 0 or y > 700) and r > minR and (newLength > GOAL_L)), newHeading, newLength
         

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

solved = False

def RRT(startCoord, goalCoord, maxIterations, maxPoints, maxDistTravellable, pygameScreen = None):
    global solved

    if solved:
        return []

    if maxIterations <= 0 or maxPoints <= 0:
        return []
    
    startPoint, startX, startY, theta, currentL = startCoord

    MIN_TURN_R = 13
    viablePoints = []

    # Sample points around the current position, line from current position to goal position, and goal position
    pointsAround = samplePointsAround(startX, startY, 50, 15)
    pointsInLine = samplePointsInLine(startX, startY, goalCoord[0], goalCoord[1], 15)
    pointsAroundGoal = samplePointsAround(goalCoord[0], goalCoord[1], 50, 15)

    for point in [*pointsAroundGoal, *pointsInLine, *pointsAround]:
        isValid, newHeading, newLength = isPointValid(point, (startX, startY, currentL), (theta[0], theta[1]), MIN_TURN_R, goalCoord[0], goalCoord[1], maxDistTravellable) 
        if isValid:
            viablePoints.append((point, newHeading, newLength)) # invert Y of heading??

            # Draw a red circle at this point
            if pygameScreen is not None:
                pygame.draw.circle(pygameScreen, pygame.Color(255, 0, 0, a = 30), (int(point[0]), int(point[1])), 2)
                pygame.display.update()

    tree = [startCoord]

    for point, heading, length in viablePoints:
        x, y = point

        if pygameScreen is not None:
            radius, arclen, newHeading, center = circle_from(np.array([startX, startY]), np.array([x, y]), np.array([theta[0], theta[1]]))
            startRadians = np.arctan2(startY - center[1], startX - center[0])
            endRadians = np.arctan2(y - center[1], x - center[0])

            if radius < 0:
                radius *= -1
                startRadians, endRadians = -endRadians, -startRadians
            else:
                startRadians, endRadians = -startRadians, -endRadians

            # pygame.draw.arc(pygameScreen, pygame.Color(0, 255, 0, a = 30), pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2), startRadians, endRadians, 1)
            # pygame.draw.line(pygameScreen, pygame.Color(255, 0, 0, a = 30), (x, y), (x + newHeading[0], y + newHeading[1]))
            pygame.draw.line(pygameScreen, pygame.Color(0, 255, 0, a = 30), (startX, startY), (x, y))
            pygame.display.update()

        # if the point is at the goal, break out of the loop
        if np.sqrt((x - goalCoord[0]) ** 2 + (y - goalCoord[1]) ** 2) < 30:
            solved = True
            return tree

        newNode = (startCoord, x, y, heading, length)

        treeFromHere = RRT(newNode, goalCoord, maxIterations - 1, maxPoints - 1, maxDistTravellable, pygameScreen)
        tree = tree + treeFromHere

    # TODO: finish
    return tree
