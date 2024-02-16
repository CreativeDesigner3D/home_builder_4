import bpy
from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        UIList,
        )
from bpy.props import (
        BoolProperty,
        FloatProperty,
        IntProperty,
        PointerProperty,
        StringProperty,
        CollectionProperty,
        )
import os
import subprocess
from .. import pyclone_utils
from .. import hb_utils
from pc_lib import pc_utils, pc_types

class TEXT_PT_python_crash_course(Panel):
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_category = "Documentation"
    bl_label = "Python Crash Course"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout    
        # layout.label(text="PyClone Examples")
        TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'docs','python_templates','Python Crash Course')
        layout.operator('text.open',text="Variables").filepath = os.path.join(TEMPLATE_PATH,"Variables.py")
        layout.operator('text.open',text="Arithmetic").filepath = os.path.join(TEMPLATE_PATH,"Arithmetic.py")

class TEXT_PT_pc_examples(Panel):
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_category = "Documentation"
    bl_label = "PyClone Examples"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout    
        # layout.label(text="PyClone Examples")
        TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'docs','python_templates','PyClone Examples')
        files = os.listdir(TEMPLATE_PATH)
        for f in files:
            file_name, ext = os.path.splitext(f)
            if '.py' in ext:
                layout.operator('text.open',text=file_name).filepath = os.path.join(TEMPLATE_PATH,f)        


class TEXT_PT_home_builder_libraries(Panel):
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_category = "Libraries"
    bl_label = "Home Builder Libraries"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        wm_props = context.window_manager
        library = hb_utils.get_active_library(context)
        library_root_folder = os.path.dirname(os.path.dirname(library.library_path))
        library_init_file = os.path.join(library_root_folder,"__init__.py")
        if library:
            layout.operator('pc_text.open_blend_file',text=library.name + " " + "Thumbnails").filepath = os.path.join(library.library_path,"library.blend")
            layout.operator('text.open',text=library.name).filepath = library_init_file
            files = os.listdir(library_root_folder)
            init_file_box = layout.box()
            operator_box = layout.box()
            operator_box.label(text="Operator Modules")
            data_box = layout.box()
            data_box.label(text="Data Modules")                
            property_box = layout.box()
            property_box.label(text="Property Modules")
            ui_box = layout.box()
            ui_box.label(text="UI Modules")            
            for f in files:
                file_name, ext = os.path.splitext(f)
                if ext == '.py':
                    if 'props_' in f:
                        property_box.operator('text.open',text=file_name).filepath = os.path.join(library_root_folder,f)                    
                    elif 'ops_' in f:
                        operator_box.operator('text.open',text=file_name).filepath = os.path.join(library_root_folder,f)
                    elif 'ui_' in f:
                        ui_box.operator('text.open',text=file_name).filepath = os.path.join(library_root_folder,f)
                    elif 'types_' in f:
                        data_box.operator('text.open',text=file_name).filepath = os.path.join(library_root_folder,f)
                    else:
                        layout.operator('text.open',text=file_name).filepath = os.path.join(library_root_folder,f)
                    

class pc_text_OT_open_blend_file(bpy.types.Operator):
    bl_idname = "pc_text.open_blend_file"
    bl_label = "Open Blend File"
    bl_description = "This exports the XML file for a room"

    filepath: bpy.props.StringProperty()

    def execute(self, context):
        command = [bpy.app.binary_path,self.filepath]
        subprocess.Popen(command)         
        return {'FINISHED'}
    
classes = (
    TEXT_PT_python_crash_course,
    TEXT_PT_pc_examples,
    TEXT_PT_home_builder_libraries,
    pc_text_OT_open_blend_file,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()                        