#Geo Node Cages can be accessed from the pc_types module.
from pc_lib import pc_types, pc_unit

#Create a class that inherits from the GeoNodeCage class
class My_Cage(pc_types.GeoNodeCage):

    def draw(self):
        self.create("My Cage")

        self.add_prompt('Material Thickness','DISTANCE',pc_unit.inch(.75))

        dim_x = self.get_dim_x_var("dim_x")
        dim_y = self.get_dim_x_var("dim_y")
        dim_z = self.get_dim_x_var("dim_z")
        mt = self.get_prompt("Material Thickness").get_var('mt')

        my_cutpart = self.add_geo_node_cutpart("My Cutpart") 
        my_cutpart.dim_x("dim_x",[dim_x])
        my_cutpart.dim_y("dim_y",[dim_y])
        my_cutpart.dim_z("mt",[mt])