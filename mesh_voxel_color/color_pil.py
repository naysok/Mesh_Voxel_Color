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


    def get_points_from_stl_np(self, file_path):
    
        ### Point From STL
        pts = sp.stl2points(file_path)
        pts_format = [pts]
        # print(pts_format)

        pts_np = np.array(pts_format)
        return pts_np


    def clac_all_distance(self, pos, pts):

        v = pos - pts
        # print("v.shape :", v.shape)

        vt = v.T

        d = np.sqrt((vt[0] * vt[0]) + (vt[1] * vt[1]) + (vt[2] * vt[2]))
        # print("d.shape :", d.shape)

        dm_np = np.amin(d, axis=0)
        # print("dm.shape :", dm_np.shape)

        return dm_np


    ########################################


    #####################
    ####              ###
    ####     Draw     ###
    ####              ###
    #####################


    def scan_image_calc_color(self, file_path, height, pts_np):

        ### Open Image
        img = self.open_image(file_path)

        w, h = img.size
        result_img = self.create_canvas_alpha(w)

        px = img.getdata()
        px_length = len(px)

        ### Running on Cuda
        print("Running on CPU !!")

        ### Generate Distance-List
        # print("Distance")
        
        px_list = []
        for i in range(w):
            for j in range(h):
                px_list.append([[i, j, height]])
        
        ### pos-numpy array (from Image)
        pos_np = np.array(px_list)
        # print("pos.shape :", pos_np.shape)

        ### Process
        ### https://qiita.com/kazuki_hayakawa/items/557edd922f9f1fafafe0
        
        SPLIT = 1000
        pos_np_split = np.array_split(pos_np, SPLIT)
        # print(len(pos_np_split))

        dist_tmp = []

        for i in range(SPLIT):

            tmp_p = pos_np_split[i]
            # print("pts.shape :", tmp_p.shape)

            ### pts-numpy array (from STL)
            # print("pts.shape :", pts_np.shape)

            ### 
            d = self.clac_all_distance(tmp_p, pts_np)
            dist_tmp.append(d)

        dist_list = np.concatenate(dist_tmp, 0)
        print(len(dist_list))
        
        # return None


        # self.clac_all_distance(pos)

        """

        dist = []

        for i in range(px_length):

            if i%200 == 0:
                
                ############################################################
                # print(i)

                rr, gg, bb = px[i]

                ### Process
                ### Calc Distance
                if rr > 127:

                    if i == 0:
                        u, v = [0, 0]
                        d = self.calc_distance_min([u, v, height], pts)
                        dist.append(d)

                    else:
                        u, v = divmod(px_length, i)
                        d = self.calc_distance_min([u, v, height], pts)
                        dist.append(d)
                ############################################################
                
                ### None
                else:
                    dist.append(0)
                
            ### None (dev)
            else:
                dist.append(0)

        # print(dist)

        ### Generate Color From Distance
        
        print("Color")

        result_px = []

        d_min = min(dist)
        d_max = max(dist)

        th = 1000

        for j in range(px_length):
            d = dist[j]
            
            ### Outside
            if d == 0:
                result_px.append((0, 0, 0, 0))

            elif d > th:
                result_px.append((255, 0, 0, 255))

            else:
                c = int(ut.remap_number(d, 0, th, 0, 255))
                # result_px.append((0, c, 0, 255))
                result_px.append((0, 0, 255, 255))


        # ### Generate New Image
        result_img.putdata(tuple(result_px))

        return result_img

        """
