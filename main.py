import sys


import pygame
from pygame import K_ESCAPE, K_LEFT, K_RIGHT, KSCAN_UP, K_DOWN, K_SPACE

from my_utils import *

from data import *
from database import *

pygame.init()

MyRealFPS = RealFPS(50)
screen=pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
last_update_time = pygame.time.get_ticks()

database["units_teamA"]=pygame.sprite.Group()
database["units_teamB"]=pygame.sprite.Group()

database["units_teamA"].add(Unit(200,300,"teamA",units_database["soldier1"],database,move_algorithm="movemendAI",attack_algorithm="attackAI",id="AAA"))
database["units_teamA"].add(Unit(400,300,"teamA",units_database["soldier1"],database,id="AAAA"))
#database["units_teamB"].add(Unit(400,300,"teamB",units_database["soldier1"],database,move_algorithm="movemendAI_B",id="BBB"))
database["units_teamB"].add(Unit(600,310,"teamB",units_database["soldier1"],database,id="BBB"))


#
# for i in range(10):
#     database["units_teamA"].add(
#         Unit(i*50, 100, "teamA", units_database["soldier1"], database, move_algorithm="movemendAI",
#              attack_algorithm="attackAI", id=str(i)))


while True:
    screen.fill("black")


    database["units_teamA"].update()
    database["units_teamA"].draw(screen)

    database["units_teamB"].update()
    database["units_teamB"].draw(screen)


    remove_units(database)

    ###DEBUG
    debug=False
    #debug=True
    if debug==True:
        for u in database["units_teamA"].sprites():
            pygame.draw.rect(screen,"white",u.hit_box_rect,1)
        for u in database["units_teamB"].sprites():
            pygame.draw.rect(screen,"white",u.hit_box_rect,1)

        for u in database["units_teamA"].sprites():
            for dir in database["possible_directions_8"]:
                pygame.draw.rect(screen,"white",u.attack_hit_box[dir],1)



    pygame.display.update()
    clock.tick(60)
    database["frame_counter"]+=1


    #real_fps=pygame.time.get_ticks() - last_update_time
    MyRealFPS.add(pygame.time.get_ticks() - last_update_time)
    last_update_time = pygame.time.get_ticks()
    #print(MyRealFPS.get())
    pygame.display.set_caption(str(floor(1000/MyRealFPS.get())))

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
