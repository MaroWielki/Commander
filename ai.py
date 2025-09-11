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
    return "asd"

def movemendAI(unit, enemies_group: pygame.sprite.Group, teammates_group: pygame.sprite.Group, database):

    enemy = find_closest_enemy(unit, enemies_group)

    ret=enemy

    #for dir in ["LEFT", "RIGHT", "UP", "DOWN"]:
    #    if unit.db["collided_with_dict"][dir] == enemy.uuid:
    #        ret=None

    if ret is not None:

        #print(unit.id,ret.id, unit.db["collided_with_dict"])
        if ret.id  in get_all_coliding_units(unit.db["collided_with_dict"]):
            ret =None
    return ret

def attackAI(unit, enemies_group: pygame.sprite.Group,database):

    enemies_in_range_dict=find_enemies_in_range(unit, enemies_group)
    ret=None
    for dir in ["LEFT", "RIGHT", "UP", "DOWN"]:
        if enemies_in_range_dict[dir] is not None:
            ret=dir

    return ret

def find_enemies_in_range(unit, enemies_group:pygame.sprite.Group):
    enemies_in_range = {}
    att_range=unit.weapon.sprites()[0].db["attack_range"]
    attack_hit_box = pygame.rect.Rect(0, 0, att_range, att_range)
    attack_hit_box.center = unit.hit_box_rect.center
    for dir in ["LEFT", "RIGHT", "UP", "DOWN"]:
        if dir =="LEFT":
            unit.attack_hit_box[dir]=attack_hit_box.move(-floor(unit.hit_box_rect.width/2)-floor(att_range/2),0)
        if dir =="RIGHT":
            unit.attack_hit_box[dir]=attack_hit_box.move(floor(unit.hit_box_rect.width/2)+floor(att_range/2),0)
        if dir =="UP":
            unit.attack_hit_box[dir]=attack_hit_box.move(0,-floor(unit.hit_box_rect.height/2)-floor(att_range/2))
        if dir =="DOWN":
            unit.attack_hit_box[dir]=attack_hit_box.move(0,+floor(unit.hit_box_rect.height/2)+floor(att_range/2))

    enemies_in_range_dict={"LEFT":None,"RIGHT":None,"UP":None,"DOWN":None}

    for dir in ["LEFT", "RIGHT", "UP", "DOWN"]:
        col = unit.attack_hit_box[dir].collidelist([i.hit_box_rect for i in  enemies_group.sprites()])
        if col !=-1:
            enemies_in_range_dict[dir]=enemies_group.sprites()[col].id

    return enemies_in_range_dict

def get_all_coliding_units(col:dict):
    ret=[]
    for dir in ["LEFT", "RIGHT", "UP", "DOWN"]:
        ret+=col[dir]
    return ret