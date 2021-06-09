import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800, 600))
rect = pygame.Rect((200, 150), (200, 300))
rect2 = pygame.Rect((400, 150), (200, 300))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            raise SystemExit
        if event.type == KEYDOWN:
            if event.key == K_w:
                rect = rect.move(0, -1)
            elif event.key == K_a:
                rect = rect.move(-1, 0)
            elif event.key == K_s:
                rect = rect.move(0, 1)
            elif event.key == K_d:
                rect = rect.move(1, 0)
    
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 255, 0), rect)
    pygame.draw.rect(screen, (0, 0, 255), rect2)
    pygame.display.update()