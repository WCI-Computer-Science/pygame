import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800, 600))

class Rectangles():
    def __init__(self, rect1startpos, rect2startpos, rect1size, rect2size, rect1colour, rect2colour):
        self.rect1 = pygame.Rect(rect1startpos, rect1size)
        self.rect2 = pygame.Rect(rect2startpos, rect2size)
        self.rect1colour = rect1colour
        self.rect2colour = rect2colour

rects = Rectangles((200, 150), (400, 150), (200, 300), (200, 300), (0, 255, 0), (0, 0, 255))

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
    pygame.display.update()