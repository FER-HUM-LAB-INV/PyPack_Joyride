from random import randint
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
explode = mixer.Sound('snd/Explode.mp3')
Elektric = mixer.Sound("snd/Elektrik.wav")
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

    def animate(self):
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
        elif self.fall <= -20:
            self.fall = -20

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


class Explosion(GameSprite):
    def __init__(self, filename, x, y, speed, w, h, kind, pos, launched, i):
        super().__init__(filename, x, y, speed, w, h, kind, pos, launched, i)
        self.frame = 0
        self.w = w
        self.h = h

    def explode(self):
        if self.frame == 0:
            explode.play()
        self.frame += 1
        if 0 <= self.frame <= 4:
            self.image = transform.scale(image.load("img/gif/2a9n-8.png"), (self.w, self.h))
        elif 5 <= self.frame <= 9:
            self.image = transform.scale(image.load("img/gif/2a9n-9.png"), (self.w, self.h))
        elif 10 <= self.frame <= 14:
            self.image = transform.scale(image.load("img/gif/2a9n-10.png"), (self.w, self.h))
        elif 15 <= self.frame <= 9:
            self.image = transform.scale(image.load("img/gif/2a9n-11.png"), (self.w, self.h))
        elif 20 <= self.frame <= 24:
            self.image = transform.scale(image.load("img/gif/2a9n-12.png"), (self.w, self.h))
        elif 25 <= self.frame <= 29:
            self.image = transform.scale(image.load("img/gif/2a9n-13.png"), (self.w, self.h))
        elif 30 <= self.frame <= 34:
            self.image = transform.scale(image.load("img/gif/2a9n-14.png"), (self.w, self.h))
        elif 35 <= self.frame <= 39:
            self.image = transform.scale(image.load("img/gif/2a9n-15.png"), (self.w, self.h))
        elif 40 <= self.frame <= 44:
            self.image = transform.scale(image.load("img/gif/2a9n-16.png"), (self.w, self.h))
        elif 45 <= self.frame <= 49:
            self.image = transform.scale(image.load("img/gif/17.png"), (self.w, self.h))
        elif 50 <= self.frame <= 54:
            self.image = transform.scale(image.load("img/gif/18.png"), (self.w, self.h))
        elif 55 <= self.frame <= 59:
            self.image = transform.scale(image.load("img/gif/19.png"), (self.w, self.h))
        elif 60 <= self.frame <= 64:
            self.image = transform.scale(image.load("img/gif/20.png"), (self.w, self.h))
        elif 65 <= self.frame <= 70:
            self.image = transform.scale(image.load("img/gif/21.png"), (self.w, self.h))

        transform.scale(self.image, (self.w, self.h))

        if self.frame == 70:
            self.rect.x = 100000


class BG(GameSprite):

    def __init__(self, filename, x, y, speed, w, h, kind, pos, launched, i):
        super().__init__(filename, x, y, speed, w, h, kind, pos, launched, i)

    def go(self):
        self.rect.x -= 20


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


class MissileTracer(GameSprite):

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


class Elektrik(GameSprite):
    def __init__(self, filename, x, y, speed, w, h, kind, pos, launched, i):
        super().__init__(filename, x, y, speed, w, h, kind, pos, launched, i)
        self.rect.x = 1001
        self.rect.y = randint(21, 718)

    def place(self):
        self.rect.x -= 22

        if self.rect.x <= -150:
            self.kill()


def reset(x, y):
    barry.rect.x = x
    barry.rect.y = y
    barry.fall = 0
    barry.kind = "run"

    bullet.rect.y = 1001

    for missile in missiles:
        missile.l = 1
        missile.launched = False
        missile.f = 1
        missile.i = 0
        missile.wait = 0
        missile.rect.x = 1024
        missile.rect.y = 0
    for elektrik in Elektrik_list:
        elektrik.l = 1
        elektrik.rect.x = 1001
    Elektrik_list.clear()


barry = Barry("img/Walk1.png", 20, 675, 10, 64, 74, "run", None, False, 0)

target = 'img/Missile_Target.png'

floor = GameSprite("img/BarryFullSpriteSheet.png", 0, 748, 0, 1024, 20, None, None, False, 0)
roof = GameSprite("img/BarryFullSpriteSheet.png", 0, 0, 0, 1024, 20, None, None, False, 0)
missile = MissileTracer(target, 0, 0, 26, 93, 34, None, None, False, 0)
missile2 = Missile(target, 0, 0, 26, 93, 34, None, None, False, 0)
missile3 = Missile(target, 0, 0, 26, 93, 34, None, None, False, 0)
missile4 = Missile(target, 0, 0, 26, 93, 34, None, None, False, 0)

bg = BG("img/bg.jpg", 0, 0, 0, 2740, 1000, None, None, None, None)
bg_rvrs = BG("img/bg_rvrs.jpg", 2740, 0, 0, 2740, 1000, None, None, None, None)

bgs = [bg, bg_rvrs]

explosion = Explosion("img/gif/2a9n-8.png", 0, 0, 0, 1000, 1000, None, None, None, None)

missiles = [missile, missile2, missile3, missile4]

bullet = Bullets("img/Bullet.png", 500, 450, 0, 10, 45, None, None, None, None)

bullets = [bullet]

Elektrik_list = []

stage = "menu"
while Game:
    for e in event.get():
        if e.type == QUIT:
            exit()
        elif stage == "menu" or stage == "lost":
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
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
        barry.animate()
        barry.move()
        barry.reset()
        for bullet in bullets:
            bullet.reset()
            bullet.rect.y += 25

        lnch = randint(1, 300)
        if missile.l == 0:
            for missile in missiles:
                missile.warning()
                missile.reset()
                if sprite.collide_rect(barry, missile):
                    stage = "lost"
                    explode.play()
        elif lnch == 35 or lnch == 45 or lnch == 55 or lnch == 65:
            for missile in missiles:
                missile.l = 0

        for elektrik in Elektrik_list:
            if elektrik.l == 0:
                elektrik.reset()
                elektrik.place()
                if sprite.collide_rect(barry, elektrik):
                    stage = "lost"
                    Elektric.play()

        if lnch == 70:
            elektrik = Elektrik("img/elektrik.png", 1001, 0, 0, 282, 68, None, None, None, None)
            elektrik.l = 0
            Elektrik_list.append(elektrik)

        elif lnch == 10:
            elektrik = Elektrik("img/elektrik_vert.png", 1001, 0, 0, 68, 282, None, None, None, None)
            elektrik.l = 0
            Elektrik_list.append(elektrik)

        explosion.reset()
        explosion.explode()

    elif stage == "lost":
        screen.fill((100, 0, 0))
        screen.blit(lost, (525 - lost.get_width() // 2, 375 - lost.get_height() // 2))

    clock.tick(fps)
    display.update()
