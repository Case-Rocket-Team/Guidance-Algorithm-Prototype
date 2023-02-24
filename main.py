import numpy as np
import pygame
import constants
from rrt import RRT, circle_from, start_RRT_return_formated_path

# Initialize pygame + some constants
pygame.init()

size = width, height = constants.SCREEN_DIM
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))

start_coords = start_x, start_y = constants.ORIGIN_COORDS 
initHeading = np.array([0, -1]) # in this case, rocket starts facing up

goal_coords = goal_x, goal_y = constants.GOAL_COORDS

running = True # pygame draw loop only runs when this is True - set to False to quit

# Draw black circle at start and yellow circle at goal
pygame.draw.circle(screen, (0, 0, 0), (start_x, start_y), 5)
pygame.draw.circle(screen, (255, 255, 0), goal_coords, 5)

printMe = True

# Generate tree
reachedGoal = False
while not reachedGoal:
    print('Trying for new RRT')
    screen.fill((255, 255, 255))
    #            origin (None), x,   y,          heading,      length, goal,maxIterations
    reachedGoal, final_node = RRT((None, start_x, start_y, np.array([0, -1]), 0, None), goal_coords, constants.MAX_ITERATIONS, screen)

print(final_node)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Backtrack through final_node's history and draw arcs between each node
    currentNode = final_node
    parentNode, x, y, _, tot_length, _ = currentNode

    # Print out some nice stats about the path we chose
    if printMe:
        print('Length of final path: ', tot_length)
        print('X and Y of closest node: ', x, y)
        print('Drawing ideal path')

    while parentNode is not None:
        _, x, y, _b, _c, _d = currentNode
        _, parentX, parentY, tang, _c, _d = parentNode
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

    # Start and goal circles - draw last so they're on top
    pygame.draw.circle(screen, (0, 0, 0), (start_x, start_y), 5)
    pygame.draw.circle(screen, (255, 255, 0), goal_coords, 5)

    pygame.display.flip()
    printMe = False

pygame.quit()
