import numpy as np
import pygame
from rrt import RRT

pygame.init()

size = width, height = (600, 600)
screen = pygame.display.set_mode(size)
black = 255, 255, 255

running = True

start_coords = 200, 200
start_x, start_y = start_coords

goal_coords = 500, 500
goal_x, goal_y = goal_coords

test_tree = []
screen.fill(black)

while len(test_tree) < 50:
    print('Trying for new RRT')
    screen.fill(black)
    test_tree = RRT((None, start_x, start_y, -1 * np.pi / 4), goal_coords, 25, 40, 30, screen)
print('Valid tree found!')

printMe = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(black)

    if printMe:
        print('Drawing paths')
    for node in test_tree:
        pygame.draw.circle(screen, (0, 0, 255), (node[1], node[2]), 2)
        originPoint, pointX, pointY, pointHeading = node
        if originPoint is not None:
            _, originX, originY, _b = originPoint
            pygame.draw.line(screen, pygame.Color(0, 255, 0, a = 30), (originX, originY), (pointX, pointY), width = 1)

    # find node closest to goal, and backtrack through its path, drawing orange lines to display
    if printMe:
        print('Finding ideal path (for now, closest to goal)')

    closestNode = None
    for node in test_tree:
        _, x, y, _ = node
        distToGoal = np.sqrt((x - goal_x) ** 2 + (y - goal_y) ** 2)
        if closestNode is None or distToGoal < closestNode[0]:
            closestNode = (distToGoal, node)

    # backtrack through closestNode path and draw lines
    if printMe:
        print('Drawing ideal path')

    _, currentNode = closestNode
    parentNode = currentNode[0]

    while parentNode is not None:
        _, x, y, _ = currentNode
        _, parentX, parentY, _ = parentNode
        pygame.draw.line(screen, (255, 165, 0), (x, y), (parentX, parentY), width = 2)
        currentNode = parentNode
        parentNode = currentNode[0]

    # Start and goal circles - draw last so they're on top
    pygame.draw.circle(screen, (0, 0, 0), (start_x, start_y), 5)
    pygame.draw.circle(screen, (255, 255, 0), goal_coords, 5)

    pygame.display.flip()
    printMe = False

pygame.quit()