import time

from mesh_voxel_color import color_pil
from mesh_voxel_color import util

cl = color_pil.ColorPIL()
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
stl_path = dir_path + "_stl_\\" + stl_name

fill_path = prj_path + "\\image_1\\"
clrs_path = prj_path + "\\image_2\\"


### Resolution : 300 DPI
### Size : mm

_INCH = 25.4
_LAYER_HEIGHT = 0.027

INCH_AMP = 2.0
VOLUME_SIZE = _INCH * INCH_AMP
CANVAS_SIZE = int(300 * INCH_AMP)
LAYER_COUNT = int(VOLUME_SIZE / _LAYER_HEIGHT)


### 
target_path = stl_path


################################################################################


time_0 = time.time()


### Prepare Project Foloder
ut.prepare_prj_dir(dir_path, prj_name)

### Get Points
# pts = cl.get_points_from_stl(target_path)
### Get Points (numpy-array)
pts_np = cl.get_points_from_stl_np(target_path)


# print(len(pts))
# print(pts[0])


for i in range(LAYER_COUNT):

    ### Format
    index = "%04d"%(int(i))

    fill_ = fill_path + "image_{}.jpg".format(index)
    clrs_ = clrs_path + "image_{}.jpg".format(index)

    height = LAYER_COUNT * i

    # if i == 72:
    if i == 420:
        image_clrs = cl.scan_image_calc_color(fill_, height, pts_np)
        # image_clrs.show()


time_1 = time.time()


################################################################################

print("Time_01 : {}Sec".format(time_1 - time_0))