import time
import numpy as np
import pygame
import rust_funcs

SCREEN_DIM = 1000, 700
DRAW_STUFF = True
PRINT = False



start_x, start_y = 600,400
goal_x, goal_y = 450,450
tang_x,tang_y = 1, 3
gas = 1000
points = []


# Initialize pygame + some constants
size = width, height = SCREEN_DIM

screen = None
if DRAW_STUFF:
    pygame.init()
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))

start_coords = start_x, start_y
initHeading = np.array([0, -1]) # in this case, rocket starts facing up

goal_coords = goal_x, goal_y

running = True # pygame draw loop only runs when this is True - set to False to quit

# Draw black circle at start and yellow circle at goal
if DRAW_STUFF:
    pygame.draw.circle(screen, (0, 0, 0), (start_x, start_y), 5)
    pygame.draw.circle(screen, (255, 255, 0), goal_coords, 5)

printMe = True

pygameScreen = None
if DRAW_STUFF:
    screen.fill((255, 255, 255))
    pygameScreen = screen

##----##
reet = rust_funcs.rrt(start_x,start_y,tang_x,tang_y,goal_x,goal_y,gas)
for x in reet:
    points.append(x)
##----##

drawn_final_path = False

while DRAW_STUFF and running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    current = points[-2].to_dict()
    goal = points[-1].to_dict()
    # Print out some nice stats about the path we chose
    if printMe:
        print('Path stats:')
        print('Length of final path: ', len(points))
        print('X and Y of closest node: ', current["coords"],current["coords"])

    for i in range(len(points)-2,0,-1):
        radius, arclen, newHead, center = rust_funcs.circle_from(points[i],points[-1])
        current = points[i].to_dict()
        currentX = current["coords"][0]
        currentY = current["coords"][1]
        parent = points[i-1].to_dict()
        parentX = parent["coords"][0]
        parentY = parent["coords"][1]
        startRadians = np.arctan2(parentY - center[1], parentX - center[0])
        endRadians = np.arctan2(currentY - center[1], currentX - center[0])
        
        if radius < 0:
            radius *= -1
            startRadians, endRadians = -endRadians, -startRadians
        else:
            startRadians, endRadians = -startRadians, -endRadians

        pygame.draw.arc(screen, (255, 165, 0), (center[0] - radius, center[1] - radius, radius * 2, radius * 2), startRadians, endRadians, 2)
        pygame.draw.circle(screen, (255, 0, 0), (currentX, currentY), 3)

        pygame.display.flip()
        time.sleep(0.05)

    # Start and goal circles - draw last so they're on top
    pygame.draw.circle(screen, (0, 0, 0), (start_x, start_y), 5)
    pygame.draw.circle(screen, (255, 255, 0), goal_coords, 5)
    #pygame.draw.arc(screen, (0, 255, 0), ((goal_coords[0] - 13, goal_coords[1] - 13), (26, 26)), 0, 360, 2)

    pygame.display.flip()
    printMe = False

pygame.quit()
