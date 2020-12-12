import time

from mesh_voxel_color import image_processing_pil
from mesh_voxel_color import slice_geometry
from mesh_voxel_color import util

ip = image_processing_pil.ImageProcessingPIL()
sg = slice_geometry.SliceGeometry()
ut = util.Util()


################################################################################


# prj_name = "bunny_light"
# stl_name = "bunny-flatfoot_fixed_light.stl"

prj_name = "bunny"
stl_name = "bunny-flatfoot_fixed.stl"

# prj_name = "ship"
# stl_name = "3DBenchy_fixed.stl"


### WINDOWS 10
dir_path = "C:\\Users\\ysoky\\Documents\\Mesh_Voxel_Color\\"
prj_path = dir_path + "_prj_\\" + prj_name + "\\"
stl_path = dir_path + "_stl_\\bunny-flatfoot_fixed_light.stl"
stl_path = dir_path + "_stl_\\" + stl_name


### Resolution : 300 DPI
### Size : mm

_INCH = 25.4
_LAYER_HEIGHT = 0.027

INCH_AMP = 2.0
VOLUME_SIZE = _INCH * INCH_AMP
CANVAS_SIZE = int(300 * INCH_AMP)
LAYER_COUNT = int(VOLUME_SIZE / _LAYER_HEIGHT)


################################################################################


time_0 = time.time()


### Prepare Project Foloder
ut.prepare_prj_dir(dir_path, prj_name)

### Parse STL
meshes, ranges = sg.get_meshes_and_ranges(stl_path)

for i in range(LAYER_COUNT):

    h = i * _LAYER_HEIGHT

    ### Calc Contour
    lines = sg.contour_meshes(meshes, ranges, h)
    
    ### Draw Contour + Save inaage
    ip.draw_contours(prj_path, CANVAS_SIZE, VOLUME_SIZE, i, lines)


time_1 = time.time()


################################################################################

print("Time_01 : {}Sec".format(time_1 - time_0))