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


    ###############################
    ####                        ###
    ####     I/O + Utilities    ###
    ####                        ###
    ###############################


    def remap_number_cp(self, arr, old_min, old_max, target_min, target_max):

        new_arr = (arr - old_min) / (old_max - old_min) * (target_max - target_min) + target_min

        return new_arr


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


    def get_points_from_txt_np(self, file_path, volume_size, canvas_size):
        
        ### Cupy

        with open(file_path) as f:
            lines = f.readlines()

        xyz_list = []

        for line in lines:
            elm = line.split(",")
            xyz =[float(elm[0]), float(elm[1]), float(elm[2])]
            xyz_list.append(xyz)

        xyz_list = [xyz_list]

        pts_cp = cp.array(xyz_list)

        pts_cp_remap = self.remap_number_cp(pts_cp, 0, volume_size, 0, canvas_size)

        # print("pts_cp_remap.shape :", pts_np_remap.shape)
        # print(pts_cp_remap)

        return pts_cp_remap


    ################################################################################


    ######################################
    ####                               ###
    ####     Image Processing (PIL)    ###
    ####                               ###
    ######################################


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


    ################################################################################


    ###########################
    ####                    ###
    ####     Math (Cupy)    ###
    ####                    ###
    ###########################


    def clac_all_distance(self, pos, pts):

        ### Calc Distance with Cupy

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

        SPLIT = 250
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


    def gen_disctance_list_ds(self, w, h, height, downsampling_xy, pts_cp):

        ### Generate Distance-List
        ### with DownSampling

        # print("Distance")

        px_list = []
        for i in range(w):
            for j in range(h):
                px = [j * downsampling_xy, i * downsampling_xy, height]
                px_list.append([px])
        
        ### pos-numpy array (from Image)
        pos_cp = cp.array(px_list)
        # print(pos_cp)
        # print("pos.shape :", pos_cp.shape)

        ### Separate Process
        ### https://qiita.com/kazuki_hayakawa/items/557edd922f9f1fafafe0

        SPLIT = 250
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


    ################################################################################


    ####################
    ###              ###
    ###     Draw     ###
    ###              ###
    ####################


    def scan_image_calc_color(self, file_path, height, pts_cp, downsampling_xy):

        ### Open Image
        img_src = self.open_image(file_path)
        
        w, h = img_src.size

        ### DownSampling
        ww = int(w / downsampling_xy)
        hh = int(h / downsampling_xy)
        img = img_src.resize((ww, hh), Image.LANCZOS)

        ### Read Shape
        px = img.getdata()
        px_cp = cp.array(px)
        # print("px_cp.shape :", px_cp.shape)

        ### Create Result Canvas
        img_tmp = self.create_canvas_alpha(ww)
        img_result = self.create_canvas_alpha(w)

        ### Segment Contour True/False
        px_seg_0 = cp.amax(px_cp)


        ### Contour : False
        if px_seg_0 < 127:
            ### Export None-Image
            px_result = [(0, 0, 0, 0) for i in range(w) for j in range(h)]
            img_result.putdata(tuple(px_result))
            return img_result


        ### Contour : True
        else:

            ### Running on Cuda
            # print("Running on Cuda !!")


            ################################################################################################


            ###########################
            ###                     ###
            ###    Calc Distance    ###
            ###                     ###
            ###########################

            # print("Distance")

            ### [X] Clac Distance
            # dist_list = self.gen_disctance_list(w, h, height, pts_cp)
            
            ### [O] Clac Distance with DownSampling
            dist_list = self.gen_disctance_list_ds(ww, hh, height, downsampling_xy, pts_cp)


            ################################################################################################


            ############################################
            ###                                      ###
            ###     Generate Color From Distance     ###
            ###                                      ###
            ############################################
            
            # print("Color")

            ### Define Colors

            ################################################################################################

            ### Offset Pattern (Small)

            dist_src = dist_list.tolist()
            # print("len(dist_src) :", len(dist_src))

            clrs = []
            amp = 1 / 2

            for d in dist_src:

                c = int((math.sin(d * amp) + 1) * (1 / 2) * 255)
                cc = 255 - c

                clrs.append([c, c, cc, 255])
                
            clrs_tuple = tuple(map(tuple, clrs))
            
            ### Generate New Image
            img_tmp.putdata(tuple(clrs_tuple))

            ################################################################################################

            """
            ### Offset Pattern (Large)

            dist_src = dist_list.tolist()
            # print("len(dist_src) :", len(dist_src))

            clrs = []

            for d in dist_src:

                th = 30

                if d < (th * 1):
                    clrs.append([255, 0, 0, 255])
                
                elif d < (th * 2):
                    clrs.append([0, 255, 0, 255])

                elif d < (th * 3):
                    clrs.append([0, 0, 255, 255])
                
                else:
                    clrs.append([255, 255, 255, 255])

            clrs_tuple = tuple(map(tuple, clrs))
            
            ### Generate New Image
            img_tmp.putdata(tuple(clrs_tuple))
            """

            ################################################################################################

            """
            ### Test Distance Map

            dist_remap = self.remap_number_cp(dist_list, 0, 200, 0, 255)
            dist_remap = dist_remap.astype('int64')

            # print("dist_remap.shape :", dist_remap.shape)
            
            ### Fill Array (255)
            alpha_array = cp.ones(dist_list.shape) * 255
            alpha_array = alpha_array.astype('int64')


            dist_img = cp.stack([dist_remap, dist_remap, dist_remap, alpha_array])
            dist_img = dist_img.T
            # print("dist_img.shape :", dist_img.shape)

            # print(dist_img)

            dist_4 = dist_img.tolist()
            dist_4 = tuple(map(tuple, dist_4))

            # print("type(dist_4) :", type(dist_4))

            ### Generate New Image
            img_tmp.putdata(tuple(dist_4))
            """

            ################################################################################################


            #########################
            ###                   ###
            ###     Composite     ###
            ###                   ###
            #########################

            # print("Composite")

            ### Scaling
            img_dist = img_tmp.resize((w, h), Image.LANCZOS)

            ### Create Canvas for Composite
            img_canvas = self.create_canvas_alpha(w)

            ### Define Mask
            img_mask = img_src.convert("L")

            ### Composite
            img_result = Image.composite(img_dist, img_canvas, img_mask)

            ### Flip
            ### Image Coordination >> Rhino Coordination
            img_flip = ImageOps.flip(img_result)

            return img_flip