from random import randint
from pygame import *
from time import sleep
import os

init()
mixer.init()
font.init()

clock = time.Clock()
fps = 60

screen_width = 1366
screen_height = 768

screen = display.set_mode((screen_width, screen_height))
display.set_caption("PyPack Joyride")


MS_DOS = font.Font("fnt/ModernDOS9x16.ttf", 100)
MS_DOS_smol = font.Font("fnt/ModernDOS9x16.ttf", 25)


lost = MS_DOS.render("YOU LOST.", True, (0, 0, 0), None)
disclaimer = MS_DOS.render("DISCLAIMER!!!!", True, (255, 0, 0))
recreation = MS_DOS_smol.render("THIS IS ONLY A RECREATION, NOT A STOLEN GAME!!!", True, (255, 0, 0))
halfbrick = MS_DOS_smol.render("ALL RIGHTS RESERVED FOR HALFBRICK STUDIOS!!!", True, (255, 0, 0))
click = MS_DOS_smol.render("PRESS ANYWHERE TO CONTINUE...", True, (255, 255, 255))
github = MS_DOS_smol.render('Press "G" to redirect to the repository.', True, (255, 255, 255))
loading = MS_DOS.render("LOADING...", True, (255, 255, 255))
tmtaw = MS_DOS_smol.render("THIS MIGHT TAKE A WHILE...", True, (255, 255, 255))
help = MS_DOS_smol.render("You need help, don't you?", True, (255, 255, 255))
lhelp = MS_DOS_smol.render("If you need help, tap 'H'.", True, (255, 255, 255))
ihelp = MS_DOS_smol.render("That will decrease the chances of the obstacles appearing.", True, (255, 255, 255))
usure = MS_DOS.render("ARE YOU SURE???", True, (150, 0, 0))
usure2 = MS_DOS_smol.render("If you click, you will continue.", True, (150, 0, 0))
usure3 = MS_DOS_smol.render('If you tap "h", then you will continue easily.', True, (150, 0, 0))

while True:
    for e in event.get():
        if e.type == QUIT:
            exit()

    print(lost.get_width(), disclaimer.get_width(), recreation.get_width(), halfbrick.get_width(), click.get_width(), github.get_width(), loading.get_width(), tmtaw.get_width(), help.get_width(), lhelp.get_width(), ihelp.get_width(), usure.get_width(), usure2.get_width(), usure3.get_width()).get_width()
    clock.tick(fps)
    display.update()
