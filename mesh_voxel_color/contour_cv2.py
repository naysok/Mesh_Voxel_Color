import numpy as np
import cv2


class ContourCV2():


    def open_image(self, file_path):
        
        img = cv2.imread(file_path)
        
        ### Show
        # cv2.imshow("image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return img


    def export_image(self, img, file_path):

        cv2.imwrite(file_path, img)
        print("imwrite :", file_path)


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


    def find_draw_hierarchy(self, img, up_sapling_xy):

        h, w, c = img.shape
        
        
        ##################################################
        ###                                            ###
        ###   Find Contours                            ###
        ###                                            ###
        ###   1) Erosion (Line ++)                     ###
        ###   2) Find Contour                          ###
        ###   3) Inside / Outside (Select Small-One)   ###
        ###   4) Dilation (Shape ++)                   ### 
        ###                                            ###
        ###################################################


        ### 
        k0 = 3
        kernel = np.ones((k0, k0), np.uint8)
        erosion = cv2.erode(img, kernel, iterations = 1)

        ### Gray Scale
        gray = cv2.cvtColor(erosion, cv2.COLOR_RGB2GRAY)

        ### opencv 4
        ### https://qiita.com/rareshana/items/6a2f5e7396f28f6eee49

        contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # print("contours=",len(contours),  "hierarchy=",len(hierarchy))
        # print(hierarchy)

        # print("Contour Count :", len(contours))


        ########################################


        #########################
        ###                   ###
        ###   Draw Contours   ###
        ###                   ###
        #########################


        ### Not Exit Contours
        if len(contours) <= 1:
            canvas_null = self.create_image(int(w / up_sapling_xy))
            return canvas_null

        ### Draw Contour
        else:

            # ### Draw Line (Test)
            # canvas_line = self.create_image(w)
            #
            # for i in range(len(contours)):
            #
            #     ### contours[0] : Image Edge
            #     # if i != 0:
            #     if i != 0:
            #
            #         cnt = contours[i]
            #         cv2.drawContours(canvas_line, cnt, -1,(0, 0, 255), 1)
            #
            # ### Show
            # cv2.imshow("image", canvas_line)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            ### Draw Fill
            canvas_all = []

            for i in range(len(contours)):

                ### contours[0] : Image Edge
                if i != 0:

                    canvas = self.create_image(w)
                    cnt = contours[i]
                    
                    ### cv2.fillPoly / cv2.fillConvecFill
                    ### http://dothiko.hatenablog.com/entry/2018/12/24/003822
                    cv2.fillPoly(canvas, [cnt], (1, 0, 0))

                    canvas_all.append(canvas)

            ### Contour Image
            img_boolean = self.boolean_canvas(canvas_all)

            ### Dilation
            k1 = 4
            kernel = np.ones((k1, k1), np.uint8)
            dilation = cv2.dilate(img_boolean, kernel, iterations = 1)

            ### Resize
            orgHeight, orgWidth = dilation.shape[:2]
            new_size = (int(orgHeight / up_sapling_xy), int(orgWidth / up_sapling_xy))
            # print(new_size)

            result = cv2.resize(dilation, new_size)

            # ### Show
            # cv2.imshow("image", result)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            
            return result