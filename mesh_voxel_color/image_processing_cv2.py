import numpy as np
import cv2


class ImageProcessingCV2():


    def open_image(self, file_path):
        
        img = cv2.imread(file_path)
        
        ### Show
        # cv2.imshow("image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return img


    def create_image(self, image_size):

        ### Create Black Image
        img = np.zeros((image_size, image_size, 3), np.uint8)
        
        ### Show
        # cv2.imshow("image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return img


    def canvas_segment(self, channel):

        new_channel = ((channel + 2)%4 == 0).astype(np.uint8)
        new_channel = new_channel * 255

        return new_channel


    def boolean_canvas(self, canvas_all):
        
        for i in range(len(canvas_all)):

            bb, gg, rr = cv2.split(canvas_all[i])

            if i == 0:
                boolean_ = bb
            
            else:
                boolean_ += bb
        
        canvas_seg = self.canvas_segment(boolean_)

        img_segment = cv2.merge((canvas_seg, canvas_seg, canvas_seg))

        return img_segment


    def find_hierarchy(self, img):

        h, w, c = img.shape
        
        ### 
        k0 = 3
        kernel = np.ones((k0, k0), np.uint8)
        erosion = cv2.erode(img, kernel, iterations = 1)

        ### Gray Scale
        gray = cv2.cvtColor(erosion, cv2.COLOR_RGB2GRAY)

        ### Show
        cv2.imshow("image", gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        ### opencv 4
        ### https://qiita.com/rareshana/items/6a2f5e7396f28f6eee49

        contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # print("contours=",len(contours),  "hierarchy=",len(hierarchy))
        # print(hierarchy)

        ### Nesting
        hierarchy = hierarchy[0]

        ### Segment
        canvas_all = []

        for i in range(len(contours)):

            ### contours[0] : Image Edge
            if i != 0:

                canvas = self.create_image(w)
                cnt = contours[i]
                cv2.fillConvexPoly(canvas, cnt, (1, 0, 0))

                canvas_all.append(canvas)

        img_boolean = self.boolean_canvas(canvas_all)

        ### Show
        cv2.imshow("image", img_boolean)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # result = contours[1]
        
        # return result