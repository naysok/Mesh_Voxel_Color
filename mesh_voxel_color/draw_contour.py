import sys
sys.path.append("_module_\\Contour_Draw_3D")

from contour_draw_3d import image_processing


class DrawContour(image_processing.ImageProcessing):

    def print_hello(self):
        print("Hello")