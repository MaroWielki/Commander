from os import spawnl
import igraph as ig

import pygame
from data import *
from math import floor
import uuid
from ai import *
from copy import deepcopy

class RealFPS:
    def __init__(self,span):
        self.queue=[]
        self.span=span
    def add(self,item):

        if len(self.queue)<self.span:
            self.queue.append(item)
        else:
            self.queue.pop(0)
            self.queue.append(item)
    def get(self):

        return sum(self.queue) / len(self.queue)


def rotate_pivot( original_image, origin, pivot, angle):

    image_rect = original_image.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center

    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)

    rotozoom_image = pygame.transform.rotate(original_image, angle)
    rect = rotozoom_image.get_rect(center = rotated_image_center)

    return rotozoom_image,rect

def cropp_img(path,frame_window_width,frame_window_height,border,start_x,start_y,frames_count,img_per_row_or_col,animation_orientation,color_key,px_scale_to_xy=None,init_rotation=0):
    pieces = []
    img = pygame.image.load(path).convert_alpha()
    frame_index=0
    while frame_index<frames_count:
        if animation_orientation=="horizontal":
            row_index=floor(frame_index/img_per_row_or_col)
            col_index=int(frame_index%img_per_row_or_col)
        if animation_orientation=="vertical":
            col_index = floor(frame_index / img_per_row_or_col)
            row_index = int(frame_index % img_per_row_or_col)
        frame_x = col_index * frame_window_width +border + start_x
        frame_y = row_index * frame_window_height + border + start_y
        if px_scale_to_xy is None:
            pieces.append(pygame.Surface.subsurface(img,frame_x,frame_y,frame_window_width-border,frame_window_height-border))
        else:
            #pieces.append(pygame.transform.scale(pygame.Surface.subsurface(img, frame_x, frame_y, frame_window_width - border,frame_window_height - border), px_scale_to_xy))

            pieces.append(pygame.transform.rotate(pygame.transform.scale(pygame.Surface.subsurface(img, frame_x, frame_y, frame_window_width - border,frame_window_height - border),px_scale_to_xy),init_rotation))


        frame_index+=1
    return pieces

class AnimationSingle:
    def __init__(self,name,kw):
        self.name = name
        self.path = kw['path']
        self.frame_window_width = kw['frame_window_width']
        self.frame_window_height = kw['frame_window_height']
        self.animation_orientation = kw['animation_orientation']
        self.border = kw['border']
        self.anim_fps = kw['anim_fps']
        self.start_x = kw['start_x']
        self.start_y = kw['start_y']
        if "fire_at_frame" in kw.keys():
            self.fire_at_frame=kw['fire_at_frame']
        if "init_rotation" in kw.keys():
            self.init_rotation = kw['init_rotation']
        else:
            self.init_rotation = 0
        self.frames_count = kw['frames_count']
        self.img_per_row_or_col = kw['img_per_row_or_col']
        self.color_key = kw['color_key']
        self.oryginal_handle_xy=kw["oryginal_handle_xy"]
        if "weapon_rotation" in kw.keys():
            self.weapon_rotation=kw["weapon_rotation"]
        else:
            self.weapon_rotation=[0]*self.frames_count



class AnimationData:
    def __init__(self,kw,sprite_name=None):
        self.animationdata={}
        self.name=sprite_name
        for key in kw:

            self.animationdata[key]=AnimationSingle(key,kw[key])







class Unit(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, team_name:str,unit_data:dict,database:dict,scale_down_factor=1,move_algorithm=None,attack_algorithm=None,id=None):
        pygame.sprite.Sprite.__init__(self)

        self.debug_lines=[]
        self.graph_verts=None
        self.id=id#str(uuid.uuid1())
        self.db = unit_data
        self.move_algorithm=move_algorithm
        self.attack_algorithm=attack_algorithm
        self.scale_down_factor=scale_down_factor
        self.direction=""
        self.to_be_removed=False
        self.action="IDLE"
        self.direction="DOWN"
        self.db["collided_with"]=[]
        self.weapon=pygame.sprite.Group()
        self.weapon.add(Item(self,items_database["sword1"]))

        self.x=x
        self.y=y
        self.blank=pygame.image.load("img/blank64x64.png").convert_alpha()
        self.fps_counter=0
        self.fps=database["fps"]

        self.animation_frames={}
        self.animation_name="IDLE_"

        self.data=AnimationData(animation_sprites["soldier2"],"soldier2")
        for anim_name in self.data.animationdata:
            anim_data=self.data.animationdata[anim_name]
            self.animation_frames[anim_name] = cropp_img(anim_data.path,anim_data.frame_window_width,anim_data.frame_window_height,anim_data.border,anim_data.start_x,anim_data.start_y,anim_data.frames_count,anim_data.img_per_row_or_col,anim_data.animation_orientation,anim_data.color_key)
        self.anim_fps =1


        self.db["size_xy"]=(floor(self.db["oryginal_size_xy"][0]/self.scale_down_factor),floor(self.db["oryginal_size_xy"][1]/self.scale_down_factor))


        self.db["handle_xy"]=(floor(self.db["oryginal_handle_xy"][0]/self.scale_down_factor),floor(self.db["oryginal_handle_xy"][1]/self.scale_down_factor))
        self.db["handle_xy"]=(floor(self.db["oryginal_handle_xy"][0]/self.scale_down_factor),floor(self.db["oryginal_handle_xy"][1]/self.scale_down_factor))

        self.image = self.animation_frames["IDLE_"][0]

        self.team_name=team_name
        self.atsp=self.db["atsp"]
        self.last_attack_frame_number=database["frame_counter"]
        self.init_hp=self.db["hp"]
        self.dmg=self.db["dmg"]
        self.hp=self.init_hp
        self.speed=self.db["speed"]
        self.database=database
        self.move_target=None
        self.hit_box_rect = pygame.rect.Rect(0,0,self.db["oryginal_hitbox_size_xy"][0],self.db["oryginal_hitbox_size_xy"][1])
        self.rect = pygame.rect.Rect(self.x, self.y, self.data.animationdata[self.animation_name].frame_window_width,
                                     self.data.animationdata[self.animation_name].frame_window_height)

        self.attack_hit_box={}
        self.attack_direction=None
        self.have_i_hit_this_anim = False


        for team in self.database["teams"]:
            if team is not self.team_name:
                self.enemy_team=team

        self.db["collided_with_dict"]=deepcopy(self.database["blank_directions"])

        self.rect.center=(self.x,self.y)
        self.hit_box_rect.center = self.rect.center



    def update(self):
        ### AI
        self.db["collided_with_dict"]=check_nearby_collisions(self,self.database["units_"+self.enemy_team].sprites()+self.database["units_"+self.team_name].sprites())

        if self.move_algorithm=="movemendAI":
            self.move_target=movemendAI(self,self.database["units_"+self.enemy_team],self.database["units_"+self.team_name],self.database)
        if self.move_algorithm=="movemendAI_B":
            self.move_target=movemendAI_B(self,self.database["units_"+self.enemy_team],self.database["units_"+self.team_name],self.database)

        if self.attack_algorithm=="attackAI":
            self.attack_direction = attackAI(self,self.database["units_"+self.enemy_team],self.database)



        #determin action

        self.action="IDLE"
        if self.move_target is not None:
            if type(self.move_target)==Unit:
                walk_dir=determin_walk_direction(self)
                if walk_dir is not None:
                    self.action="WALK"
                    self.direction=walk_dir
            else:
                self.action="WALK"

        if self.attack_direction is not None:
            self.action="ATTACK"
            self.direction=self.attack_direction

        if self.hp<1:
            self.action = "DEATH"


        self.move()


        if self.action+"_"+self.direction != self.animation_name :
            self.fps_counter=0   # Start new animation from frame 0
        self.animation_name=self.action+"_"+self.direction
        self.anim_fps=self.data.animationdata[self.animation_name].anim_fps

        ### ANIMATION
        self.fps_counter += 1
        if self.anim_fps != 0:

            self.animation_index = floor(self.fps_counter / (self.fps / self.anim_fps))
            if self.animation_index >= len(self.animation_frames[self.animation_name]):
                self.animation_index = 0
                self.fps_counter = 0
                self.have_i_hit_this_anim = False
                if self.action=="ATTACK":
                    print("tu")
                    self.action = "IDLE"
                if self.action=="DEATH":
                    self.to_be_removed=True

        ### ATTACK ANIMATION
        if self.action=="ATTACK":
            if self.animation_index == self.data.animationdata[self.animation_name].fire_at_frame and not self.have_i_hit_this_anim:
                self.have_i_hit_this_anim=True

                if self.attack_direction is not None:
                    perform_attack(self,self.database["units_"+self.enemy_team],self.database)
                    self.last_attack_frame_number=self.database["frame_counter"]



        img = self.animation_frames[self.animation_name][self.animation_index].copy()

        ### BLIT WEAPON
        self.weapon.update()
        self.image=self.blank.copy()

        if self.direction not in ["RIGHT","DOWN","RIGHTDOWN","LEFTDOWN"]:
            self.weapon.draw(self.image)

        self.image.blit(img,(0,0))

        if self.direction  in ["RIGHT","DOWN","RIGHTDOWN","LEFTDOWN"]:
            self.weapon.draw(self.image)

        ### LIFE BAR
        if self.team_name=="teamA":
            color="green"
        else:
            color="red"
        pygame.draw.rect(self.image, color, (0,0,self.rect.width*(self.hp/self.init_hp),2))




        ### DEBUG
        if self.id=="AAA":
            get_graph_vers(self,self.database)
            get_graph_edges(self,self.database)



        # pygame.draw.rect(self.image, "red", (0,0,self.rect.width,self.rect.height),1)
        # pygame.draw.rect(self.image, "red", (0, 0, self.hit_box_rect.width, self.hit_box_rect.height), 1)


    def move(self):


        if self.action=="WALK":
            new_xy=move_xy((self.rect.center),self.direction,self.speed)
            tmp_rect= self.hit_box_rect.copy()
            tmp_rect.center=new_xy
            all_units_list=self.database["units_"+self.enemy_team].sprites()+self.database["units_"+self.team_name].sprites()


            if tmp_rect.collidelist([i.hit_box_rect for i in all_units_list if i.id!=self.id]) ==-1:

                self.rect.center=new_xy
                self.hit_box_rect.center=new_xy







class Item(pygame.sprite.Sprite):
    def __init__(self,attached_to:Unit,item:dict,scale_down_factor=2.5):
        pygame.sprite.Sprite.__init__(self)

        self.id = str(uuid.uuid1())
        self.scale_down_factor=scale_down_factor
        self.attached_to = attached_to
        self.db=item
        self.pointing_direction="left"

        self.image_with_dir = {}
        img= pygame.image.load(self.db["left"]["img_path"]).convert_alpha()
        self.image_with_dir["left"] = pygame.transform.scale_by(img,1/self.scale_down_factor)
        img= pygame.image.load(self.db["right"]["img_path"]).convert_alpha()
        self.image_with_dir["right"] = pygame.transform.scale_by(img,1/self.scale_down_factor)

        self.image=self.image_with_dir[self.pointing_direction]

        self.db["size_xy"]=(floor(self.db[self.pointing_direction]["oryginal_size_xy"][0]/self.scale_down_factor),floor(self.db[self.pointing_direction]["oryginal_size_xy"][1]/self.scale_down_factor))

        self.db["handle_xy"]={}
        self.db["handle_xy"]["left"]=(floor(self.db["left"]["oryginal_handle_xy"][0]/self.scale_down_factor),floor(self.db["left"]["oryginal_handle_xy"][1]/self.scale_down_factor))
        self.db["handle_xy"]["right"]=(floor(self.db["right"]["oryginal_handle_xy"][0]/self.scale_down_factor),floor(self.db["right"]["oryginal_handle_xy"][1]/self.scale_down_factor))

        self.rect = self.image.get_rect()


    def update(self, *args, **kwargs):
        #self.rect.topleft=(self.attached_to.rect.x,self.attached_to.rect.y)
        if self.attached_to.direction in ["RIGHT","DOWN","RIGHTDOWN","LEFTDOWN"]:
            pointing_direction="right"
            img  = self.image_with_dir[pointing_direction]
        else:
            pointing_direction = "left"
            img =  self.image_with_dir[pointing_direction]



        attach_point_in_frame_xy=self.attached_to.data.animationdata[self.attached_to.animation_name].oryginal_handle_xy[self.attached_to.animation_index]
        rot_in_frame=self.attached_to.data.animationdata[self.attached_to.animation_name].weapon_rotation[self.attached_to.animation_index]



        self.image, self.rect = rotate_pivot(img, (attach_point_in_frame_xy[0],attach_point_in_frame_xy[1]),
                                     (self.db["handle_xy"][pointing_direction][0], self.db["handle_xy"][pointing_direction][1]), rot_in_frame)


def perform_attack(unit:Unit,enemies_group,database:dict):

    dir=unit.attack_direction
    col = unit.attack_hit_box[dir].collidelist([i.hit_box_rect for i in enemies_group.sprites()])

    enemies_group.sprites()[col].hp-=25

def check_nearby_collisions(unit:Unit,units_group):

    ret = deepcopy(unit.database["blank_directions"])
    for dir in unit.database["possible_directions"]:

        if dir =="LEFT":
            temp_hitbox=unit.hit_box_rect.move(-unit.speed,0)
        if dir =="RIGHT":
            temp_hitbox=unit.hit_box_rect.move(unit.speed,0)
        if dir =="UP":
            temp_hitbox=unit.hit_box_rect.move(0,-unit.speed)
        if dir =="DOWN":
            temp_hitbox=unit.hit_box_rect.move(0,unit.speed)

        hit=temp_hitbox.collidelist([i.hit_box_rect for i in units_group])
        if hit != -1:
            if unit.id != units_group[hit].id:

                ret[dir]+=[units_group[hit].id]




    return ret


def move_xy(xy:tuple,direction:str,speed:int):


    if direction=="LEFT":
        ret= xy[0]-speed,xy[1]
    if direction == "RIGHT":
        ret= xy[0] + speed, xy[1]
    if direction == "UP":
        ret= xy[0], xy[1]-speed
    if direction == "DOWN":
        ret= xy[0] , xy[1]+speed

    speed_diag=(speed/2)**(1/2)
    if direction=="LEFTUP":
        ret= xy[0]-speed_diag,xy[1]-speed_diag
    if direction == "LEFTDOWN":
        ret= xy[0] - speed_diag, xy[1]+speed_diag
    if direction == "RIGHTUP":
        ret= xy[0]+speed_diag, xy[1]-speed_diag
    if direction == "RIGHTDOWN":
        ret= xy[0]+speed_diag , xy[1]+speed_diag


    return ret

def determin_walk_direction(unit:Unit):
    start_xy=unit.rect.center
    target_xy=unit.move_target.rect.center
    ret=None
    if target_xy[0]<start_xy[0]: ret="LEFT"
    if target_xy[0]>start_xy[0] : ret = "RIGHT"
    if target_xy[1]<start_xy[1]: ret="UP"
    if target_xy[1]>start_xy[1] : ret = "DOWN"

    if target_xy[0]<start_xy[0] and target_xy[1]<start_xy[1] : ret="LEFTUP"
    if target_xy[0] < start_xy[0] and target_xy[1]>start_xy[1]: ret = "LEFTDOWN"
    if target_xy[0]>start_xy[0] and target_xy[1]<start_xy[1]: ret = "RIGHTUP"
    if target_xy[0]>start_xy[0] and target_xy[1]>start_xy[1]: ret = "RIGHTDOWN"


    return ret

def remove_units(database):
    for unit in database["units_teamA"]:
        if unit.to_be_removed == True:
            unit.remove(database["units_teamA"])
    for unit in database["units_teamB"]:
        if unit.to_be_removed == True:
            unit.remove(database["units_teamB"])


def get_all_objects_except(database:dict,exclude:Unit):
    ret=[]
    for unit in database["units_"+exclude.team_name].sprites()+database["units_"+exclude.enemy_team].sprites():
        if unit.id!=exclude.id:
            ret.append(unit)
    return ret

def get_graph_vers(unit,database):
    tmp_rects=[unit.hit_box_rect.copy()]
    other_objects=get_all_objects_except(database,exclude=unit)
    for other_unit in other_objects:

        tmp_rects.append(unit.hit_box_rect.copy())
        tmp=other_unit.hit_box_rect.topleft
        tmp_rects[-1].bottomright = (tmp[0]-1,tmp[1]-1)

        tmp_rects.append(unit.hit_box_rect.copy())
        tmp=other_unit.hit_box_rect.topright
        tmp_rects[-1].bottomleft = (tmp[0]+1,tmp[1]-1)

        tmp_rects.append(unit.hit_box_rect.copy())
        tmp=other_unit.hit_box_rect.bottomleft
        tmp_rects[-1].topright = (tmp[0]-1,tmp[1]+1)

        tmp_rects.append(unit.hit_box_rect.copy())
        tmp=other_unit.hit_box_rect.bottomright
        tmp_rects[-1].topleft = (tmp[0]+1,tmp[1]+1)

        unit.graph_verts=tmp_rects


    #return tmp_rects   # WYblituj to w mainie zobaczyc czy OK

def get_graph_edges(unit,database):
    all_objects=get_all_objects_except(database,exclude=unit)
    unit.debug_lines=[]
    starting_vert=unit.graph_verts[0]
    for vert_from in unit.graph_verts:
        for vert_to in unit.graph_verts:
            if vert_from != vert_to:
                line = (vert_from.center, vert_to.center)
                is_clear=True
                for obstacle in unit.graph_verts[1:]+[x.rect for x in all_objects]:

                    #unit.debug_lines.append(line)
                    if obstacle.clipline(line)!=() and obstacle not in [vert_to,vert_from]:
                        is_clear=False
                if is_clear: unit.debug_lines.append(line)

