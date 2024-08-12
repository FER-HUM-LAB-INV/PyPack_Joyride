from time import sleep
import os
from pygame import *

init()

clock = time.Clock()
fps = 60

screen_width = 1024
screen_height = 768

screen = display.set_mode((screen_width, screen_height))
display.set_caption("PyPack Joyride")

Game = True


Sheet = image.load("img/BarryFullSpriteSheet.png")
Walk1 = image.load("img/Walk1.png")
Walk2 = image.load("img/Walk2.png")
Walk3 = image.load("img/Walk3.png")
Walk4 = image.load("img/Walk4.png")


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        pos = mouse.get_pos()

        if self.rect.collidepoint(pos):
            if mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if mouse.get_pressed()[0] == 0:
            self.clicked = False

        # button
        screen.blit(self.image, self.rect)

        return action

    def reset(self):
        screen.blit(self.image, (self.x, self.y))


class GameSprite(sprite.Sprite):
    def __init__(self, filename, x, y, speed, w, h):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(image.load(filename), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self.counter = 0
        self.fall = 0

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Barry(GameSprite):
    def animation(self):
        self.counter += 1
        if 0 <= self.counter < 10:
            self.image = transform.scale(image.load('img/Walk1.png'), (self.w, self.h))
        elif 10 <= self.counter < 20:
            self.image = transform.scale(image.load('img/Walk2.png'), (self.w, self.h))
        elif 20 <= self.counter < 30:
            self.image = transform.scale(image.load('img/Walk3.png'), (self.w, self.h))
        elif 30 <= self.counter < 40:
            self.image = transform.scale(image.load('img/Walk4.png'), (self.w, self.h))

        if self.counter > 40:
            self.counter = 0

    def move(self):
        keys = key.get_pressed()
        if keys[K_SPACE]:
            self.rect.y -= self.speed
            self.fall = self.speed
        if not keys[K_SPACE]:
            self.fall += 0.5
            self.rect.y += self.fall
            if self.fall >= 10:
                self.fall = 10
            elif sprite.spritecollide(self, floor, False):
                self.fall = -0.25


barry = Barry("img/Walk1.png", 20, 664, 10, 64, 74)

floor = GameSprite("img/BarryFullSpriteSheet.png", 0, 0, 0, 10, 10)


while Game:
    for e in event.get():
        if e.type == QUIT:
            exit()

    k = key.get_pressed()
    if k == K_TAB:
        barry -= 5

    floor.reset()
    screen.fill((100, 100, 100))
    barry.animation()
    barry.move()
    barry.reset()
    clock.tick(fps)
    display.update()
