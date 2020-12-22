import sys
sys.path.append("C:\\Users\\ysoky\\Documents\\Mesh_Voxel_Color\\_module_\\Mesh_Contour")


import math
import numpy as np
import random
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


    def create_canvas_alpha(self, canvas_size):
        new = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        return new


    def get_points_from_stl(self, file_path):
        
        ### Point From STL
        pts = sp.stl2points(file_path)
        return pts


    def calc_distance_min(self, pos, pts):

        pos_n = np.array(pos)
        pts_n = np.array(pts)

        v = pts_n - pos_n
        vt = v.T
        
        d = np.sqrt((vt[0] * vt[0]) + (vt[1] * vt[1]) + (vt[2] * vt[2]))
        d_min = np.min(d)

        return d_min


    ########################################


    #####################
    ####              ###
    ####     Draw     ###
    ####              ###
    #####################


    def scan_image_calc_color(self, file_path, height, pts):

        ### Open Image
        img = self.open_image(file_path)

        w, h = img.size
        result_img = self.create_canvas_alpha(w)

        px = img.getdata()
        px_length = len(px)

        ### Generate Distance-List

        print("Distance")

        dist = []

        for i in range(px_length):

            print(i)

            rr, gg, bb = px[i]

            ### Process
            ### Calc Distance
            if rr > 127:

                u, v = divmod(px_length, i)
                d = self.calc_distance_min([u, v, height], pts)
                dist.append(d)
            
            ### None
            else:
                dist.append(0)

        ### Generate Color From Distance
        
        print("Color")

        result_px = []

        d_min = min(dist)
        d_max = max(dist)

        th = 100

        for j in range(px_length):
            d = dist[j]
            
            ### Outside
            if d == 0:
                result_px.append((0, 0, 0, 0))

            elif d > th:
                result_px.append((255, 255, 255, 255))

            else:
                c = int(ut.remap_number(d, 0, 100, 0, 255))
                result_px.append((c, c, c, 255))


        # ### Generate New Image
        result_img.putdata(tuple(result_px))

        return result_img
