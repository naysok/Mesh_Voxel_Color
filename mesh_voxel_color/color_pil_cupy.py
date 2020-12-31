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


    #####################
    ####              ###
    ####     Math     ###
    ####              ###
    #####################


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

        ### Generate Distance-List with DownSampling

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


    ################################################################################


    #####################
    ####              ###
    ####     Draw     ###
    ####              ###
    #####################


    def scan_image_calc_color(self, file_path, height, pts_cp, downsampling_xy):

        ### Open Image
        img_src = self.open_image(file_path)
        
        w, h = img_src.size
        ww = int(w / downsampling_xy)
        hh = int(h / downsampling_xy)

        ### DownSampling
        img = img_src.resize((ww, hh))

        ### Result Canvas
        img_result = self.create_canvas_alpha(w)


        ### Read Shape
        px = img.getdata()
        px_cp = cp.array(px)
        print("px_cp.shape :", px_cp.shape)

        ### Segment Contour True/False
        px_seg_0 = cp.amax(px_cp)


        ### Contour : True
        if px_seg_0 > 127:

            ### Running on Cuda
            # print("Running on Cuda !!")

            ### Calc Distance
            print("Distance")
            # dist_list = self.gen_disctance_list(w, h, height, pts_cp)
            dist_list = self.gen_disctance_list_ds(w, h, height, downsampling_xy, pts_cp)


            ### Generate Color From Distance
            print("Color")


            dist_remap = self.remap_number_cp(dist_list, 0, 200, 0, 255)
            dist_remap = dist_remap.astype('int64')

            # print("dist_remap.shape :", dist_remap.shape)
            
            ### Fill Array (255)
            alpha_array = cp.ones(dist_list.shape) * 255
            alpha_array = alpha_array.astype('int64')


            dist_img = cp.stack([dist_remap, dist_remap, dist_remap, alpha_array])
            dist_img = dist_img.T
            print("dist_img.shape :", dist_img.shape)

            # print(dist_img)

            dist_4 = dist_img.tolist()
            dist_4 = tuple(map(tuple, dist_4))

            print("type(dist_4) :", type(dist_4))

            ### Generate New Image
            img_result.putdata(tuple(dist_4))

            return img_result


            ########################################


            ### Generate New Image
            # img_result.putdata(tuple(px_result))

            # return img_result

            # px_result = []
            
            # px_np = cp.array(px)
            # dist_cp = dist_list

            # shape_cp = cp.amin(px_np, axis=1)

            # shape_cp_bin = cp.where(shape_cp > 127, 1, 0)
            # shape_cp_alpha = cp.where(shape_cp > 127, 255, 0)
            

            # print("dist.shape :", dist_cp.shape)
            # print("shape.shape :", shape_cp.shape)

            # th_0 = 30
            # th_1 = 60
            # th_2 = 90
            # th_3 = 120

            # # dist_cp = cp.where(dist_cp < th_0, )


            # dist_shape_cp = dist_cp * shape_cp
            # # print("dist_shape_cp.shape :", dist_shape_cp.shape)
            
            # dist_img = cp.stack([dist_cp, dist_cp, dist_cp, dist_cp])
            # dist_img = dist_img.T
            # print("dist_img.shape :", dist_img.shape)

            # dist = dist_img.tolist()

            # exit()

            ### Generate New Image
            # img_result.putdata(tuple(px_result))

            # return img_result
        
            # return None

            # px_result = np.where(dist_np < 4, -1, 100)

            # for j in range(px_length):
                
            #     rr, gg, bb = px[j]
            #     d = dist_list[j]

            #     black = (0, 0, 0, 255)
            #     white = (255, 255, 255, 255)
            #     red = (255, 0, 0, 255)
            #     green = (0, 255, 0, 255)
            #     blue = (0, 0, 255, 255)



            #     ### White (Inside)
            #     if rr > 127:
                    
            #         th_0 = 20
            #         th_1 = 40
            #         th_2 = 60
            #         th_3 = 80



                    
            #         if d < th_0:
            #             px_result.append(red)

            #         elif d < th_1:
            #             px_result.append(green)

            #         elif d < th_2:
            #             px_result.append(blue)

            #         elif d < th_3:
            #             px_result.append(white)

            #         else:
            #             px_result.append(black)

            #     ### Outside
            #     else:
            #         c = (0, 0, 0, 0)
            #         px_result.append(c)
                    
            # ### Generate New Image
        #     img_result.putdata(tuple(px_result))

        #     return img_result



        ### Contour : False
        else:
            px_result = [(0, 0, 0, 0) for i in range(w) for j in range(h)]
            img_result.putdata(tuple(px_result))
            return img_result