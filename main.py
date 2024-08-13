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


class GameSprite(sprite.Sprite):
    def __init__(self, filename, x, y, speed, w, h, kind):
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
        self.kind = kind

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Barry(GameSprite):

    def animation(self):
        self.counter += 1
        if self.kind == "run":
            if 0 <= self.counter < 10:
                self.image = transform.scale(image.load('img/Walk1.png'), (self.w, self.h))
            elif 10 <= self.counter < 20:
                self.image = transform.scale(image.load('img/Walk2.png'), (self.w, self.h))
            elif 20 <= self.counter < 30:
                self.image = transform.scale(image.load('img/Walk3.png'), (self.w, self.h))
            elif 30 <= self.counter < 40:
                self.image = transform.scale(image.load('img/Walk4.png'), (self.w, self.h))

        elif self.kind == "fly":
            if 0 <= self.counter < 5:
                self.image = transform.scale(image.load('img/Fly1.png'), (self.w, self.h))
            elif 5 <= self.counter < 10:
                self.image = transform.scale(image.load('img/Fly2.png'), (self.w, self.h))
            elif 10 <= self.counter < 15:
                self.image = transform.scale(image.load('img/Fly3.png'), (self.w, self.h))
            elif 15 <= self.counter < 20:
                self.image = transform.scale(image.load('img/Fly1.png'), (self.w, self.h))
            elif 20 <= self.counter < 25:
                self.image = transform.scale(image.load('img/Fly2.png'), (self.w, self.h))
            elif 25 <= self.counter < 30:
                self.image = transform.scale(image.load('img/Fly3.png'), (self.w, self.h))
            elif 30 <= self.counter < 35:
                self.image = transform.scale(image.load('img/Fly2.png'), (self.w, self.h))
            elif 35 <= self.counter < 40:
                self.image = transform.scale(image.load('img/Fly3.png'), (self.w, self.h))

        elif self.kind == "fly":
            self.image = transform.scale(image.load('img/FlyFall.png'), (self.w, self.h))

        if self.counter > 40:
            self.counter = 0

    def move(self):
        keys = key.get_pressed()
        if keys[K_SPACE]:
            self.kind = "fly"
            print(self.fall)
            self.rect.y -= self.fall
            self.fall += 0.5
            if self.fall >= 10:
                self.fall = 10
            if sprite.collide_rect(self, floor):
                self.fall = 4
        if not keys[K_SPACE]:
            print(self.fall)
            self.fall -= 0.5
            self.rect.y -= self.fall
            if self.fall >= 10:
                self.fall = 10
            elif sprite.collide_rect(self, floor):
                self.fall = 0
                self.rect.y = 675
                self.kind = "run"
            elif not sprite.collide_rect(self, floor):
                self.kind = "fall"


barry = Barry("img/Walk1.png", 20, 675, 10, 64, 74, "run")

floor = GameSprite("img/BarryFullSpriteSheet.png", 0, 748, 0, 1024, 20, None)
roof = GameSprite("img/BarryFullSpriteSheet.png", 0, 0, 0, 1024, 20, None)


stage = "menu"
while Game:
    for e in event.get():
        if e.type == QUIT:
            exit()
        elif stage == "menu":
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    print("a")
                    stage = "run"

    if stage == "run":
        floor.reset()
        roof.reset()
        barry.animation()
        barry.move()
        barry.reset()

        keys = key.get_pressed()
        if keys[K_SPACE] and sprite.collide_rect(barry, floor):
            barry.fall = 4
        elif sprite.collide_rect(barry, roof):
            barry.fall = 0
        elif not keys[K_SPACE]:
            if sprite.collide_rect(barry, floor):
                barry.fall = 0
                barry.rect.y = 675
                barry.kind = "run"
            elif not sprite.collide_rect(barry, floor):
                barry.kind = "fall"

    clock.tick(fps)
    display.update()
