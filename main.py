import sys

import pygame
from pygame import K_ESCAPE, K_LEFT, K_RIGHT, KSCAN_UP, K_DOWN, K_SPACE
from utils import *
from data import *

pygame.init()

screen=pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
last_update_time = pygame.time.get_ticks()

units=pygame.sprite.Group()

units.add(Unit(100,100,"teamA",units_database["soldier1"]))
#units.add(Unit(400,300,"teamB",units_database["soldier1"]))

while True:
    screen.fill("black")

    units.update()
    units.draw(screen)


    pygame.display.update()
    clock.tick(60)
    real_fps=pygame.time.get_ticks() - last_update_time
    last_update_time = pygame.time.get_ticks()
    pygame.display.set_caption(str(floor(1000/real_fps)))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == K_LEFT:
                units.sprites()[0].direction = "LEFT"
            if event.key == K_RIGHT:
                units.sprites()[0].direction = "RIGHT"
            if event.key == pygame.K_UP:
                units.sprites()[0].direction = "UP"
            if event.key == K_DOWN:
                units.sprites()[0].direction = "DOWN"
            if event.key==K_SPACE:
                units.sprites()[0].action = "ATTACK"
