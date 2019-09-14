
import cv2
import numpy as np
from networktables import NetworkTables
import logging
import sys
import imutils

from findshapespipeline import GripPipeline
from ShapeDetector import ShapeDetector
from PID import PID

grip = GripPipeline()

# initial working pid values
# P: 0.001
# I: 0
# D: 0

pid = PID(0.001, 0.001, 0)
#cap = cv2.VideoCapture("http://10.62.39.96:1181/stream.mjpg")


class Driver:

    singleImg = True


    def __init__(self):
        #initalize the various blank or cloned images
        self.blank_image = np.zeros((480, 640, 3), np.uint8)
        self.contoursImg = None
        self.shapeImg = None
        self.centers = None                                                                                                     
        self.frame = None
        self.contoursImg = None
        self.isSeen = None
        

        #set up camera stream
        self.cap = cv2.VideoCapture("http://10.62.39.55:1181/stream.mjpg")
        
        #Practice IP: 10.62.39.55
        #Competition IP: 10.62.39.12
        
        #self.cap = cv2.VideoCapture(0)

        #start the logging and set the level

        #set up Network Tables
        self.rp = NetworkTables.getTable("Camera1")
        self.shapeDetect = ShapeDetector()
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

        #compute the bounding rectangle and get x, y, width and height variables of the rectangle
        (x,y,w,h) = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x,y), (x+w,y+h), (255, 0, 0), 2)

        cX = int(x+(w/2))
        cY = int(y+(h/2))

        cv2.circle(img, (cX, cY), 10, (0, 255, 0))
        return cX, cY

    def runSingleImg(self):

        self.frame = cv2.imread("shotSmall.jpg")
        resized = imutils.resize(self.frame, width=320, inter=cv2.INTER_CUBIC)
        ratio = self.frame.shape[0] / float(resized.shape[0])
        self.contoursImg = resized.copy()
        grip.process(self.contoursImg)
        #cv2.imshow("thresh", grip.hsv_threshold_output)

        self.shapeImg = self.contoursImg.copy()

        circleXCenter = self.drawRectangle(grip.filter_contours_output, grip.contour_hierarchy, self.contoursImg)

        cv2.imshow("rectangle", self.contoursImg)

        circleXCenter = (circleXCenter - 320) / 3.2
        self.rp.putNumber("distance", circleXCenter)

        self.centers = np.zeros([2, 2])
        num = 0

        for contour in grip.filter_contours_output:
            shape = self.shapeDetect.detect(contour)
            #print(shape)
            M = cv2.moments(contour)
            
            if shape == "rectangle":
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
                self.centers[num, 0] = cX
                self.centers[num, 1] = cY
                print(num, self.centers[num])
                self.drawRectangleBetter(self.shapeImg, contour)
                num += 1
                if num == 2:
                    break

        cv2.imshow("shapes", self.shapeImg)
        cv2.waitKey(0)

    """
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
    """
    def runCameraStream(self):
        i = 0
        while True:
            try:
                ret, self.frame = self.cap.read()
                resized = imutils.resize(self.frame, width=640, height=480, inter=cv2.INTER_CUBIC)
                ratio = self.frame.shape[0] / float(resized.shape[0])
                self.contoursImg = resized.copy()
                grip.process(self.contoursImg)
                print("test")
                #cv2.imshow("thresh", grip.hsv_threshold_output)

                self.shapeImg = self.contoursImg.copy()

                #circleXCenter = self.drawRectangle(grip.filter_contours_output, grip.contour_hierarchy, self.contoursImg)

                cv2.imshow("rectangle", self.contoursImg)
                
                cv2.imshow("thresh", grip.hsv_threshold_output)

                #circleXCenter = (circleXCenter - 320) / 3.2
                #self.rp.putNumber("distance", circleXCenter)
                #self.centers = np.zeros([2, 2])
                num = 0
                if grip.filter_contours_output is None:
                    raise ValueError

                self.centers = np.zeros([int(len(grip.filter_contours_output)), 2])

                for contour in grip.filter_contours_output:
                    shape = self.shapeDetect.detect(contour)
                    #print(len(grip.filter_contours_output))
                    #print(shape)
                    
                    if shape == "rectangle":
                        cX, cY = self.drawRectangleBetter(self.shapeImg, contour)
                        self.centers[num, 0] = cX
                        self.centers[num, 1] = cY
                        #print(num, self.centers[num])
                        num += 1

                try:
                    centerXPos = self.centers[0, 0] + ((self.centers[1, 0] - self.centers[0, 0]) / 2)
                    centerYPos = int(self.centers[1, 1] + ((self.centers[0, 1] - self.centers[1, 1]) / 2))

                    cv2.circle(self.shapeImg, (int(centerXPos), centerYPos), 10, (0, 0, 255))

                    centerXPos = int(np.interp(centerXPos, [0, 640], [-100, 100]))

                    #print(str(centerXPos) + " " + str(centerYPos))
                    self.isSeen = True

                    speed = -pid.calculateSpeed(centerXPos)
                    self.rp.putBoolean("isSeen", self.isSeen)

                    
                    self.rp.putNumber("distance", -speed)
                    #i = 0
                    print(-speed)
                    #i += 1

                except IndexError:
                    print("something went wrong")
                    self.isSeen = False

                cv2.circle(self.shapeImg, (int(640/2), int(480/2)), 5, (0, 0, 255))
                
                cv2.imshow("shapes", self.shapeImg)
                #print(self.isSeen)
                #cv2.waitKey(0)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except ValueError:
                print("Filter contours empty")
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    

if __name__ == "__main__":
    driver = Driver()
    driver.runCameraStream()
