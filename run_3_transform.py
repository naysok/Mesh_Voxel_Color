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

clrs_path = prj_path + "image_2" + "\\"
affn_path = prj_path + "image_3" + "\\"


### Resolution : 300 DPI
### Size : mm

_INCH = 25.4
_LAYER_HEIGHT = 0.027

INCH_AMP = 2.0
VOLUME_SIZE = _INCH * INCH_AMP
CANVAS_SIZE = int(300 * INCH_AMP)
LAYER_COUNT = int(VOLUME_SIZE / _LAYER_HEIGHT)

IMAGE_SIZE = (800, 800)

ROT_UNIT = 90
ROT_COUNT = 2
### rotate = ROT_UNIT * ROT_COUNT

################################################################################


time_0 = time.time()


### Prepare Project Foloder
ut.prepare_prj_dir(dir_path, prj_name)


################################


### Affine Transform

### Define Matrix for Render
mat_aff = dc.define_matrix_for_render(IMAGE_SIZE)
# print("Matrix_Render :", mat_aff)


for i in range(LAYER_COUNT):

    ### Format
    index = "%04d"%(int(i))

    src_ = clrs_path + "image_{}.png".format(index)
    aff_ = affn_path + "image_{}.png".format(index)

    # if i == 420:
    if i >= 0:
        
        ### Open
        img = dc.open_image(src_)

        ### (1) Rotation
        img_rot = dc.rotate_image(img, ROT_UNIT * ROT_COUNT)
        # img_rot.show()
        
        ### (2) Affine Transform
        img_eddited = dc.run_transform(img_rot, IMAGE_SIZE, mat_aff)

        # img_eddited.show()
        dc.export_image(img_eddited, aff_)


time_1 = time.time()


################################################################################

print("Total : {}Sec".format(time_1 - time_0))
# print("Process : {}Sec".format(time_01 - time_00))
