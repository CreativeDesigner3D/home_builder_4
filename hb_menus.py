import bpy
from pc_lib import pc_utils

class HOME_BUILDER_MT_wall_commands(bpy.types.Menu):
    bl_label = "Wall Commands"

    def draw(self, context):
        wall_bp = pc_utils.get_bp_by_tag(context.object,'IS_WALL_BP')
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator('home_builder.wall_prompts',text="Wall Prompts",icon='WINDOW')
        layout.separator()
        layout.operator('home_builder.edit_part',text="Edit Wall Shape",icon='EDITMODE_HLT')
        layout.operator('home_builder.add_wall_length_dimension',text="Add Wall Length Dimension",icon='DRIVER_DISTANCE').wall_bp_name = wall_bp.name
        layout.operator('home_builder.select_room_base_point',text="Select Room Base Point",icon='EMPTY_DATA').wall_bp_name = wall_bp.name
        layout.operator('home_builder.delete_wall',text="Delete Wall",icon='X').wall_obj_bp_name = wall_bp.name


class HOME_BUILDER_MT_dimension_commands(bpy.types.Menu):
    bl_label = "Dimension Commands"

    def draw(self, context):
        wall_bp = pc_utils.get_bp_by_tag(context.object,'IS_WALL_BP')
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator('pc_layout_view.show_dimension_properties',text="Dimension Prompts",icon='WINDOW')
        layout.separator()
        layout.operator('object.delete',text="Delete Dimension",icon='X')


def draw_home_builder(self,context):
    layout = self.layout
    layout.menu('HOME_BUILDER_MT_home_builder_menu')

def register():
    bpy.utils.register_class(HOME_BUILDER_MT_wall_commands)
    bpy.utils.register_class(HOME_BUILDER_MT_dimension_commands)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_home_builder)

def unregister():    
    bpy.utils.unregister_class(HOME_BUILDER_MT_wall_commands)
    bpy.utils.unregister_class(HOME_BUILDER_MT_dimension_commands)
    bpy.types.VIEW3D_MT_edit_mesh.remove(draw_home_builder)