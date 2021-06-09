import pygame
from pygame.locals import *

FRAMERATE = 30
WIDTH = 800
HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Rectangles():
    def __init__(self, rect1startpos, rect2startpos, rect1size, rect2size, rect1colour, rect2colour, speed, windowwidth, windowheight):
        self.rect1 = pygame.Rect(rect1startpos, rect1size)
        self.rect2 = pygame.Rect(rect2startpos, rect2size)
        self.originalrect1 = pygame.Rect(rect1startpos, rect1size)
        self.originalrect2 = pygame.Rect(rect2startpos, rect2size)
        self.rect1colour = rect1colour
        self.rect2colour = rect2colour
        self.speed = speed
        self.windowrect = pygame.Rect((0, 0), (windowwidth, windowheight))

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
        if self.rect1.x < self.windowrect.x:
            self.rect1.x = self.windowrect.x
            self.rect2.x = self.windowrect.x + self.rect1.w
        if self.rect1.y < self.windowrect.y:
            self.rect1.y = self.windowrect.y
            self.rect2.y = self.windowrect.y
        if self.rect2.right > self.windowrect.right:
            self.rect1.x = self.windowrect.right-self.rect2.w-self.rect1.w
            self.rect2.x = self.windowrect.right-self.rect2.w
        if self.rect2.bottom > self.windowrect.bottom:
            self.rect1.y = self.windowrect.bottom-self.rect1.height
            self.rect2.y = self.windowrect.bottom-self.rect2.height

    def setpos(self, x, y): # Sets top-left position
        self.rect1.x = x
        self.rect1.y = y
        self.rect2.x = x+self.rect1.w
        self.rect2.y = y
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.rect1colour, self.rect1)
        pygame.draw.rect(screen, self.rect2colour, self.rect2)
    
    def checkcollision(self, spritegroup):
        for i in spritegroup:
            if self.rect1.colliderect(i.rect) or self.rect1.colliderect(i.rect):
                return True
        return False
    
    def reset(self):
        self.rect1 = self.originalrect1
        self.rect2 = self.originalrect2

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.rect = pygame.Rect((x, y), (w, h))
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

rects = Rectangles((200, 150), (400, 150), (200, 300), (200, 300), (0, 255, 0), (0, 0, 255), 20, WIDTH, HEIGHT)
walls = pygame.sprite.Group()
walls.add(Wall(100, 100, 40, 20))

clock = pygame.time.Clock()

while True:
    clock.tick(FRAMERATE) # Stall until the next frame
    for event in pygame.event.get():
        if event.type == QUIT:
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            rects.setpos(pos[0], pos[1])
        
    rects.update()
    if rects.checkcollision(walls):
        rects.reset()
    screen.fill((255, 255, 255))
    rects.draw(screen)
    for sprite in walls:
        sprite.draw(screen)
    pygame.display.update()