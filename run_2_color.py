import time

from mesh_voxel_color import color_pil
from mesh_voxel_color import color_pil_cupy
from mesh_voxel_color import util

# cl = color_pil.ColorPIL()
cl = color_pil_cupy.ColorPILCupy()
ut = util.Util()


################################################################################


prj_name = "bunny_light"
stl_name = "bunny-flatfoot_fixed_light.stl"

# prj_name = "bunny"
# stl_name = "bunny-flatfoot_fixed_upsampling.stl"
# stl_name = "bunny-flatfoot_fixed.stl"

# prj_name = "ship"
# stl_name = "3DBenchy_fixed.stl"



### WINDOWS 10
dir_path = "C:\\Users\\ysoky\\Documents\\Mesh_Voxel_Color\\"
prj_path = dir_path + "_prj_\\" + prj_name + "\\"
stl_path = dir_path + "_stl_\\" + stl_name

fill_path = prj_path + "image_1" + "\\"
clrs_path = prj_path + "image_2" + "\\"


### pts_path
pts_path = dir_path + "_pts_\\" + "bunny_10000.txt"


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


### [X] Get Points (numpy-array)
# pts_np = cl.get_points_from_stl_np(target_path, VOLUME_SIZE, CANVAS_SIZE)
# print("pts_np.shape :", pts_np.shape)

### Get Points (numpy-array)
pts_np = cl.get_points_from_txt_np(pts_path, VOLUME_SIZE, CANVAS_SIZE)
# print("pts_np.shape :", pts_np.shape)



for i in range(LAYER_COUNT):

    ### Format
    index = "%04d"%(int(i))

    fill_ = fill_path + "image_{}.jpg".format(index)
    clrs_ = clrs_path + "image_{}.png".format(index)

    height = (CANVAS_SIZE / LAYER_COUNT) * i
    # print(height)

    # if i == :
    # if i > 140:
    if i == 430:

        time_00 = time.time()

        image_clrs = cl.scan_image_calc_color(fill_, height, pts_np)
        cl.export_image(image_clrs, clrs_)
        # image_clrs.show()

        time_01 = time.time()


time_1 = time.time()


################################################################################

print("Total : {}Sec".format(time_1 - time_0))
print("Process : {}Sec".format(time_01 - time_00))
