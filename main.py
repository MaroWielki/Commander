import sys


import pygame
from pygame import K_ESCAPE, K_LEFT, K_RIGHT, KSCAN_UP, K_DOWN, K_SPACE

from my_utils import *

from data import *
from database import *

pygame.init()

pygame.font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 15)

MyRealFPS = RealFPS(50)
screen=pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
last_update_time = pygame.time.get_ticks()

database["units_teamA"]=pygame.sprite.Group()
database["units_teamB"]=pygame.sprite.Group()

#database["units_teamA"].add(Unit(200,300,"teamA",units_database["soldier1"],database,move_algorithm="movementAI",attack_algorithm="attackAI",id="AAA"))
database["units_teamA"].add(Unit(200,300,"teamA",units_database["soldier1"],database,move_algorithm="movementAI_Graph",attack_algorithm="attackAI",id="AAA"))
database["units_teamA"].add(Unit(400,300,"teamA",units_database["soldier1"],database,id="AAAA"))
database["units_teamB"].add(Unit(600,300,"teamB",units_database["soldier1"],database,move_algorithm="movemendAI_B",id="BBB"))
#database["units_teamB"].add(Unit(600,310,"teamB",units_database["soldier1"],database,id="BBB"))


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
    #debug=False
    debug=True
    if debug==True:
        for u in database["units_teamA"].sprites():
            pygame.draw.rect(screen,"white",u.hit_box_rect,1)
        for u in database["units_teamB"].sprites():
            pygame.draw.rect(screen,"white",u.hit_box_rect,1)

        # for u in database["units_teamA"].sprites():
        #     for dir in database["possible_directions_8"]:
        #         if u.attack_hit_box[dir] is not None:
        #             pygame.draw.rect(screen,"white",u.attack_hit_box[dir],1)

        for x in database["units_teamA"].sprites()[0].graph_verts:
            pygame.draw.rect(screen,"yellow",x[0],1)

        for x in database["units_teamA"].sprites()[0].debug_lines:
            pygame.draw.line(screen,"yellow",x[0],x[1])
        pygame.draw.circle(screen,"red",database["units_teamA"].sprites()[0].move_target,5)




        text_surface = my_font.render(str(pygame.mouse.get_pos()), False, "white")

        screen.blit(text_surface,(0,0))

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
