


units_database={
    "soldier1":{
        "img_path": "img/units/soldier1/soldier.png",
        "oryginal_handle_xy": (26, 34),
        "oryginal_size_xy": (64, 64),
        "oryginal_hitbox_size_xy":(20,45),
        "atsp":200,
        "hp":100,
        "dmg":10,
        "speed":2
    }
}

items_database={
    "sword1":{
        "left":{
            "img_path":"img/weapon/sword1_left.png",
            "oryginal_handle_xy":(42,49),
            "oryginal_size_xy":(64,64)
        },
        "right":{
            "img_path":"img/weapon/sword1_right.png",
            "oryginal_handle_xy":(21,48),
            "oryginal_size_xy":(64,64)
        },
        "attack_range": 15

    }

}


animation_sprites={}
animation_sprites["soldier2"] = {
'IDLE_': {
'path': "img/units/soldier2/medival_knight_walk_south.png",
'frame_window_width':64,
'frame_window_height':64,
'animation_orientation':"horizontal",
'border':1,
'anim_fps':6,
'start_x':0,
'start_y':0,
'frames_count':1,
'img_per_row_or_col':6,
'color_key':(0,0,0),
"oryginal_handle_xy": [(26, 34)]
},
'IDLE_RIGHT': {
'path': "img/units/soldier2/medival_knight_walk_east.png",
'frame_window_width':64,
'frame_window_height':64,
'animation_orientation':"horizontal",
'border':1,
'anim_fps':6,
'start_x':0,
'start_y':0,
'frames_count':1,
'img_per_row_or_col':6,
'color_key':(0,0,0),
"oryginal_handle_xy": [(26, 34)]
},
'IDLE_LEFT': {
'path': "img/units/soldier2/medival_knight_walk_west.png",
'frame_window_width':64,
'frame_window_height':64,
'animation_orientation':"horizontal",
'border':1,
'anim_fps':6,
'start_x':0,
'start_y':0,
'frames_count':1,
'img_per_row_or_col':6,
'color_key':(0,0,0),
"oryginal_handle_xy": [(26, 34)]
},
'IDLE_UP': {
'path': "img/units/soldier2/medival_knight_walk_north.png",
'frame_window_width':64,
'frame_window_height':64,
'animation_orientation':"horizontal",
'border':1,
'anim_fps':6,
'start_x':0,
'start_y':0,
'frames_count':1,
'img_per_row_or_col':6,
'color_key':(0,0,0),
"oryginal_handle_xy": [(26, 34)]
},
'IDLE_DOWN': {
'path': "img/units/soldier2/medival_knight_walk_south.png",
'frame_window_width':64,
'frame_window_height':64,
'animation_orientation':"horizontal",
'border':1,
'anim_fps':6,
'start_x':0,
'start_y':0,
'frames_count':1,
'img_per_row_or_col':6,
'color_key':(0,0,0),
"oryginal_handle_xy": [(26, 34)]
},
'WALK_UP': {
    'path': "img/units/soldier2/medival_knight_walk_north.png",
    'frame_window_width': 64,
    'frame_window_height': 64,
    'animation_orientation': "horizontal",
    'border': 1,
    'anim_fps': 6,
    'start_x': 0,
    'start_y': 0,
    'frames_count': 6,
    'img_per_row_or_col': 6,
    'color_key': (0, 0, 0),
    "oryginal_handle_xy": [(40, 34),(40, 31),(40, 31),(40, 36),(40, 36),(40, 36)]
},'WALK_DOWN': {
    'path': "img/units/soldier2/medival_knight_walk_south.png",
    'frame_window_width': 64,
    'frame_window_height': 64,
    'animation_orientation': "horizontal",
    'border': 1,
    'anim_fps': 6,
    'start_x': 0,
    'start_y': 0,
    'frames_count': 6,
    'img_per_row_or_col': 6,
    'color_key': (0, 0, 0),
    "oryginal_handle_xy": [(26, 33),(26, 35),(26, 35),(26, 35),(25, 31),(25, 31)]
},'WALK_LEFT': {
    'path': "img/units/soldier2/medival_knight_walk_west.png",
    'frame_window_width': 64,
    'frame_window_height': 64,
    'animation_orientation': "horizontal",
    'border': 1,
    'anim_fps': 6,
    'start_x': 0,
    'start_y': 0,
    'frames_count': 6,
    'img_per_row_or_col': 6,
    'color_key': (0, 0, 0),
    "oryginal_handle_xy": [(32, 36),(30, 35),(31, 34),(33, 32),(34, 34),(34, 34)]
},'WALK_RIGHT': {
    'path': "img/units/soldier2/medival_knight_walk_east.png",
    'frame_window_width': 64,
    'frame_window_height': 64,
    'animation_orientation': "horizontal",
    'border': 1,
    'anim_fps': 6,
    'start_x': 0,
    'start_y': 0,
    'frames_count': 6,
    'img_per_row_or_col': 6,
    'color_key': (0, 0, 0),
    "oryginal_handle_xy": [(31, 38),(27, 39),(27, 39),(31, 38),(37, 37),(36, 37)]
},
    'ATTACK_UP': {
        'path': "img/units/soldier2/medival_knight_cross-punch_north.png",
        'frame_window_width': 64,
        'frame_window_height': 64,
        'animation_orientation': "horizontal",
        'border': 1,
        'anim_fps': 6,
        'start_x': 0,
        'start_y': 0,
        'frames_count': 6,
        "fire_at_frame":4,
        'img_per_row_or_col': 6,
        'color_key': (0, 0, 0),
        "oryginal_handle_xy": [(39,30), (40,34), (40,25), (34,20), (39,27), (39,31)],
        "weapon_rotation":[0,0,-45,0,0,0]
    }, 'ATTACK_DOWN': {
        'path': "img/units/soldier2/medival_knight_cross-punch_south.png",
        'frame_window_width': 64,
        'frame_window_height': 64,
        'animation_orientation': "horizontal",
        'border': 1,
        'anim_fps': 6,
        'start_x': 0,
        'start_y': 0,
        'frames_count': 6,
        "fire_at_frame": 4,
        'img_per_row_or_col': 6,
        'color_key': (0, 0, 0),
        "oryginal_handle_xy": [(24,28), (25,27), (24,26), (29,39), (27,33), (25,29)],
        "weapon_rotation":[0,0,90,180,90,0]
    }, 'ATTACK_LEFT': {
        'path': "img/units/soldier2/medival_knight_cross-punch_west.png",
        'frame_window_width': 64,
        'frame_window_height': 64,
        'animation_orientation': "horizontal",
        'border': 1,
        'anim_fps': 6,
        'start_x': 0,
        'start_y': 0,
        'frames_count': 6,
        "fire_at_frame": 4,
        'img_per_row_or_col': 6,
        'color_key': (0, 0, 0),
        "oryginal_handle_xy": [(28,28), (32,28), (36,28), (16,30), (22,27), (27,34)],
        "weapon_rotation":[0,0,0,45,0,0]
    }, 'ATTACK_RIGHT': {
        'path': "img/units/soldier2/medival_knight_cross-punch_east.png",
        'frame_window_width': 64,
        'frame_window_height': 64,
        'animation_orientation': "horizontal",
        'border': 1,
        'anim_fps': 6,
        'start_x': 0,
        'start_y': 0,
        'frames_count': 6,
        "fire_at_frame": 4,
        'img_per_row_or_col': 6,
        'color_key': (0, 0, 0),
        "oryginal_handle_xy": [(30,35), (26,35), (24,35), (47,32), (39,32), (28,36)],
        "weapon_rotation":[0,0,0,-45,0,0]
    }
}
