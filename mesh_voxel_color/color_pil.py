import sys
sys.path.append("C:\\Users\\ysoky\\Documents\\Mesh_Voxel_Color\\_module_\\Mesh_Contour")


import math
from PIL import Image, ImageDraw, ImageOps, ImageEnhance


from mesh_contour import stl_parser
sp = stl_parser.StlParser()


from .import util
ut = util.Util()


class ColorPIL():


    ############################
    ####                     ###
    ####     I/O + Basics    ###
    ####                     ###
    ############################


    def open_image(self, path):
        img = Image.open(path)
        return img


    def export_image(self, img, path):
        img.save(path, quality=100)
        print("Export : {}".format(path))


    def create_canvas(self, canvas_size):
        new = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
        return new


    def get_points_from_stl(self, file_path):
        
        ### Point From STL
        pts = sp.stl2points(file_path)
        return pts