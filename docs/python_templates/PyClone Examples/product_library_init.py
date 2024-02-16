#IMPORT MODULES AND LIBRARIES
import os

#PATH TO BLEND WITH THUMBNAILS
LIBRARY_PATH = os.path.join(os.path.dirname(__file__),'library',"MY Library")

#SET LIBRARY PROPERTIES
MY_LIBRARY = {"library_name": "My Library",
              "library_type": "PRODUCTS",
              "library_path": LIBRARY_PATH,
              "library_menu_id": "HOME_BUILDER_MT_closet_library_menu",
              "library_activate_id": "hb_sample_cabinets.active_cabinet_library",
              "libary_drop_id": "pro_closet.drop_closet"}

#VAR FOR REGISTERING WITH LIBRARY
LIBRARIES = [MY_LIBRARY]

#REGISTER MODULES WITH BLENDER
def register():
    pass