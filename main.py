import numpy as np
import pygame

pygame.init()

size = width, height = (400, 400)
screen = pygame.display.set_mode(size)
black = 255, 255, 255

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(black)
    pygame.draw.circle(screen, (255, 255, 255), (200, 200), 2)
    pygame.display.flip()

pygame.quit()