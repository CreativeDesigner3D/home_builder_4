import bpy
import os
from pc_lib import pc_unit
from . import hb_utils
import math
from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        UIList,
        AddonPreferences,
        )
from bpy.props import (
        BoolProperty,
        FloatProperty,
        FloatVectorProperty,
        IntProperty,
        PointerProperty,
        StringProperty,
        CollectionProperty,
        EnumProperty,
        )

def update_library_tab(self,context):
    prefs = context.preferences
    asset_lib = prefs.filepaths.asset_libraries.get('home_builder_library')
    library = hb_utils.get_active_library(context)
    if library:
        asset_lib.path = library.library_path

        for workspace in bpy.data.workspaces:
            workspace.asset_library_reference = "home_builder_library"
        
        if bpy.ops.asset.library_refresh.poll():
            bpy.ops.asset.library_refresh()

        #TODO FIGURE OUT HOW TO FIX WHEN INDEX IS GREATER THAN LENGTH
        # workspace = context.workspace.home_builder
        # wm_props = context.window_manager.home_builder
        # print('INDEX',workspace.home_builder_library_index,'LENGTH',len(wm_props.home_builder_library_assets))
        # if workspace.home_builder_library_index > len(wm_props.home_builder_library_assets):
        #     print("INDEX GREATER THAN LENGTH")

def update_wall_index(self,context):
    bpy.ops.object.select_all(action='DESELECT')
    wall = self.walls[self.wall_index]
    wall.wall_mesh.select_set(True)


class Material_Pointer(PropertyGroup):
    library_path: StringProperty(name="Library Path")
    library_name: StringProperty(name="Library Name")
    category_name: StringProperty(name="Category Name")
    material_name: StringProperty(name="Material Name")
    is_custom: BoolProperty(name="Is Custom",default=False)


class Asset_Library(PropertyGroup):
    library_type: StringProperty(name="Library Type")
    library_path: StringProperty(name="Library Path")
    library_menu_ui: StringProperty(name="Library Settings UI")
    activate_id: StringProperty(name="Activate ID")
    drop_id: StringProperty(name="Drop ID")
    enabled: BoolProperty(name="Enabled",default=True)
    is_external_library: BoolProperty(name="Is External Library",default=False)


class Wall(PropertyGroup):
    wall_mesh: PointerProperty(name="Wall Mesh",
                               type=bpy.types.Object,
                               description="This is the wall mesh.")

    obj_bp: PointerProperty(name="Wall Base Point",
                            type=bpy.types.Object,
                            description="This is the wall base point.")


class Library_Package(PropertyGroup):
    enabled: BoolProperty(name="Enabled",default=True)
    expand: BoolProperty(name="Expand",default=False)
    package_path: bpy.props.StringProperty(name="Package Path",subtype='DIR_PATH')
    asset_libraries: bpy.props.CollectionProperty(type=Asset_Library)


class Home_Builder_Object_Props(PropertyGroup):

    connected_object: bpy.props.PointerProperty(name="Connected Object",
                                                type=bpy.types.Object,
                                                description="This is the used to store objects that are connected together.")

    @classmethod
    def register(cls):
        bpy.types.Object.home_builder = PointerProperty(
            name="Home Builder Props",
            description="Home Builder Props",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.Object.home_builder

class Home_Builder_Scene_Props(PropertyGroup):  
    main_tabs: EnumProperty(name="Main Tabs",
                          items=[('LIBRARY',"Library","Show the Library"),
                                 ('SETTINGS',"Settings","Show the Library Settings")],
                          default='LIBRARY')

    library_tabs: EnumProperty(name="Library Tabs",
                          items=[('ROOMS',"Rooms","Show the Room Library"),
                                 ('PRODUCTS',"Products","Show the Product Library"),
                                 ('BUILD',"Build","Show the Build Library"),
                                 ('DECORATIONS',"Decorations","Show the Decoration Library"),
                                 ('MATERIALS',"Materials","Show the Materials")],
                          default='ROOMS',
                          update=update_library_tab)

    room_tabs: EnumProperty(name="Room Tabs",
                          items=[('WALLS',"Walls","Show the Walls"),
                                 ('CURRENT_ROOM',"Current Room","Show the Current Room Options"),
                                 ('OBSTACLES',"Obstacles","Show the Obstacles")],
                          default='WALLS',
                          update=update_library_tab)

    build_tabs: EnumProperty(name="Build Tabs",
                          items=[('STARTERS',"Starters","Show the Closet Starters"),
                                 ('INSERTS',"Inserts","Show the Closet Inserts"),
                                 ('PARTS',"Parts","Show the Closet Parts"),
                                 ('LIBRARY',"Library","Show the User Library")],
                          default='STARTERS',
                          update=update_library_tab)

    material_pointers: CollectionProperty(name="Material Pointers",type=Material_Pointer)

    walls: bpy.props.CollectionProperty(name="Walls",type=Wall)
    wall_index: bpy.props.IntProperty(name="Wall Index",update=update_wall_index)  

    wall_height: FloatProperty(name="Wall Height",default=pc_unit.inch(96),subtype='DISTANCE')
    wall_thickness: FloatProperty(name="Wall Thickness",default=pc_unit.inch(6),subtype='DISTANCE')

    wall_distance_snap_value: FloatProperty(name="Wall Distance Snap Value",default=pc_unit.inch(1),subtype='DISTANCE')
    wall_angle_snap_value: FloatProperty(name="Wall Angle Snap Value",default=math.radians(15),subtype='ANGLE')

    is_elevation_view: BoolProperty(name="Is Elevation View",default=False)
    view_rotation: FloatVectorProperty(name="View Rotation",size=4)
    view_location: FloatVectorProperty(name="View Location",size=3)
    view_distance: FloatProperty(name="View Distance")
    view_perspective: EnumProperty(name="View Perspective",
                                   items=[('PERSP',"Perspective","Perspective"),
                                          ('ORTHO',"Orthographic","Orthographic"),
                                          ('CAMERA',"Camera","Camera")])
    
    @classmethod
    def register(cls):
        bpy.types.Scene.home_builder = PointerProperty(
            name="Home Builder Props",
            description="Home Builder Props",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.Scene.home_builder    


class Home_Builder_Workspace_Props(PropertyGroup):  
    home_builder_library_index: bpy.props.IntProperty()

    @classmethod
    def register(cls):
        bpy.types.WorkSpace.home_builder = PointerProperty(
            name="Home Builder Props",
            description="Home Builder Props",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.WorkSpace.home_builder    


class Home_Builder_Window_Manager_Props(PropertyGroup):
    home_builder_library_assets: bpy.props.CollectionProperty(
        type=bpy.types.AssetHandle,
        description="Current Set of Assets In Asset Browser")

    asset_libraries: bpy.props.CollectionProperty(
        type=Asset_Library,
        description="Collection of all asset libraries loaded into Home Builder")

    library_packages: bpy.props.CollectionProperty(
        type=Library_Package,
        description="Collection of all external asset packages loaded into Home Builder")

    show_built_in_asset_libraries: bpy.props.BoolProperty(
        name="Show Built In Asset Libraries",
        description="UI toggle to display the build in asset libraries",
        default=False)

    active_product_library_name: bpy.props.StringProperty(name="Active Product Library Name")
    active_build_library_name: bpy.props.StringProperty(name="Active Build Library Name")
    active_starter_library_name: bpy.props.StringProperty(name="Active Closet Starter Library Name")
    active_insert_library_name: bpy.props.StringProperty(name="Active Closet Insert Library Name")
    active_part_library_name: bpy.props.StringProperty(name="Active Closet Part Library Name")
    active_decorations_library_name: bpy.props.StringProperty(name="Active Decorations Library Name")
    active_materials_library_name: bpy.props.StringProperty(name="Active Materials Library Name")

    def load_asset_libraries(self):
        print("LOADING ASSET LIBRARIES")

    def get_active_library(self,context):
        return hb_utils.get_active_library(context)

    def get_active_asset(self,context):
        workspace = context.workspace.home_builder
        return self.home_builder_library_assets[workspace.home_builder_library_index]

    @classmethod
    def register(cls):
        bpy.types.WindowManager.home_builder = PointerProperty(
            name="Home Builder Props",
            description="Home Builder Props",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.WindowManager.home_builder            


classes = (
    Material_Pointer,
    Wall,
    Asset_Library,
    Library_Package,
    Home_Builder_Object_Props,
    Home_Builder_Scene_Props,
    Home_Builder_Workspace_Props,
    Home_Builder_Window_Manager_Props,
)

register, unregister = bpy.utils.register_classes_factory(classes)             