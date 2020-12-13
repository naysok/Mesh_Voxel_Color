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


    def find_hierarchy(self, img):

        k = 2
        kernel = np.ones((k, k), np.uint8)
        erosion = cv2.erode(img, kernel, iterations = 1)
        
        gray = cv2.cvtColor(erosion, cv2.COLOR_RGB2GRAY) 

        ### Show
        # cv2.imshow("image", gray)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        ### https://qiita.com/rareshana/items/6a2f5e7396f28f6eee49

        contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # print("contours=",len(contours),  "hierarchy=",len(hierarchy))
        print(hierarchy)

        ### contours[0] : Image Edge
        ### contours[1] : Contour-Outside
        ### contours[2] : Contour-Inside

        cv2.drawContours(img, contours[0], -1,(255,  0,  0),3)
        cv2.drawContours(img, contours[1], -1,(  0,255,  0),3)
        cv2.drawContours(img, contours[2], -1,(  0,  0,255),3)


        ### Show
        cv2.imshow("image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # result = contours[1]
        
        # return result