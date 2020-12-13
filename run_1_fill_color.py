import time

from mesh_voxel_color import image_processing_cv2
from mesh_voxel_color import util

ic = image_processing_cv2.ImageProcessingCV2()
ut = util.Util()


################################################################################


# prj_name = "bunny_light"

# prj_name = "bunny"

prj_name = "ship"



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


################################################################################


time_0 = time.time()


### Prepare Project Foloder
ut.prepare_prj_dir(dir_path, prj_name)


for i in range(LAYER_COUNT):

    ### Format
    index = "%04d"%(int(i))

    line_ = line_path + "image_{}.jpg".format(index)
    fill_ = fill_path + "image_{}.jpg".format(index)


    if i == 420:
        # ic.create_image(CANVAS_SIZE)

        image_line = ic.open_image(line_)
        polylines = ic.find_hierarchy(image_line)


time_1 = time.time()


################################################################################

print("Time_01 : {}Sec".format(time_1 - time_0))