from copy import deepcopy

import pygame
from math import floor

def find_closest_enemy(unit, enemies_group: pygame.sprite.Group):
    closest_enemy = None
    closest_enemy_distance = 9999
    my_position_v2 = pygame.math.Vector2(unit.x, unit.y)
    for enemy in enemies_group.sprites():

        distance = my_position_v2.distance_to((enemy.x, enemy.y))
        if distance < closest_enemy_distance:
            closest_enemy_distance = distance
            closest_enemy = enemy


    return closest_enemy

def movemendAI_B(unit, enemies_group: pygame.sprite.Group, teammates_group: pygame.sprite.Group, database):
    ret=None
    if unit.action=="WALK":
        ret = unit.direction

    if ret is not None and unit.action == "WALK":
        #print(unit.direction,unit.db["collided_with_dict"])
        if unit.db["collided_with_dict"][unit.direction] !=[]:
            ret =None
    return ret

def movemendAI(unit, enemies_group: pygame.sprite.Group, teammates_group: pygame.sprite.Group, database):

    enemy = find_closest_enemy(unit, enemies_group)

    ret=enemy

    #for dir in ["LEFT", "RIGHT", "UP", "DOWN"]:
    #    if unit.db["collided_with_dict"][dir] == enemy.uuid:
    #        ret=None

    if ret is not None:

        #print(unit.id,ret.id, unit.db["collided_with_dict"])
        if ret.id  in get_all_coliding_units(unit.db["collided_with_dict"],database):
            ret =None
    return ret

def attackAI(unit, enemies_group: pygame.sprite.Group,database):

    enemies_in_range_dict=find_enemies_in_range(unit, enemies_group,database)

    ret=None

    for dir in list(reversed(database["possible_directions_8"])):
        if enemies_in_range_dict[dir] !=[]:
            ret=dir

    return ret

def find_enemies_in_range(unit, enemies_group:pygame.sprite.Group,database):
    enemies_in_range = {}
    att_range=unit.weapon.sprites()[0].db["attack_range"]

    attack_hit_box_side = pygame.rect.Rect(0, 0, att_range, 5)
    attack_hit_box_side.center = unit.hit_box_rect.center
    attack_hit_box_updown = pygame.rect.Rect(0, 0, 5, att_range)
    attack_hit_box_updown.center = unit.hit_box_rect.center

    tmp=att_range/(2**(1/2))


    attack_hit_box_diagonal = pygame.rect.Rect(0, 0, tmp, tmp)
    attack_hit_box_diagonal.center = unit.hit_box_rect.center


    for dir in database["possible_directions_8"]:
        if dir =="LEFT":
            unit.attack_hit_box[dir]=attack_hit_box_side.move(-floor(unit.hit_box_rect.width/2)-floor(att_range/2),0)
        if dir =="RIGHT":
            unit.attack_hit_box[dir]=attack_hit_box_side.move(floor(unit.hit_box_rect.width/2)+floor(att_range/2),0)
        if dir =="UP":
            unit.attack_hit_box[dir]=attack_hit_box_updown.move(0,-floor(unit.hit_box_rect.height/2)-floor(att_range/2))
        if dir =="DOWN":
            unit.attack_hit_box[dir]=attack_hit_box_updown.move(0,+floor(unit.hit_box_rect.height/2)+floor(att_range/2))


        if dir =="LEFTUP":
            unit.attack_hit_box[dir]=attack_hit_box_diagonal.move(-(unit.hit_box_rect.width/2)-(tmp/2),-(unit.hit_box_rect.height/2)-(tmp/2))
        if dir =="RIGHTUP":
            unit.attack_hit_box[dir]=attack_hit_box_diagonal.move((unit.hit_box_rect.width/2)+(tmp/2),-(unit.hit_box_rect.height/2)-(tmp/2))
        if dir =="LEFTDOWN":
            unit.attack_hit_box[dir]=attack_hit_box_diagonal.move(-(unit.hit_box_rect.width/2)-(tmp/2),(unit.hit_box_rect.height/2)+(tmp/2))
        if dir =="RIGHTDOWN":
            unit.attack_hit_box[dir]=attack_hit_box_diagonal.move((unit.hit_box_rect.width/2)+(tmp/2),(unit.hit_box_rect.height/2)+(tmp/2))


    #enemies_in_range_dict={"LEFT":None,"RIGHT":None,"UP":None,"DOWN":None}
    enemies_in_range_dict=deepcopy(database["blank_directions_8"])
    for dir in database["possible_directions_8"]:
        col = unit.attack_hit_box[dir].collidelist([i.hit_box_rect for i in  enemies_group.sprites()])
        if col !=-1:
            enemies_in_range_dict[dir]+=[enemies_group.sprites()[col].id]


    return enemies_in_range_dict

def get_all_coliding_units(col:dict,database):
    ret=[]
    for dir in database["possible_directions"]:
        ret+=col[dir]
    return ret