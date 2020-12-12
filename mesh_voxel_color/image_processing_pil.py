import math
from PIL import Image, ImageDraw, ImageOps, ImageEnhance


class ImageProcessingPIL():

    def open_image(self, path):
        img = Image.open(path)
        return img


    def export_image(self, img, path):
        img.save(path, quality=100)
        print("Export : {}".format(path))
    

    def create_canvas(self, canvas_size):
        new = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        return new
    
    
    def draw_line(self, canvas_draw, line):

        canvas_draw.line((line), fill=(0, 0, 0), width = 2)
        return canvas_draw


    def draw_lines(self, canvas, lines):

        ### Lines = vert2s
        ### vert2s = [vert2, vert2, , , , , , vert2]
        ### vert2s = [[[x0, y0, z0], [x1, y1, z1]], , , , , , [[xm, ym, zm], [xn, yn, zn]]]
        
        lines = [[0, 0, 200, 200], [200, 0, 200, 200]]

        ### Convert Canvas to Draw
        canvas_draw = ImageDraw.Draw(canvas)

        for i in range(len(lines)):
            line = lines[i]
            self.draw_line(canvas_draw, line)

        return canvas_draw


    ########################################


    def draw_contours(self, prj_path, canvas_size, index, lines):

        ### Create Canvas
        canvas = self.create_canvas(canvas_size)
        
        ### Draw Lines
        self.draw_lines(canvas, None)

        ### canvas.show()

        ### Save Canvas
        export_path = prj_path + "image_0\\image_{}.png".format(str(int(index))) 
        self.export_image(canvas, export_path)