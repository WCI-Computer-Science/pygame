import pygame
from pygame.locals import *

FRAMERATE = 30

pygame.init()

screen = pygame.display.set_mode((800, 600))

class Rectangles():
    def __init__(self, rect1startpos, rect2startpos, rect1size, rect2size, rect1colour, rect2colour, speed):
        self.rect1 = pygame.Rect(rect1startpos, rect1size)
        self.rect2 = pygame.Rect(rect2startpos, rect2size)
        self.rect1colour = rect1colour
        self.rect2colour = rect2colour
        self.speed = speed

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.rect1 = self.rect1.move(0, -self.speed)
            self.rect2 = self.rect2.move(0, -self.speed)
        if keys[K_a]:
            self.rect1 = self.rect1.move(-self.speed, 0)
            self.rect2 = self.rect2.move(-self.speed, 0)
        if keys[K_s]:
            self.rect1 = self.rect1.move(0, self.speed)
            self.rect2 = self.rect2.move(0, self.speed)
        if keys[K_d]:
            self.rect1 = self.rect1.move(self.speed, 0)
            self.rect2 = self.rect2.move(self.speed, 0)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.rect1colour, self.rect1)
        pygame.draw.rect(screen, self.rect2colour, self.rect2)
        


rects = Rectangles((200, 150), (400, 150), (200, 300), (200, 300), (0, 255, 0), (0, 0, 255), 20)

clock = pygame.time.Clock()

while True:
    clock.tick(FRAMERATE) # Stall until the next frame
    for event in pygame.event.get():
        if event.type == QUIT:
            raise SystemExit
    rects.update()
    screen.fill((255, 255, 255))
    rects.draw(screen)
    pygame.display.update()