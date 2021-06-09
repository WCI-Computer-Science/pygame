import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
rect = pygame.Rect((200, 150), (200, 300))
rect2 = pygame.Rect((400, 150), (200, 300))
pygame.draw.rect(screen, (0, 255, 0), rect)
pygame.draw.rect(screen, (0, 0, 255), rect2)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            raise SystemExit
    pygame.display.update()