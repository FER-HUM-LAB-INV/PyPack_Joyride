from random import randint
import os
from pygame import *

init()
mixer.init()
font.init()

clock = time.Clock()
fps = 60

screen_width = 1024
screen_height = 768

screen = display.set_mode((screen_width, screen_height))
display.set_caption("PyPack Joyride")

warning = mixer.Sound("snd/Warning.mp3")
launch = mixer.Sound("snd/Launch.mp3")
theme = mixer.Sound("snd/Theme.mp3")
MS_DOS = font.Font("fnt/ModernDOS9x16.ttf", 100)
lost = MS_DOS.render("YOU LOST.", True, (0, 0, 0), None)

Game = True
m = 0


class GameSprite(sprite.Sprite):
    def __init__(self, filename, x, y, speed, w, h, kind, pos, launched, i):
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
        self.pos = pos
        self.launched = launched
        self.i = i

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        color = (255, 0, 0)
        draw.rect(screen, color, Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h), 2)


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

        elif self.kind == "fall":
            self.image = transform.scale(image.load('img/Walk1.png'), (self.w, self.h))

        if self.counter > 40:
            self.counter = 0

    def move(self):
        keys = key.get_pressed()
        if keys[K_SPACE]:
            bullet = Bullets("img/Bullet.png", self.rect.x, self.rect.y + self.h, 0, 10, 45, None, None, None, None)
            bullets.append(bullet)

            for bullet in bullets:
                bullet.shoot()

            self.kind = "fly"
            print(self.fall)
            self.rect.y -= self.fall
            self.fall += 0.5
            if sprite.collide_rect(self, floor):
                self.fall = 4

        if self.fall >= 10:
            self.fall = 10

        if sprite.collide_rect(barry, roof):
            barry.fall = 0

        if not keys[K_SPACE]:
            print(self.fall)
            self.fall -= 0.5
            self.rect.y -= self.fall
            if sprite.collide_rect(self, floor):
                self.fall = 0
                self.rect.y = 675
                self.kind = "run"
            elif not sprite.collide_rect(self, floor):
                self.kind = "fall"


class BG(GameSprite):

    def __init__(self, filename, x, y, speed, w, h, kind, pos, launched, i):
        super().__init__(filename, x, y, speed, w, h, kind, pos, launched, i)

    def go(self):
        self.rect.x -= 10


class Missile(GameSprite):

    def __init__(self, filename, x, y, speed, w, h, kind, pos, launched, i):
        super().__init__(filename, x, y, speed, w, h, kind, pos, launched, i)
        self.l = None
        self.f = None
        self.wait = None

    def animate(self):

        if 0 <= self.counter < 5:
            self.image = transform.scale(image.load('img/Rocket1.png'), (self.w, self.h))
        elif 5 <= self.counter < 10:
            self.image = transform.scale(image.load('img/Rocket2.png'), (self.w, self.h))
        elif 10 <= self.counter < 15:
            self.image = transform.scale(image.load('img/Rocket3.png'), (self.w, self.h))
        elif 15 <= self.counter < 20:
            self.image = transform.scale(image.load('img/Rocket4.png'), (self.w, self.h))

        self.counter += 1
        if self.counter >= 20:
            self.counter = 0

    def warning(self):
        if not self.launched:
            self.pos = randint(20, 714)
            warning.play()
            self.l = 0
        self.launch()

    def launch(self):

        if not self.launched:
            self.i = 0
            self.rect.x = 1024
            self.launched = True
            self.wait = 0
            self.f = 0

        if self.wait == 35:
            if self.i != 75:
                self.rect.x -= self.speed
                self.i += 1
            else:
                self.i = 0
                self.wait = 0
                self.launched = False
                self.l = 1

            if self.f != 1:
                launch.play()
                self.f = 1

            self.rect.y = self.pos
            self.animate()
        else:
            self.wait += 1


class Missile_Tracer(GameSprite):

    def __init__(self, filename, x, y, speed, w, h, kind, pos, launched, i):
        super().__init__(filename, x, y, speed, w, h, kind, pos, launched, i)
        self.l = None
        self.f = None
        self.wait = None

    def animate(self):

        if 0 <= self.counter < 5:
            self.image = transform.scale(image.load('img/Rocket1.png'), (self.w, self.h))
        elif 5 <= self.counter < 10:
            self.image = transform.scale(image.load('img/Rocket2.png'), (self.w, self.h))
        elif 10 <= self.counter < 15:
            self.image = transform.scale(image.load('img/Rocket3.png'), (self.w, self.h))
        elif 15 <= self.counter < 20:
            self.image = transform.scale(image.load('img/Rocket4.png'), (self.w, self.h))

        self.counter += 1
        if self.counter >= 20:
            self.counter = 0

    def warning(self):
        if not self.launched:
            self.rect.y = barry.rect.y
            warning.play()
            self.l = 0
        self.launch()

    def launch(self):

        if not self.launched:
            self.i = 0
            self.rect.x = 1024
            self.launched = True
            self.wait = 0
            self.f = 0

        if self.wait == 35:
            if self.i != 75:
                self.rect.x -= self.speed
                self.i += 1
            else:
                self.i = 0
                self.wait = 0
                self.launched = False
                self.l = 1

            if self.f != 1:
                launch.play()
                self.f = 1

            self.animate()
        else:
            self.wait += 1


class Bullets(GameSprite):

    def shoot(self):
        j = randint(-15, 10)
        self.rect.x = barry.rect.x + 23.5 + j


def reset(x, y):
    barry.rect.x = x
    barry.rect.y = y
    barry.fall = 0
    barry.kind = "run"

    for bullet in bullets:
        bullet.rect.y = 1001

    for missile in missiles:
        missile.l = 1
        missile.launched = False
        missile.f = 1
        missile.i = 0
        missile.wait = 0
        missile.rect.x = 1024
        missile.rect.y = 0


barry = Barry("img/Walk1.png", 20, 675, 10, 64, 74, "run", None, False, 0)

floor = GameSprite("img/BarryFullSpriteSheet.png", 0, 748, 0, 1024, 20, None, None, False, 0)
roof = GameSprite("img/BarryFullSpriteSheet.png", 0, 0, 0, 1024, 20, None, None, False, 0)
missile = Missile_Tracer("img/Missile_Target.png", 0, 0, 20, 93, 34, None, None, False, 0)
missile2 = Missile("img/Missile_Target.png", 0, 0, 20, 93, 34, None, None, False, 0)
missile3 = Missile("img/Missile_Target.png", 0, 0, 20, 93, 34, None, None, False, 0)
missile4 = Missile("img/Missile_Target.png", 0, 0, 20, 93, 34, None, None, False, 0)

bg = BG("img/bg.jpg", 0, 0, 0, 2740, 1000, None, None, None, None)
bg_rvrs = BG("img/bg_rvrs.jpg", 2740, 0, 0, 2740, 1000, None, None, None, None)

bgs = [bg, bg_rvrs]

missiles = [missile, missile2, missile3, missile4]

bullet = Bullets("img/Bullet.png", 500, 450, 0, 10, 45, None, None, None, None)

bullets = [bullet]

stage = "menu"
while Game:
    for e in event.get():
        if e.type == QUIT:
            exit()
        elif stage == "menu" or stage == "lost":
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    stage = "run"
                    reset(20, 675)

    if stage == "run":
        if m == 0:
            theme.play()
            m = 1
        screen.fill((100, 100, 100))
        if bg.rect.x == -2740:
            bg.rect.x = 2740
        elif bg_rvrs.rect.x == -2740:
            bg_rvrs.rect.x = 2740
        bg.reset()
        bg.go()
        bg_rvrs.reset()
        bg_rvrs.go()

        floor.reset()
        roof.reset()
        barry.animation()
        barry.move()
        barry.reset()
        for bullet in bullets:
            bullet.reset()
            bullet.rect.y += 1

        lnch = randint(1, 70)
        if missile.l == 0:
            for missile in missiles:
                missile.warning()
                missile.reset()
                if sprite.collide_rect(barry, missile):
                    stage = "lost"
        elif lnch == 35:
            for missile in missiles:
                missile.warning()
                missile.reset()
                if sprite.collide_rect(barry, missile):
                    stage = "lost"

    elif stage == "lost":
        screen.fill((100, 0, 0))
        screen.blit(lost, (525 - lost.get_width() // 2, 375 - lost.get_height() // 2))

    clock.tick(fps)
    display.update()
