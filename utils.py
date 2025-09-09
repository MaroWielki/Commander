
import pygame
from data import *
from math import floor


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
    def __init__(self, x:int, y:int, team_name:str,unit_data:dict,scale_down_factor=1):
        pygame.sprite.Sprite.__init__(self)

        self.db = unit_data
        self.scale_down_factor=scale_down_factor
        self.direction=""
        self.action="IDLE"

        self.weapon=pygame.sprite.Group()
        self.weapon.add(Item(self,items_database["sword1"]))


        self.x=x
        self.y=y
        self.blank=pygame.image.load("img/blank64x64.png").convert_alpha()
        self.fps_counter=0
        self.fps=60
        self.animation_frames={}
        self.animation_name="IDLE"

        self.data=AnimationData(animation_sprites["soldier2"],"soldier2")
        for anim_name in self.data.animationdata:
            anim_data=self.data.animationdata[anim_name]
            self.animation_frames[anim_name] = cropp_img(anim_data.path,anim_data.frame_window_width,anim_data.frame_window_height,anim_data.border,anim_data.start_x,anim_data.start_y,anim_data.frames_count,anim_data.img_per_row_or_col,anim_data.animation_orientation,anim_data.color_key)
        self.anim_fps =8


        self.db["size_xy"]=(floor(self.db["oryginal_size_xy"][0]/self.scale_down_factor),floor(self.db["oryginal_size_xy"][1]/self.scale_down_factor))


        self.db["handle_xy"]=(floor(self.db["oryginal_handle_xy"][0]/self.scale_down_factor),floor(self.db["oryginal_handle_xy"][1]/self.scale_down_factor))
        self.db["handle_xy"]=(floor(self.db["oryginal_handle_xy"][0]/self.scale_down_factor),floor(self.db["oryginal_handle_xy"][1]/self.scale_down_factor))

        self.image = self.animation_frames["IDLE_"][0]

        self.team_name=team_name
        self.hp=100
        self.init_hp=100
        self.speed=2



    def update(self):



        self.move()
        self.fps_counter += 1
        if self.anim_fps != 0:
            self.animation_index = floor(self.fps_counter / (self.fps / self.anim_fps))
            if self.animation_index >= len(self.animation_frames[self.animation_name]):
                self.animation_index = 0
                self.fps_counter = 0



        #self.image = self.animation_frames[self.animation_name][self.animation_index].copy()
        img = self.animation_frames[self.animation_name][self.animation_index].copy()
        self.rect = pygame.rect.Rect(self.x, self.y, self.data.animationdata[self.animation_name].frame_window_width,
                                     self.data.animationdata[self.animation_name].frame_window_height)


        self.weapon.update()

        #self.weapon.draw(self.image)

        self.image=self.blank.copy()

        if self.direction not in ["RIGHT","DOWN"]:
            self.weapon.draw(self.image)

        self.image.blit(img,(0,0))

        if self.direction  in ["RIGHT","DOWN"]:
            self.weapon.draw(self.image)


        if self.team_name=="teamA":
            color="green"
        else:
            color="red"
        pygame.draw.rect(self.image, color, (0,0,self.rect.width*(self.hp/self.init_hp),2))




    def move(self):
        self.animation_name = self.action+"_"+self.direction


        if self.action+"_"+self.direction == "WALK_RIGHT":
            self.x+=self.speed
        if self.action+"_"+self.direction == "WALK_LEFT":
            self.x-=self.speed
        if self.action+"_"+self.direction == "WALK_UP":
            self.y-=self.speed
        if self.action+"_"+self.direction == "WALK_DOWN":
            self.y+=self.speed

class Item(pygame.sprite.Sprite):
    def __init__(self,attached_to:Unit,item:dict,scale_down_factor=2.5):
        pygame.sprite.Sprite.__init__(self)

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
        if self.attached_to.direction in ["RIGHT","DOWN"]:
            pointing_direction="right"
            img  = self.image_with_dir[pointing_direction]
        else:
            pointing_direction = "left"
            img =  self.image_with_dir[pointing_direction]



        attach_point_in_frame_xy=self.attached_to.data.animationdata[self.attached_to.animation_name].oryginal_handle_xy[self.attached_to.animation_index]
        rot_in_frame=self.attached_to.data.animationdata[self.attached_to.animation_name].weapon_rotation[self.attached_to.animation_index]

        #img, img_rect = rotate_pivot(img,(self.attached_to.x+self.db["handle_xy"][pointing_direction][0],self.attached_to.y+self.db["handle_xy"][pointing_direction][1]),attach_point_in_frame_xy,20)

        #print(self.db["handle_xy"][pointing_direction][0],self.db["handle_xy"][pointing_direction][1])
        #img, img_rect = rotate_pivot(img, (attach_point_in_frame_xy[0]-self.db["handle_xy"][pointing_direction][0],attach_point_in_frame_xy[1]-self.db["handle_xy"][pointing_direction][1]),(attach_point_in_frame_xy[0],attach_point_in_frame_xy[1]), 20)



        img, img_rect = rotate_pivot(img, (attach_point_in_frame_xy[0],attach_point_in_frame_xy[1]),
                                     (self.db["handle_xy"][pointing_direction][0], self.db["handle_xy"][pointing_direction][1]), rot_in_frame)

        #self.rect.topleft = (attach_point_in_frame_xy[0]-self.db["handle_xy"][pointing_direction][0],attach_point_in_frame_xy[1]-self.db["handle_xy"][pointing_direction][1])

        self.rect=img_rect

        #print(self.rect)

        self.image=img


