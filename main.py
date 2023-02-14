import numpy as np
import pygame
from rrt import RRT, circle_from

pygame.init()

size = width, height = (700, 700)
screen = pygame.display.set_mode(size)
black = 255, 255, 255

running = True

start_coords = 200, 200
start_x, start_y = start_coords

goal_coords = 500, 500
goal_x, goal_y = goal_coords

# Draw black circle at start and yellow circle at goal
pygame.draw.circle(screen, (0, 0, 0), (start_x, start_y), 5)
pygame.draw.circle(screen, (255, 255, 0), goal_coords, 5)

test_tree = []
screen.fill(black)

# test to see if this path reached the goal
def reachedGoal(tree):
    for node in tree:
        _, x, y, __, ___ = node
        distToGoal = np.sqrt((x - goal_x) ** 2 + (y - goal_y) ** 2)
        if distToGoal <= 30:
            return True

    return False

printMe = True

# Generate tree
# while not reachedGoal(test_tree):
while len(test_tree) < 20:
    print('Trying for new RRT')
    screen.fill(black)
    # test_tree = RRT((None, start_x, start_y, np.array([1, 0]), 0), goal_coords, 50, 40, 30, screen)
    test_tree = RRT((None, start_x, start_y, np.array([0, -1]), 0), goal_coords, 10, 40, 30, screen)
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # screen.fill(black)

    # if printMe:
        # print('Drawing paths')
    # for node in test_tree:
    #     pygame.draw.circle(screen, (0, 0, 255), (node[1], node[2]), 2)
    #     originPoint, pointX, pointY, pointHeading, length, arcData = node

    #     if originPoint is not None and arcData is not None:
    #         arcCenter, arcRadius, radiansToStart, radiansToEnd = arcData
    #         _, originX, originY, _b, _c, _d = originPoint
    #         pygame.draw.arc(screen, pygame.Color(0, 255, 0, a = 30), pygame.Rect(arcCenter[0] - arcRadius, arcCenter[1] - arcRadius, arcRadius * 2, arcRadius * 2), radiansToStart, radiansToEnd, 1)
            # pygame.draw.line(screen, pygame.Color(0, 255, 0, a = 30), (originX, originY), (pointX, pointY), width = 1)

    # find node closest to goal, and backtrack through its path, drawing orange lines to display
    if printMe:
        print('Finding ideal path (for now, closest to goal)')

    closestNode = None
    for node in test_tree:
        _, x, y, _b, _c = node
        distToGoal = np.sqrt((x - goal_x) ** 2 + (y - goal_y) ** 2)
        if closestNode is None or distToGoal < closestNode[0]:
            closestNode = (distToGoal, node)

    # # backtrack through closestNode path and draw lines
    if printMe:
        print('Drawing ideal path')

    _, currentNode = closestNode
    
    if printMe:
        _, x, y, _b, length = currentNode
        print('Length of final path: ', length)
        print('X and Y of closest node: ', x, y)
    
    parentNode = currentNode[0]

    while parentNode is not None:
        _, x, y, _b, _c = currentNode
        _, parentX, parentY, tang, _c = parentNode
        # pygame.draw.line(screen, (255, 165, 0), (x, y), (parentX, parentY), width = 2)
        radius, arclen, newHead, center = circle_from(np.array([parentX, parentY]), np.array([x, y]), tang)

        startRadians = np.arctan2(parentY - center[1], parentX - center[0])
        endRadians = np.arctan2(y - center[1], x - center[0])

        if radius < 0:
            radius *= -1
            startRadians, endRadians = -endRadians, -startRadians
        else:
            startRadians, endRadians = -startRadians, -endRadians

        pygame.draw.arc(screen, (255, 165, 0), (center[0] - radius, center[1] - radius, radius * 2, radius * 2), startRadians, endRadians, 2)
        currentNode = parentNode
        parentNode = currentNode[0]
    # lastNode = test_tree[-1]

    # Draw each node as a red circle going up lastNode's path
    # while lastNode is not None:
    #     pygame.draw.circle(screen, pygame.Color(255, 0, 0, a = 30), (lastNode[1], lastNode[2]), 2);
    #     heading = lastNode[3]
    #     pygame.draw.line(screen, pygame.Color(255, 0, 0, a = 30), (lastNode[1], lastNode[2]), (lastNode[1] + heading[0] * 5, lastNode[2] + heading[1] * 5), width = 1)
    #     pygame.display.update()
    #     lastNode = lastNode[0]

    # Start and goal circles - draw last so they're on top
    pygame.draw.circle(screen, (0, 0, 0), (start_x, start_y), 5)
    pygame.draw.circle(screen, (255, 255, 0), goal_coords, 5)

    pygame.display.flip()
    printMe = False

pygame.quit()