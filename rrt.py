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

def isPointValid(point, rocketPoint, heading, minR, maxDistTravellable):
    x, y = point
    rocketX, rocketY = rocketPoint

    distToPoint = np.sqrt((x - rocketX) ** 2 + (y - rocketY) ** 2)

    orthogonalRightAngle = heading + np.pi / 2
    orthogonalLeftAngle = heading - np.pi / 2
    rightCircCenter = (rocketX + minR * np.cos(orthogonalRightAngle), rocketY + minR * np.sin(orthogonalRightAngle))
    leftCircCenter = (rocketX + minR * np.cos(orthogonalLeftAngle), rocketY + minR * np.sin(orthogonalLeftAngle))

    distToRightCircle = np.sqrt((x - rightCircCenter[0]) ** 2 + (y - rightCircCenter[1]) ** 2)
    distToLeftCircle = np.sqrt((x - leftCircCenter[0]) ** 2 + (y - leftCircCenter[1]) ** 2)

    new_heading = np.arctan2(y - rocketY, x - rocketX)

    return not (x > 600 or x < 0 or y < 0 or y > 600) and distToPoint < maxDistTravellable and distToRightCircle > minR and distToLeftCircle > minR and np.abs(new_heading - heading) < np.pi / 2
         

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

def RRT(startCoord, goalCoord, maxIterations, maxPoints, maxDistTravellable, pygameScreen = None):
    global MAX_POINTS

    if maxIterations <= 0 or maxPoints <= 0:
        return []
    
    startPoint, startX, startY, theta = startCoord

    MIN_TURN_R = 25
    viablePoints = []

    # Sample points around the current position, line from current position to goal position, and goal position
    pointsAround = samplePointsAround(startX, startY, maxDistTravellable, 10)
    pointsInLine = samplePointsInLine(startX, startY, goalCoord[0], goalCoord[1], 13)
    pointsAroundGoal = samplePointsAround(goalCoord[0], goalCoord[1], maxDistTravellable, 7)

    for point in [*pointsAround, *pointsInLine, *pointsAroundGoal]:
        if isPointValid(point, (startX, startY), theta, MIN_TURN_R, maxDistTravellable):
            heading = np.arctan2(point[1] - startY, point[0] - startX)
            viablePoints.append((point, heading))

    tree = [startCoord]

    for point, heading in viablePoints:
        x, y = point

        # if the point is at the goal, break out of the loop
        if np.sqrt((x - goalCoord[0]) ** 2 + (y - goalCoord[1]) ** 2) < 20:
            break

        newNode = (startCoord, x, y, heading)

        treeFromHere = RRT(newNode, goalCoord, maxIterations - 1, maxPoints - 1, maxDistTravellable)
        tree = tree + treeFromHere

        if pygameScreen is not None:
            pygame.draw.line(pygameScreen, pygame.Color(0, 255, 0, a = 30), (startX, startY), (x, y))
            pygame.display.update()

    # TODO: finish
    return tree
