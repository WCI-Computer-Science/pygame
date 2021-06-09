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
        self.rect = pygame.Rect((x, y), (w, h))
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class WinShape(pygame.sprite.Sprite):
    def __init__(self, centerx, centery, radius):
        super().__init__()
        self.center = (centerx, centery)
        self.radius = radius
        self.rect = pygame.draw.circle(screen, (0, 255, 0), self.center, self.radius) #pygame.draw returns the bounding box of what it draws, so that's our rect

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), self.center, self.radius)

class MessageScreen():
    def __init__(self, screenwidth, screenheight):
        self.c = 0
        self.moveon = False
        self.backgroundrect = pygame.Rect((0, 0), (screenwidth, screenheight))
        self.font = pygame.font.Font(None, 100)
        self.canclick = False
        self.clickfont = pygame.font.Font(None, 30)
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.nextlevel = 1
        self.win = False
        

    def draw(self, screen):

        text = (self.font.render("You lost!", True, (255, 255, 255)) if not self.moveon else self.font.render("You passed the level!", True, (255, 255, 255))) if not self.win else self.font.render("You won!", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (self.screenwidth/2, self.screenheight/2)

        pygame.draw.rect(screen, (255, 0, 0) if not self.moveon and not self.win else (0, 255, 0), self.backgroundrect)
        screen.blit(text, textrect)
        if self.canclick:
            clicktext = (self.clickfont.render("Click to try again.", True, (255, 255, 255)) if not self.moveon else self.clickfont.render("Click to move on.", True, (255, 255, 255))) if not self.win else self.clickfont.render("Click to restart.", True, (255, 255, 255))
            clicktextrect = clicktext.get_rect()
            clicktextrect.center = (self.screenwidth/2, self.screenheight/2+100)
            screen.blit(clicktext, clicktextrect)

    def update(self, win=False, moveon=False, reset=False, nextlevel=1):
        if reset:
            self.nextlevel = nextlevel
            self.win = win
            self.moveon = moveon
            self.canclick = False
            self.c = 0
        else:
            self.c += 1
        out = 0
        if self.c > 20:
            if pygame.mouse.get_pressed()[0]:
                out = self.nextlevel
            self.canclick = True
        return out

rects = Rectangles((350, 250), (400, 250), (50, 100), (50, 100), (0, 255, 0), (0, 0, 255), 20, WIDTH, HEIGHT)

walllist = []
winslist = []
## Level 1
walllist.append(pygame.sprite.Group())
walllist[-1].add(Wall(125, 125, WIDTH-250, 25))
walllist[-1].add(Wall(125, HEIGHT-150, WIDTH-250, 25))
walllist[-1].add(Wall(125, 125, 25, HEIGHT-250))
walllist[-1].add(Wall(WIDTH-150, 125, 25, HEIGHT-250))
winslist.append(pygame.sprite.Group())
winslist[-1].add(WinShape(50, 50, 25))

messagescreen = MessageScreen(WIDTH, HEIGHT)

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
                gamelevel = messagescreen.update(reset=True)
                messagescreen.draw(screen)
            elif event.code == "WIN":
                gamelevel = messagescreen.update(moveon=True, reset=True, nextlevel=gamelevel+1)
                messagescreen.draw(screen)

    if prevgamelevel != gamelevel:
        prevgamelevel = gamelevel
        rects.reset()
    screen.fill((255, 255, 255))
    if gamelevel != 0:
        if gamelevel > len(walllist) or gamelevel > len(winslist):
            gamelevel = messagescreen.update(win=True, reset=True)
            pygame.display.update()
            continue
        walls = walllist[gamelevel-1]
        wins = winslist[gamelevel-1]
        rects.update()
        if rects.checkcollision(walls):
            loseevent = pygame.event.Event(USEREVENT, code="LOSE")
            pygame.event.post(loseevent)
        if rects.checkcollision(wins):
            winevent = pygame.event.Event(USEREVENT, code="WIN")
            pygame.event.post(winevent)
        rects.draw(screen)
        for sprite in walls:
            sprite.draw(screen)
        for sprite in wins:
            sprite.draw(screen)
        
    else:
        gamelevel = messagescreen.update()
        messagescreen.draw(screen)
    pygame.display.update()