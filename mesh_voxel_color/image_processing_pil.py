import math
from PIL import Image, ImageDraw, ImageOps, ImageEnhance


from .import util
ut = util.Util()


class ImageProcessingPIL():


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


    ########################################


    ##############################
    ####                       ###
    ####     Draw, Convert     ###
    ####                       ###
    ##############################


    def convert_vert2_to_line(self, canvas_size, volume_size, up_sampling_xy, vert2):
        
        ### vert2 = [vert, vert]
        ### vert2 = [[x0, y0, z0], [x1, y1, z1]]
        
        p0 = vert2[0]
        p1 = vert2[1]

        _v0 = p0[0]
        _v1 = p0[1]
        _v2 = p1[0]
        _v3 = p1[1]
        
        ### Clac Resolution
        v0 = ut.remap_number(_v0, 0, volume_size, 0, canvas_size * up_sampling_xy)
        v1 = ut.remap_number(_v1, 0, volume_size, 0, canvas_size * up_sampling_xy)
        v2 = ut.remap_number(_v2, 0, volume_size, 0, canvas_size * up_sampling_xy)
        v3 = ut.remap_number(_v3, 0, volume_size, 0, canvas_size * up_sampling_xy)

        line = [v0, v1, v2, v3]

        return line


    def convert_vert2s_to_lines(self, canvas_size, volume_size, up_sampling_xy, vert2s):

        ### vert2s = [vert2, vert2, , , , , , vert2]
        ### vert2s = [[[x0, y0, z0], [x1, y1, z1]], , , , , , [[xm, ym, zm], [xn, yn, zn]]]
        
        lines = []

        for i in range(len(vert2s)):
            vert2 = vert2s[i]
            line = self.convert_vert2_to_line(canvas_size, volume_size, up_sampling_xy, vert2)
            lines.append(line)

        return lines


    def draw_line(self, canvas_draw, line):

        ### Color : Black
        ### Line Width : 2

        canvas_draw.line((line), fill = (0, 0, 0), width = 3)
        return canvas_draw


    def draw_lines(self, canvas, canvas_size, volume_size, up_sampling_xy, lines):

        ### Lines = vert2s
        ### vert2s = [vert2, vert2, , , , , , vert2]
        ### vert2s = [[[x0, y0, z0], [x1, y1, z1]], , , , , , [[xm, ym, zm], [xn, yn, zn]]]
        
        ### Convert (vert2s >> lines) + Clac Resolution
        lines_draw = self.convert_vert2s_to_lines(canvas_size, volume_size, up_sampling_xy, lines)

        ### Convert Canvas to Draw
        canvas_draw = ImageDraw.Draw(canvas)

        for i in range(len(lines_draw)):
            line = lines_draw[i]
            self.draw_line(canvas_draw, line)

        return canvas_draw


    ########################################


    def draw_contours(self, prj_path, canvas_size, volume_size, up_sampling_xy, index, lines):

        ### Create Canvas
        canvas = self.create_canvas(canvas_size * up_sampling_xy)
        
        ### Draw Lines
        self.draw_lines(canvas, canvas_size, volume_size, up_sampling_xy, lines)

        ### Format
        index_pad = "%04d"%(int(index))

        ### Save Canvas
        export_path = prj_path + "image_0\\image_{}.jpg".format(str(index_pad)) 
        self.export_image(canvas, export_path)