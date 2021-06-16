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
        self.backuprect = pygame.Rect(topleft, wh)
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
        pygame.draw.rect(screen, (0, 255, 0), self.rect)
    
    def goto(self, pos, walls):
        rectcenterbackup = self.rect.center
        self.rect.center = pos
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.center = rectcenterbackup

    def reset(self):
        self.rect = self.backuprect.move(0, 0)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.rect = pygame.Rect((x, y), (w, h))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class LoseScreen():
    def __init__(self, screensize):
        self.screensize = screensize
        self.screenrect = pygame.Rect((0, 0), screensize)
        self.font = pygame.font.Font(None, 100)
        self.text = self.font.render("You lost!", True, (255, 255, 255))
        self.textrect = self.text.get_rect(center = (screensize[0]/2, screensize[1]/2))
        self.count = 0
    
    def draw(self, screen):
        if self.count > 0:
            pygame.draw.rect(screen, (255, 0, 0), self.screenrect)
            screen.blit(self.text, self.textrect)

    def update(self, reset=False):
        if reset:
            self.count = 40
            return 0
        self.count -= 1
        return 0 if self.count > 0 else 1

rect = Rectangles((200, 150), (100, 100), 10, (WIDTH, HEIGHT))
losescreen = LoseScreen((WIDTH, HEIGHT))
level = 1

clock = pygame.time.Clock()

walls = pygame.sprite.Group()
walls.add(Wall(0, 0, 100, 100))
walls.add(Wall(400, 0, 100, 100))

while True:
    clock.tick(FRAMERATE)
    for event in pygame.event.get():
        if event.type == QUIT:
            raise SystemExit
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                rect.goto(event.pos, walls)
        elif event.type == USEREVENT and event.code == "LOSE":
            level = losescreen.update(reset=True)
            rect.reset()
    screen.fill((255,255,255))
    if level == 0:
        level = losescreen.update()
        losescreen.draw(screen)
    else:
        rect.update()
        rect.draw(screen)
        for wall in walls:
            wall.draw(screen)
            if rect.rect.colliderect(wall.rect):
                pygame.event.post(pygame.event.Event(USEREVENT, code="LOSE"))


    pygame.display.update()
