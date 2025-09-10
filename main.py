import sys

import pygame
from pygame import K_ESCAPE, K_LEFT, K_RIGHT, KSCAN_UP, K_DOWN, K_SPACE

from my_utils import *

from data import *
from database import *

pygame.init()

screen=pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
last_update_time = pygame.time.get_ticks()

database["units_teamA"]=pygame.sprite.Group()
database["units_teamB"]=pygame.sprite.Group()

database["units_teamA"].add(Unit(100,100,"teamA",units_database["soldier1"],database,move_algorithm="movemendAI",attack_algorithm="attackAI"))
database["units_teamB"].add(Unit(400,300,"teamB",units_database["soldier1"],database))



while True:
    screen.fill("black")


    database["units_teamA"].update()
    database["units_teamA"].draw(screen)

    database["units_teamB"].update()
    database["units_teamB"].draw(screen)


    ###DEBUG
    for u in database["units_teamA"].sprites():
        pygame.draw.rect(screen,"white",u.hit_box_rect,1)
    for u in database["units_teamB"].sprites():
        pygame.draw.rect(screen,"white",u.hit_box_rect,1)

    for u in database["units_teamA"].sprites():
        for dir in ["LEFT", "RIGHT", "UP", "DOWN"]:
            pygame.draw.rect(screen,"white",u.attack_hit_box[dir],1)


    pygame.display.update()
    clock.tick(60)
    database["frame_counter"]+=1
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
                database["units_teamB"].sprites()[0].direction = "LEFT"
                database["units_teamB"].sprites()[0].action = "WALK"
            if event.key == K_RIGHT:
                database["units_teamB"].sprites()[0].direction = "RIGHT"
                database["units_teamB"].sprites()[0].action = "WALK"
            if event.key == pygame.K_UP:
                database["units_teamB"].sprites()[0].direction = "UP"
                database["units_teamB"].sprites()[0].action = "WALK"
            if event.key == K_DOWN:
                database["units_teamB"].sprites()[0].direction = "DOWN"
                database["units_teamB"].sprites()[0].action = "WALK"
            if event.key==K_SPACE:
                database["units_teamB"].sprites()[0].action = "ATTACK"
