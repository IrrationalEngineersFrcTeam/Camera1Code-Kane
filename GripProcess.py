import cv2
import numpy as np
from networktables import NetworkTables
import logging
import sys
from multiprocessing import Process
from grip import GripPipeline

"""
grip = GripPipeline()

cap = cv2.VideoCapture(0)

blank_image = np.zeros((480, 640, 3), np.uint8)

contoursImg = None
newVar = None

logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize(server='10.62.39.2')

rp = NetworkTables.getTable("RaspberryPi")"""


class Main():

    def __init__(self):
        self.grip = GripPipeline()

        self.cap = cv2.VideoCapture(0)

        self.blank_image = np.zeros((480, 640, 3), np.uint8)

        self.contoursImg = None
        self.newVar = None

        logging.basicConfig(level=logging.DEBUG)

        NetworkTables.initialize(server='10.62.39.2')

        self.rp = NetworkTables.getTable("RaspberryPi")

        
        


    def drawRectangle(self, contour_output, contour_hierarchy, source0):

        height, width, _ = source0.shape
        min_x, min_y = width, height
        max_x = max_y = 0
        # computes the bounding box for the contour, and draws it on the frame,
        for contour, hier in zip(contour_output, contour_hierarchy):
            (x,y,w,h) = cv2.boundingRect(contour)
            min_x, max_x = min(x, min_x), max(x+w, max_x)
            min_y, max_y = min(y, min_y), max(y+h, max_y)
            center = x+(w/2)
            if w > 80 and h > 80:
                cv2.rectangle(source0, (x,y), (x+w,y+h), (255, 0, 0), 2)
                cv2.circle(source0, (int(x+(w/2)), int(y+(h/2))), 10, (0, 255, 0))

            if max_x - min_x > 0 and max_y - min_y > 0:
                cv2.rectangle(source0, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
                cv2.circle(source0, (int(x+(w/2)), int(y+(h/2))), 10, (0, 255, 0))

        return center

    def drawRectangleBetter(self, cnt, img):
        rect = cv2.minAreaRect(img)
        box = cv2.boxPoints(rect) # cv2.boxPoints(rect) for OpenCV 3.x
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, (0,0,255), 2)

    def run(self):

        while True:
            ret, frame = self.cap.read()
            contoursImg = frame.copy()
            self.grip.process(frame)

            cv2.drawContours(self.blank_image, self.grip.find_contours_output, cv2.FILLED, [0, 0, 255], 2)

            circleXCenter = self.drawRectangle(self.grip.filter_contours_output, self.grip.contour_hierarchy, contoursImg)

            #cv2.imshow("source", frame)
            #cv2.imshow("rectangle", contoursImg)
            #cv2.imshow("frame", blank_image)
            circleXCenter = (circleXCenter - 320) / 10
            self.rp.putNumber("distance", circleXCenter)
            #rp.getNumber("distance", newVar)
            #print(newVar)

            
main = Main()

if __name__ == '__main__':
    
   main.run()