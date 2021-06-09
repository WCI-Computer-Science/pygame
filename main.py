import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            raise SystemExit
    pygame.display.update()