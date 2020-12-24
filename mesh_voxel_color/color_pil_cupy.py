import sys
sys.path.append("C:\\Users\\ysoky\\Documents\\Mesh_Voxel_Color\\_module_\\Mesh_Contour")


import math
import cupy as cp
import random
from PIL import Image, ImageDraw, ImageOps, ImageEnhance


from mesh_contour import stl_parser
sp = stl_parser.StlParser()


from .import util
ut = util.Util()


class ColorPILCupy():


    ############################
    ####                     ###
    ####     I/O + Basics    ###
    ####                     ###
    ############################


    def remap_number_cp(self, arr, old_min, old_max, target_min, target_max):

        new_arr = (arr - old_min) / (old_max - old_min) * (target_max - target_min) + target_min

        return new_arr


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


    ########################################


    def get_points_from_stl(self, file_path):
        
        ### Point From STL
        pts = sp.stl2points(file_path)

        return pts


    def get_points_from_stl_np(self, file_path, volume_size, canvas_size):
    
        ### Cupy
        
        ### Point From STL
        pts = sp.stl2points(file_path)
        pts_format = [pts]
        # print(pts_format)

        pts_cp = cp.array(pts_format)

        pts_cp_remap = self.remap_number_cp(pts_cp, 0, volume_size, 0, canvas_size)

        # print(pts_cp)

        return pts_cp_remap


    def clac_all_distance(self, pos, pts):

        ### Calc Cupy

        ### Generate Vector
        v = pos - pts
        # print("v.shape :", v.shape)
        # print(v)

        vt = v.T

        ### Calc Distance
        d = cp.sqrt((vt[0] * vt[0]) + (vt[1] * vt[1]) + (vt[2] * vt[2]))
        # print("d.shape :", d.shape)

        ### Select Min Value
        dm_cp = cp.amin(d, axis=0)
        # print("dm.shape :", dm_cp.shape)

        return dm_cp


    def gen_disctance_list(self, w, h, height, pts_cp):

        ### Generate Distance-List
        # print("Distance")

        px_list = []
        for i in range(w):
            for j in range(h):
                px_list.append([[j, i, height]])
        
        ### pos-numpy array (from Image)
        pos_cp = cp.array(px_list)
        # print("pos.shape :", pos_cp.shape)

        ### Separate Process
        ### https://qiita.com/kazuki_hayakawa/items/557edd922f9f1fafafe0

        SPLIT = 500
        pos_cp_split = cp.array_split(pos_cp, SPLIT)
        # print(len(pos_cp_split))

        dist_tmp = []

        for i in range(SPLIT):

            tmp_p = pos_cp_split[i]
            # print("pts.shape :", tmp_p.shape)

            ### pts-numpy array (from STL)
            # print("pts.shape :", pts_cp.shape)

            ### 
            d = self.clac_all_distance(tmp_p, pts_cp)
            dist_tmp.append(d)

        dist_list = cp.concatenate(dist_tmp, 0)
        # print(len(dist_list))

        return dist_list


    ########################################


    #####################
    ####              ###
    ####     Draw     ###
    ####              ###
    #####################


    def scan_image_calc_color(self, file_path, height, pts_cp):

        ### Open Image
        img = self.open_image(file_path)

        w, h = img.size
        img_result = self.create_canvas_alpha(w)

        px = img.getdata()
        px_length = len(px)
        
        px_cp = cp.array(px)
        px_seg_0 = cp.amax(px_cp)

        # print("px.shape :", px_cp.shape)
        # print("px_seg_0 :", px_seg_0)


        ### Running on Cuda
        # print("Running on Cuda !!")

        ### Contour : True
        if px_seg_0 > 127:
            ### Distance
            dist_list = self.gen_disctance_list(w, h, height, pts_cp)




            ### Generate Color From Distance
            # print("Color")

            dist_min = cp.amin(dist_list)
            dist_max = cp.amax(dist_list)

            dist = dist_list.tolist()


            # dist_remap = self.remap_number_cp(dist_list, 0, 600, 0, 150)
            # dist = dist_remap.tolist()


            # print(type(dist_remap))
            # print(type(dist))

            px_result = []
            
            for j in range(px_length):
                
                rr, gg, bb = px[j]
                d = dist_list[j]

                black = (0, 0, 0, 255)
                white = (255, 255, 255, 255)
                red = (255, 0, 0, 255)
                green = (0, 255, 0, 255)
                blue = (0, 0, 255, 255)



                ### White (Inside)
                if rr > 127:
                    
                    th_0 = 20
                    th_1 = 40
                    th_2 = 60
                    th_3 = 80



                    
                    if d < th_0:
                        px_result.append(red)

                    elif d < th_1:
                        px_result.append(green)

                    elif d < th_2:
                        px_result.append(blue)

                    elif d < th_3:
                        px_result.append(white)

                    else:
                        px_result.append(black)

                ### Outside
                else:
                    c = (0, 0, 0, 0)
                    px_result.append(c)
                    
            # ### Generate New Image
            img_result.putdata(tuple(px_result))

            return img_result



        ### Contour : False
        else:
            px_result = [(0, 0, 0, 0) for i in range(w) for j in range(h)]
            img_result.putdata(tuple(px_result))

            return img_result