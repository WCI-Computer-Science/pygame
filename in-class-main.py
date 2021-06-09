import pygame
from pygame.locals import *

FRAMERATE = 30
WIDTH = 800
HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Rectangles():
    def __init__(self, topleft, wh, speed, screensize):
        self.rect = pygame.Rect(topleft, wh)
        self.speed = speed
        self.screen = pygame.Rect((0, 0), screensize)
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.rect = self.rect.move(0, -self.speed)
        if keys[K_LEFT]:
            self.rect = self.rect.move(-self.speed, 0)
        if keys[K_DOWN]:
            self.rect = self.rect.move(0, self.speed)
        if keys[K_RIGHT]:
            self.rect = self.rect.move(self.speed, 0)
        
        if self.rect.y < self.screen.y:
            self.rect.y = self.screen.y
        if self.rect.x < self.screen.x:
            self.rect.x = self.screen.x
        if self.rect.bottom > self.screen.bottom:
            self.rect.y = self.screen.bottom-self.rect.height
        if self.rect.right > self.screen.right:
            self.rect.x = self.screen.right-self.rect.width

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

rect = Rectangles((200, 150), (200, 300), 10, (WIDTH, HEIGHT))

clock = pygame.time.Clock()

while True:
    clock.tick(FRAMERATE)
    for event in pygame.event.get():
        if event.type == QUIT:
            raise SystemExit
    screen.fill((255,255,255))
    rect.update()
    rect.draw(screen)

    pygame.display.update()