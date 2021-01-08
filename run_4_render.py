import time

from mesh_voxel_color import draw_contour
from mesh_voxel_color import util

dc = draw_contour.DrawContour()
ut = util.Util()


################################################################################


# prj_name = "bunny_light"

prj_name = "bunny"

# prj_name = "ship"


### WINDOWS 10
dir_path = "C:\\Users\\ysoky\\Documents\\Mesh_Voxel_Color\\"
prj_path = dir_path + "_prj_\\" + prj_name + "\\"

affn_path = prj_path + "image_3" + "\\"
rend_path = prj_path + "image_4" + "\\"

### Resolution : 300 DPI
### Size : mm

_INCH = 25.4
_LAYER_HEIGHT = 0.027

INCH_AMP = 2.0
VOLUME_SIZE = _INCH * INCH_AMP
CANVAS_SIZE = int(300 * INCH_AMP)
LAYER_COUNT = int(VOLUME_SIZE / _LAYER_HEIGHT)

IMAGE_SIZE = (800, 800)
RENDER_SIZE = 1000


################################################################################


time_0 = time.time()


### Prepare Project Foloder
ut.prepare_prj_dir(dir_path, prj_name)


### Render

### Get File Count
count = ut.get_file_count(affn_path)

for i in range(count):

    ### Format
    index = "%04d"%(int(i))
    index_before = "%04d"%(int(i - 1))

    aff_ = affn_path + "image_{}.png".format(index)
    ren_ = rend_path + "image_{}.png".format(index)
    ren_before = rend_path + "image_{}.png".format(index_before)

    if i >= 0:
        img_render = dc.run_render(aff_, ren_before, count, i, RENDER_SIZE)
        dc.export_image(img_render, ren_)

time_1 = time.time()


################################################################################

print("Total : {}Sec".format(time_1 - time_0))
# print("Process : {}Sec".format(time_01 - time_00))
