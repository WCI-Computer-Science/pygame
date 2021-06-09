import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))

pygame.draw.circle(screen, (0, 0, 0), (400, 300), 25)
pygame.draw.rect(screen, (255, 0, 0), ((200, 150), (200, 300)))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            raise SystemExit
    pygame.display.update()