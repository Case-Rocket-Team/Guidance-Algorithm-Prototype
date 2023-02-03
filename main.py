import numpy as np
import pygame
from rrt import RRT

pygame.init()

size = width, height = (400, 400)
screen = pygame.display.set_mode(size)
black = 255, 255, 255

running = True
test_tree = RRT((200, 200), (200, 200), 20, 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(black)
    pygame.draw.circle(screen, (0, 0, 0), (200, 200), 5);

    for node in test_tree:
        pygame.draw.circle(screen, (0, 0, 255), (node[1], node[2]), 2)

    pygame.display.flip()

pygame.quit()