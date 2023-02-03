import numpy as np
import pygame
from rrt import RRT

pygame.init()

size = width, height = (400, 400)
screen = pygame.display.set_mode(size)
black = 255, 255, 255

running = True
test_tree = RRT((None, 200, 200, -np.pi / 4), (200, 200), 15, 30)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(black)
    pygame.draw.circle(screen, (0, 0, 0), (200, 200), 5);

    # test
    heading = -np.pi / 4 
    orthogonalRight = heading + np.pi / 2
    orthogonalLeft = heading - np.pi / 2
    orthoRightPt = (200 + 30 * np.cos(orthogonalRight), 200 + 30 * np.sin(orthogonalRight))
    orthoLeftPt = (200 + 30 * np.cos(orthogonalLeft), 200 + 30 * np.sin(orthogonalLeft))
    pygame.draw.circle(screen, (255, 0, 0), orthoRightPt, 30)
    pygame.draw.circle(screen, (255, 0, 0), orthoLeftPt, 30)
    # pygame.draw.line(screen, (0, 0, 255), (200, 200), (200 + 20 * np.cos(heading), 200 + 20 * np.sin(heading)))

    for node in test_tree:
        pygame.draw.circle(screen, (0, 0, 255), (node[1], node[2]), 2)
        originPoint, pointX, pointY, pointHeading = node
        if originPoint is not None:
            _, originX, originY, _b = originPoint
            pygame.draw.line(screen, pygame.Color(0, 255, 0, a = 30), (originX, originY), (pointX, pointY), width = 1)

    pygame.display.flip()

pygame.quit()