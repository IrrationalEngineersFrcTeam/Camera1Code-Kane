import cv2
import numpy as np
from matplotlib import pyplot as plt
import urllib3
import io
import imutils
from ShapeDetector import ShapeDetector
import argparse
from numpy import zeros
#tutorial from https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/

url='http://192.168.1.171:8080/shot.jpg'
#http = urllib3.PoolManager()
#imgResp=http.request('GET',url)
# Numpy to convert into a array
#imgNp = np.array(bytearray(imgResp.data), dtype=np.uint8)
# Finally decode the array to OpenCV usable format ;)
#image = cv2.imdecode(imgNp, -1)

#cap = cv2.VideoCapture(url)

#image = cap.read()
#cv2.imshow("Image1", image)
#cv2.waitKey(0)
# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,help="path to the input image")
#args = vars(ap.parse_args())
# load the image and resize it to a smaller factor so that
# the shapes can be approximated better

image = cv2.imread('shotSmall.jpg')
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
height=image.shape[0]
width=image.shape[1]

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#blurred = cv2.medianBlur(gray, 11)
thresh = cv2.threshold(blurred, 170, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()
# loop over the contours
num=0

loc = zeros([2,2])

for c in cnts:
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)
    shape = sd.detect(c)
    if shape=='rectangle':
        
        shape=shape+"_"+str(num)
        #looks like numpy arrays are x(r,c) so a 3 x 3 array still has two indices
        loc[num,0]=cX
        loc[num,1]=cY

        #loc[num-1,num]=cY
        print(num,loc)
        num+=1
    # multiply the contour (x, y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape on the image
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    centerX=int(width/2)
    centerY=int(height/2)
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2)

    # show the output image

    cv2.imshow("gray", gray)
    cv2.imshow("blur", blurred)
    cv2.imshow("THRESH", thresh)
#'x' is relative to the frame
cv2.putText(image,'C', (centerX,int(loc[0,1])), cv2.FONT_ITALIC,
            1.0,(0,255,0),1,1)
midpoint=int(min(loc[0,0],loc[1,0])+(abs(loc[0,0]-loc[1,0]))/2)
#a is the midpoint between the two images
cv2.putText(image,'M', (midpoint,int(loc[0,1])), cv2.FONT_ITALIC,
            1.0,(0,255,0),1,1)
cv2.imshow("Image", image)
cv2.waitKey(0)