


units_database={
    "soldier1":{
        "img_path": "img/units/soldier1/soldier.png",
        "oryginal_handle_xy": (26, 34),
        "oryginal_size_xy": (64, 64)
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
        }
    }

}


animation_sprites={}
animation_sprites["soldier2"] = {
'IDLE': {
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
    "oryginal_handle_xy": [(34, 36),(29, 32),(29, 35),(34, 36),(29, 37),(29, 38)]
}}
