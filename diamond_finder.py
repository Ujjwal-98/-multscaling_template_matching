#!/usr/bin/env python

import cv2 as cv
import sys
import os
import shutil
import numpy as np
import imutils
from imutils.object_detection import non_max_suppression
from glob import glob

import time


# class diamond_finder:
    # def __init__(self):
    #     pass

def find_diamond():
    img_files = glob("input_imgs/*")

    ### Read the template image
    template_bgr = cv.imread("template.jpg")
    template_gray = cv.cvtColor(template_bgr, cv.COLOR_BGR2GRAY)
    w, h = template_gray.shape[::-1]

    output = {}
    for i, iterator in enumerate(img_files):
        img_bgr = cv.imread(iterator)
        # cv.imshow("s", img_bgr)
        # print(iterator)
        if img_bgr is None:
            sys.exit("Could not read the image.")

        img_gray = cv.cvtColor(img_bgr, cv.COLOR_BGR2GRAY)

        # initialize our list of final_rectangles to be printed on nth image (iterator)
        # final_rects = []
        final_rects2 = []

        t0=time.time()
        # resizing the input_images to match the given_template

        for scale in np.linspace(1.0, 5, 20)[::-1]:
            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            resized = imutils.resize(img_gray, width=int(img_gray.shape[1] * scale))
            r = img_gray.shape[1] / float(resized.shape[1])
            # if the resized image is smaller than the template, then break
            # from the loop
            # if resized.shape[0] < h or resized.shape[1] < w:
            #     break
            # template_matching with the resized image
            res = cv.matchTemplate(resized, template_gray, cv.TM_CCOEFF_NORMED)
            threshold = 0.95
            # coordinates of the point where it achieves the given threshold
            (yCoords, xCoords) = np.where(res >= threshold)

            # print('scale:{:2.3}  matches:{:4} rect:{}'.format(scale, len(yCoords), len(final_rects2)))
            
            ### Find rectangle coordiantes and apply the non-max suppresion
            if yCoords.size != 0: # not empty
                temp_rects = np.stack((xCoords, yCoords, xCoords+w, yCoords+h)).T  # rectangle cooridnates
                pick = non_max_suppression(temp_rects)                             # apply non-maximal suppression
                pick_ind = r*np.array(pick)
                final_rects2.append(pick_ind.astype('int'))
        
        t1 = time.time()
        # print('time taken', t1-t0)



        # many overlapping boxes due to the resizing, therefore apply non-maxima suppression to the rectangles one more time
        # final_pick = non_max_suppression(np.array(final_rects))
        name = iterator.split('/')
        if len(final_rects2) != 0:
            img_coord = []
            final_pick = non_max_suppression(np.concatenate(final_rects2))
            print('{}-Image {}: Detected {} diamonds'.format(i, name[1], len(final_pick)))
            for (startX, startY, endX, endY) in final_pick:
                # draw the bounding box on the image
                cv.rectangle(img_bgr, (int(startX), int(startY)), (int(endX), int(endY)), (255, 0, 0), 1)
                img_coord.append([int(startX), int(startY)])    
                print('{}, {}'.format(int(startX), int(startY)))
            output[name[1]] = img_coord
        else:
            print('{}-Image {}: No diamonds detected!'.format(i, name[1]))
            output[name[1]] = []
        '''cv.imshow("Display window", img_bgr)
        cv.imshow("original", img_gray)
        k = cv.waitKey(10)'''

        if not cv.imwrite('output_imgs/' + name[1], img_bgr):
            raise Exception("Could not write image")
    return output



if __name__==   "__main__":
    # obj = diamond_finder()
    t0 = time.time()
    # obj.find_diamond()
    find_diamond()
    print('total time:', time.time()-t0)

