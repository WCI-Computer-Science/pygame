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

    def setpos(self, x, y, safe=False, colliders=None): # Sets top-left position
        if safe:
            backuprect1 = self.rect1.move(0,0)
            backuprect2 = self.rect2.move(0,0)
        self.rect1.x = x
        self.rect1.y = y
        self.rect2.x = x+self.rect1.w
        self.rect2.y = y
        if safe and self.checkcollision(colliders):
            self.rect1 = backuprect1.move(0,0)
            self.rect2 = backuprect2.move(0,0)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.rect1colour, self.rect1)
        pygame.draw.rect(screen, self.rect2colour, self.rect2)
    
    def checkcollision(self, spritegroup):
        for i in spritegroup:
            if self.rect1.colliderect(i.rect) or self.rect2.colliderect(i.rect):
                return True
        return False
    
    def reset(self):
        self.rect1 = self.originalrect1.move(0, 0) # Re-set the rectangles, using .move() to ensure that they don't just point to self.originalrect#
        self.rect2 = self.originalrect2.move(0, 0)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.rect = pygame.Rect((x, y), (w, h))
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class MessageScreen():
    def __init__(self, screenwidth, screenheight, win=False):
        self.c = 0
        self.win = win
        self.backgroundrect = pygame.Rect((0, 0), (screenwidth, screenheight))
        font = pygame.font.Font(None, 100)
        self.text = font.render("You lost!", True, (255, 255, 255)) if not win else font.render("You passed the level!", True, (255, 255, 255))
        self.textrect = self.text.get_rect()
        self.textrect.center = (screenwidth/2, screenheight/2)
        self.canclick = False
        clickfont = pygame.font.Font(None, 30)
        self.clicktext = clickfont.render("Click to try again.", True, (255, 255, 255)) if not win else clickfont.render("Click to move on.", True, (255, 255, 255))
        self.clicktextrect = self.clicktext.get_rect()
        self.clicktextrect.center = (screenwidth/2, screenheight/2+100)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0) if not self.win else (0, 255, 0), self.backgroundrect)
        screen.blit(self.text, self.textrect)
        if self.canclick:
            screen.blit(self.clicktext, self.clicktextrect)

    def update(self, reset=False):
        if reset:
            self.c = 0
        else:
            self.c += 1
        out = 0
        if self.c > 20:
            if pygame.mouse.get_pressed()[0]:
                out = 1
            self.canclick = True
        return out

rects = Rectangles((350, 250), (400, 250), (50, 100), (50, 100), (0, 255, 0), (0, 0, 255), 20, WIDTH, HEIGHT)
walls = pygame.sprite.Group()
walls.add(Wall(125, 125, WIDTH-250, 25))
walls.add(Wall(125, HEIGHT-150, WIDTH-250, 25))
walls.add(Wall(125, 125, 25, HEIGHT-250))
walls.add(Wall(WIDTH-150, 125, 25, HEIGHT-250))

losescreen = MessageScreen(WIDTH, HEIGHT)
winscreen = MessageScreen(WIDTH, HEIGHT, win=True)

clock = pygame.time.Clock()

gamelevel = 1
prevgamelevel = 0

while True:
    clock.tick(FRAMERATE) # Stall until the next frame
    for event in pygame.event.get():
        if event.type == QUIT:
            raise SystemExit
        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            rects.setpos(pos[0], pos[1], safe=True, colliders=walls)
        if event.type == USEREVENT:
            if event.code == "LOSE":
                gamelevel = losescreen.update(reset=True)
                losescreen.draw(screen)

    if prevgamelevel != gamelevel:
        prevgamelevel = gamelevel
        rects.reset()
    screen.fill((255, 255, 255))
    if gamelevel != 0:
        rects.update()
        if rects.checkcollision(walls):
            loseevent = pygame.event.Event(USEREVENT, code="LOSE")
            pygame.event.post(loseevent)
        rects.draw(screen)
        for sprite in walls:
            sprite.draw(screen)
    else:
        gamelevel = losescreen.update()
        losescreen.draw(screen)
    pygame.display.update()