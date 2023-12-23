import bpy
from pc_lib import pc_types, pc_utils, pc_unit

def add_wall(location,length,height,thickness):
    '''
    create the wall and return the mesh object in blender for this particular wall
    '''

    wall = pc_types.Wall()
    wall.draw_wall(length,height,thickness)
    wall.obj_bp.location = location
    return wall

def assign_wall_texture(wall_obj,texture_id):
    pass

def assign_floor_texture(floor_obj,texture_id):
    pass

def create_window(wall,location,size,window_id):
    '''
    create a window on the given wall object
    the wall object that the window should be on, the window position and size, and window_id refers to a particular window style (assuming windows are parametric models)   
    '''
    bool_clearance = .01
    window = pc_types.GeoNodeCage()
    window.create(window_id)
    window.obj.parent = wall.obj_bp
    window.obj.location.x = location[0]
    window.obj.location.z = location[1]
    window.obj.location.y = -bool_clearance
    window.set_input("Dim X",size[0])
    window.set_input("Dim Y",wall.obj_y.location.y+bool_clearance)
    window.set_input("Dim Z",size[1])
    
    wall_mesh = None
    for child in wall.obj_bp.children:
        if 'IS_WALL_MESH' in child:
            wall_mesh = child

    mod = wall_mesh.modifiers.new(window_id,'BOOLEAN')
    mod.object = window.obj
    mod.operation = 'DIFFERENCE'

def create_door(wall,location,size,door_id):
    '''
    create a window on the given wall object
    the wall object that the window should be on, the window position and size, and window_id refers 
    to a particular window style (assuming windows are parametric models)   
    '''
    bool_clearance = .01
    door = pc_types.GeoNodeCage()
    door.create(door_id)
    door.obj.parent = wall.obj_bp
    door.obj.location.x = location
    door.obj.location.z = -bool_clearance
    door.obj.location.y = -bool_clearance
    door.set_input("Dim X",size[0])
    door.set_input("Dim Y",wall.obj_y.location.y+bool_clearance)
    door.set_input("Dim Z",size[1] + bool_clearance)
    
    wall_mesh = None
    for child in wall.obj_bp.children:
        if 'IS_WALL_MESH' in child:
            wall_mesh = child

    mod = wall_mesh.modifiers.new(door_id,'BOOLEAN')
    mod.object = door.obj
    mod.operation = 'DIFFERENCE'

wall = add_wall((0,0,0),pc_unit.inch(120),pc_unit.inch(96),pc_unit.inch(6))
create_window(wall,location=(pc_unit.inch(10),pc_unit.inch(42)),size=(pc_unit.inch(24),pc_unit.inch(24)),window_id='Standard Window')
create_door(wall,location=pc_unit.inch(50),size=(pc_unit.inch(36),pc_unit.inch(86)),door_id='Standard Door')