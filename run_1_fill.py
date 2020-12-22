import time

from mesh_voxel_color import contour_cv2
from mesh_voxel_color import util

cc = contour_cv2.ContourCV2()
ut = util.Util()


################################################################################


# prj_name = "bunny_light"
# stl_name = "bunny-flatfoot_fixed_light.stl"

# prj_name = "bunny"
# stl_name = "bunny-flatfoot_fixed.stl"

prj_name = "ship"
stl_name = "3DBenchy_fixed.stl"



### WINDOWS 10
dir_path = "C:\\Users\\ysoky\\Documents\\Mesh_Voxel_Color\\"
prj_path = dir_path + "_prj_\\" + prj_name + "\\"

line_path = prj_path + "\\image_0\\"
fill_path = prj_path + "\\image_1\\"


### Resolution : 300 DPI
### Size : mm

_INCH = 25.4
_LAYER_HEIGHT = 0.027

INCH_AMP = 2.0
VOLUME_SIZE = _INCH * INCH_AMP
CANVAS_SIZE = int(300 * INCH_AMP)
LAYER_COUNT = int(VOLUME_SIZE / _LAYER_HEIGHT)

UP_SAMPLING_XY = 2


################################################################################


time_0 = time.time()


### Prepare Project Foloder
ut.prepare_prj_dir(dir_path, prj_name)


for i in range(LAYER_COUNT):

    ### Format
    index = "%04d"%(int(i))

    line_ = line_path + "image_{}.jpg".format(index)
    fill_ = fill_path + "image_{}.jpg".format(index)

    ##3 Process
    image_line = cc.open_image(line_)
    image_fill = cc.find_draw_hierarchy(image_line, UP_SAMPLING_XY)
    cc.export_image(image_fill, fill_)


time_1 = time.time()


################################################################################

print("Time_01 : {}Sec".format(time_1 - time_0))