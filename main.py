import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))

while True:
    for i in pygame.event.get():
        pass
    pygame.display.update()