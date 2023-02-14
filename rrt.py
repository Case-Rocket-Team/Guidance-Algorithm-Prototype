import numpy as np
import pygame
import constants

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

# Samples numPts random points along the line between (x1, y1) and (x2, y2)
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

# Function for generating a circle given two points and a tangent (heading) vector
# Args must be in np array form
# Written by Ben :3
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


# Determines if a point is valid or not, meaning if a course can be plotted from the rocket's current position to the point using the circle_from function
# point, heading = (x, y) tuple
# returns tuple of (isValid, newHeading, newLength)
def isPointValid(point, rocketPoint, heading, goalX, goalY):
    x, y = point
    rocketX, rocketY, currentLength = rocketPoint

    r, length, newHeading, _ = circle_from(np.array([rocketX, rocketY]), np.array([x, y]), np.array([heading[0], heading[1]]))

    # New length is the current length + length of the new arc
    newLength = currentLength + length
    # goalLength is an estimate of the total length of this hypothetical path - combines newLength with current (straight line) dist to goal
    goalLength = newLength + np.sqrt((x - goalX) ** 2 + (y - goalY) ** 2)

    # TODO: fix the length condition. The goal of this is to ensure that all lengths are of the correct minimum length, so that we don't crash in the ground 
    # or get to the goal too early. Currently, it's just broken, and depening on what GOAL_L is the paths may not be created at all.

    #             screen bounds conndition,                 turn radius condition,               goal length condition,     also return the new heading + length
    return (not (x > 700 or x < 0 or y < 0 or y > 700) and r > constants.MIN_TURN_RADIUS and goalLength >= constants.GOAL_L), newHeading, newLength
         

"""
    Rapidly-exploring Random Tree for parafoil pathfinding
    This algorithm will begin at the start coordinate, and sample random points around the current position and goal position.
    It will then determine which of these points are viable given the turn radius and maximum distance travellable.
    Once viable points are found, it will connect them to the current point, and for each of these new points repeat this process until we reach the goal.
"""

solved = False

def RRT(startCoord, goalCoord, maxIterations, maxPoints, maxDistTravellable, pygameScreen = None):
    global solved

    # If one of the paths has reached the goal, don't bother further exploring
    # TODO: this is a bad condition, we should keep making multiple feasible paths so that we can score them at the end
    if solved:
        print('Already solved, returning...')
        return []

    # Max iterations is a constraint which keeps the simulation from running forever
    # Every time a new point is explored, we decrement the maxIterations counter, and once it reaches 0 we stop exploring
    if maxIterations <= 0:
        return []
    
    # theta = current heading
    # startPoint = tuple of previous point (if it exists, None if not)
    startPoint, startX, startY, theta, currentL = startCoord

    # First step of RRT: generate lots of random sample points

    # Sample points around the current position, line from current position to goal position, and goal position
    pointsAround = samplePointsAround(startX, startY, 50, 15)
    pointsInLine = samplePointsInLine(startX, startY, goalCoord[0], goalCoord[1], 15)
    pointsAroundGoal = samplePointsAround(goalCoord[0], goalCoord[1], 50, 15)
    # Combind into a single array
    randomPoints = [*pointsAroundGoal, *pointsInLine, *pointsAround] 

    viablePoints = []

    # For each of the random sample points, check if it's valid or not
    # if valid, add to list of valid points
    for point in randomPoints:
        isValid, newHeading, newLength = isPointValid(point, (startX, startY, currentL), (theta[0], theta[1]), goalCoord[0], goalCoord[1]) 
        if isValid:
            viablePoints.append((point, newHeading, newLength)) 

            # Draw a red circle at this point
            if pygameScreen is not None:
                pygame.draw.circle(pygameScreen, pygame.Color(255, 0, 0, a = 30), (int(point[0]), int(point[1])), 2)
                pygame.display.update()

    # Second step of RRT: go through valid points and make connections to each of them, then recursively explore using that point as the new start
    tree = [startCoord]

    for point, heading, length in viablePoints:
        x, y = point

        # This if block is just for correctly displaying the path we are exploring
        if pygameScreen is not None:
            radius, arclen, newHeading, center = circle_from(np.array([startX, startY]), np.array([x, y]), np.array([theta[0], theta[1]]))
            startRadians = np.arctan2(startY - center[1], startX - center[0])
            endRadians = np.arctan2(y - center[1], x - center[0])

            if radius < 0:
                radius *= -1
                startRadians, endRadians = -endRadians, -startRadians
            else:
                startRadians, endRadians = -startRadians, -endRadians

            pygame.draw.arc(pygameScreen, pygame.Color(0, 255, 0, a = 30), pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2), startRadians, endRadians, 1)
            pygame.display.update()

        # If we've reached the goal, set the global sovled to True, which will stop other branches from exploring
        # TODO: as explained in earlier comment, this is dumb
        if np.sqrt((x - goalCoord[0]) ** 2 + (y - goalCoord[1]) ** 2) < 30:
            solved = True
            print('solved')
            return tree

        # Recursively explore from this point
        newNode = (startCoord, x, y, heading, length)
        treeFromHere = RRT(newNode, goalCoord, maxIterations - 1, maxPoints - 1, maxDistTravellable, pygameScreen)

        # Combine the current tree with the tree just explored
        tree = tree + treeFromHere

    return tree
