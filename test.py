import numpy as np
import pygame
from rrt import circle_from

p1 = np.array([100, 100])
h1 = np.array([1, -1])

p2 = np.array([200, 180])
p3 = np.array([300, 300])

r1, al1, h2, c1 = circle_from(p1, p2, (h1[0], h1[1]))
r2, al2, h3, c2 = circle_from(p2, p3, h2)

pygame.init()
size = width, height = (400, 400)
screen = pygame.display.set_mode(size)
black = 255, 255, 255
screen.fill(black)
pygame.display.update()

# draw points
pygame.draw.circle(screen, (0, 0, 0), (int(p1[0]), int(p1[1])), 5)
pygame.draw.circle(screen, (0, 0, 0), (int(p2[0]), int(p2[1])), 5)
pygame.draw.circle(screen, (0, 0, 0), (int(p3[0]), int(p3[1])), 5)
pygame.display.update()

pygame.draw.line(screen, (255, 0, 0), (int(p1[0]), int(p1[1])), (int(p1[0] + h1[0] * 15), int(p1[1] + h1[1] * 15)))
pygame.display.update()

# draw arcs between p1 and p2, using r1 as radius and c1 as the circle's center, p1 as the start point and p2 as the end point
sr1 = np.arctan2(p1[1] - c1[1], p1[0] - c1[0])
er1 = np.arctan2(p2[1] - c1[1], p2[0] - c1[0])
pygame.draw.arc(screen, (0, 0, 255), (int(c1[0] - r1), int(c1[1] - r1), int(r1 * 2), int(r1 * 2)), sr1, er1, 1)
pygame.display.update()

# draw arcs between p2 and p3, using r2 as radius and c2 as the circle's center, p2 as the start point and p3 as the end point
sr2 = np.arctan2(p2[1] - c2[1], p2[0] - c2[0])
er2 = np.arctan2(p3[1] - c2[1], p3[0] - c2[0])

pygame.draw.line(screen, (255, 0, 0), (int(p2[0]), int(p2[1])), (int(p2[0] - h2[0] * 1), int(p2[1] - h2[1] * 1)))
pygame.draw.arc(screen, (0, 0, 255), (int(c2[0] - r2), int(c2[1] - r2), int(r2 * 2), int(r2 * 2)), sr2, er2, 1)
pygame.draw.line(screen, (255, 0, 0), (int(p3[0]), int(p3[1])), (int(p3[0] + h3[0] * 1), int(p3[1] + h3[1] * 1)))
pygame.display.update()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()