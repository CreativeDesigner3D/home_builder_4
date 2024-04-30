import bpy
import os
from pc_lib import pc_utils, pc_types

class MACHINE_TOKENS_MT_add_machine_token(bpy.types.Menu):
    bl_label = "Add Machine Token"

    def draw(self, context):
        layout = self.layout
        path = pc_utils.get_machine_tokens_path()
        tokens = os.listdir(path)
        for token_file in tokens:
            filename, ext = os.path.splitext(token_file)
            if ext == '.blend':
                layout.operator('machine_tokens.add_machine_token',text=filename).token_type = filename


class machine_tokens_OT_add_machine_token(bpy.types.Operator):
    bl_idname = "machine_tokens.add_machine_token"
    bl_label = "Add Machine Token"

    token_type: bpy.props.StringProperty(name="Token Type")

    token_name: bpy.props.StringProperty(name="Token Name",default="Token Name")

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self,'token_name')

    def execute(self, context):
        obj = context.object
        machine_token = pc_types.MachineToken(obj)
        machine_token.add_token(self.token_type,self.token_name)
        return {'FINISHED'}

class machine_tokens_OT_remove_machine_token(bpy.types.Operator):
    bl_idname = "machine_tokens.remove_machine_token"
    bl_label = "Remove Machine Token"

    modifier_name: bpy.props.StringProperty(name="Modifer Name")

    def execute(self, context):
        obj = context.object
        
        for mod in obj.modifiers:
            if mod.name == self.modifier_name:
                obj.modifiers.remove(mod)
                break
        
        return {'FINISHED'}
    

classes = (
    MACHINE_TOKENS_MT_add_machine_token,
    machine_tokens_OT_add_machine_token,
    machine_tokens_OT_remove_machine_token,
)

register, unregister = bpy.utils.register_classes_factory(classes)             