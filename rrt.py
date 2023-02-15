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
        # change to slope form, walk across slope.
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
    # Estimate the total length of this hypothetical path - combines newLength with current (straight line) dist to goal
    totalEstLength = newLength + np.sqrt((x - goalX) ** 2 + (y - goalY) ** 2)

    in_field = x > 0 and y > 0 and x < constants.SCREEN_DIM[0] and y < constants.SCREEN_DIM[1]
    big_enough = r > constants.MIN_TURN_RADIUS
    small_enough = r < constants.MAX_CURVE
    travellable = totalEstLength < constants.GOAL_L

    
    valid = in_field and big_enough and small_enough and travellable

    return valid, newHeading, newLength
         

"""
    Rapidly-exploring Random Tree for parafoil pathfinding
    This algorithm will begin at the start coordinate, and sample random points around the current position and goal position.
    It will then determine which of these points are viable given the turn radius and maximum distance travellable.
    Once viable points are found, it will connect them to the current point, and for each of these new points repeat this process until we reach the goal.
"""

def RRT(startCoord, goalCoord, maxIterations, pygameScreen = None):
    solved = False

    # Max iterations is a constraint which keeps the simulation from running forever
    # Every time a new point is explored, we decrement the maxIterations counter, and once it reaches 0 we stop exploring
    if maxIterations <= 0:
        return solved, startCoord
    
    # theta = current heading
    # startPoint = tuple of previous point (if it exists, None if not)
    startPoint, startX, startY, theta, currentL = startCoord

    # First step of RRT: generate lots of random sample points

    # Sample points around the current position, line from current position to goal position, and goal position
    pointsAround = samplePointsAround(startX, startY, constants.MAX_SEARCH_RAD, constants.NUM_POINTS)
    pointsInLine = samplePointsInLine(startX, startY, goalCoord[0], goalCoord[1], constants.NUM_POINTS)
    pointsAroundGoal = samplePointsAround(goalCoord[0], goalCoord[1], constants.MAX_SEARCH_RAD, constants.NUM_POINTS)
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
    np.random.shuffle(viablePoints)
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

            #pygame.draw.arc(pygameScreen, pygame.Color(0, 255, 0, a = 30), pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2), startRadians, endRadians, 1)
            pygame.display.update()

        # Check if we've reached our 'sovled conditions,' and if so, return this node as the last one w/ solved = True
        close_enough = np.sqrt((x - goalCoord[0]) ** 2 + (y - goalCoord[1]) ** 2) < constants.LANDING_MARGIN
        within_landing = length + constants.LANDING_MARGIN > constants.GOAL_L

        newNode = (startCoord, x, y, heading, length)

        if close_enough and within_landing:
            print('length: ',length)
            solved = True
            print('solved')
            return solved, newNode

        # Recursively explore from this point
        solved, lastNode = RRT(newNode, goalCoord, maxIterations - 1, pygameScreen)
        if solved:
            return solved, lastNode

    # If this point reached, no viable points satisfied the solved conditions
    return solved, startCoord
