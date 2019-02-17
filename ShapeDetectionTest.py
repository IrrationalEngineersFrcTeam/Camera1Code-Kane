import cv2
import numpy as np
from networktables import NetworkTables
import logging
import sys
import imutils

from findshapespipeline import GripPipeline
from ShapeDetector import ShapeDetector

grip = GripPipeline()
#cap = cv2.VideoCapture("http://10.62.39.96:1181/stream.mjpg")

class Driver:

    rp = NetworkTables.getTable("RaspberryPi")
    shapeDetect = ShapeDetector()

    def __init__(self):

        self.blank_image = np.zeros((480, 640, 3), np.uint8)

        self.contoursImg = None
        self.newVar = None
        self.shapeImg = None

        logging.basicConfig(level=logging.DEBUG)

        NetworkTables.initialize(server='10.62.39.2')

    def drawRectangle(self, contour_output, contour_hierarchy, source0):

        height, width, _ = source0.shape
        min_x, min_y = width, height
        max_x = max_y = 0
        # computes the bounding box for the contour, and draws it on the frame
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

    def drawRectangleBetter(self, img, cnt):

        height, width, _ = img.shape
        min_x, min_y = width, height
        max_x = max_y = 0

        (x,y,w,h) = cv2.boundingRect(cnt)
        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y)
        center = x+(w/2)
        if w > 80 and h > 80:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255, 0, 0), 2)
            cv2.circle(img, (int(x+(w/2)), int(y+(h/2))), 10, (0, 255, 0))

        if max_x - min_x > 0 and max_y - min_y > 0:
            cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
            cv2.circle(img, (int(x+(w/2)), int(y+(h/2))), 10, (0, 255, 0))

    def run(self):
        #while True:
        frame = cv2.imread("shotSmall.jpg")
        resized = imutils.resize(frame, width=480)
        ratio = frame.shape[0] / float(resized.shape[0])
        contoursImg = resized.copy()
        grip.process(contoursImg)
        #cv2.imshow("thresh", grip.hsv_threshold_output)
        cv2.drawContours(self.blank_image, grip.find_contours_output, cv2.FILLED, [0, 0, 255], 2)

        self.shapeImg = contoursImg.copy()

        circleXCenter = self.drawRectangle(grip.filter_contours_output, grip.contour_hierarchy, contoursImg)

        cv2.imshow("rectangle", contoursImg)

        circleXCenter = (circleXCenter - 320) / 3.2
        self.rp.putNumber("distance", circleXCenter)

        centers = np.zeros([2, 2])
        num = 0

        for contour in grip.filter_contours_output:
            shape = self.shapeDetect.detect(contour)
            print(shape)
            M = cv2.moments(contour)
            
            if shape == "rectangle":
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
                centers[num, 0] = cX
                centers[num, 1] = cY
                print(num, centers[num])
                self.drawRectangleBetter(self.shapeImg, contour)
            num += 1

        cv2.imshow("shapes", self.shapeImg)
        cv2.waitKey(0)

    """
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
    """
if __name__ == "__main__":
    driver = Driver()
    driver.run()