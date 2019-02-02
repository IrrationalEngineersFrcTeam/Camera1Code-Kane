import numpy as np
import cv2

areaArray = []

frame = cv2.imread('1ftH2ftD1Angle0Brightness.jpg')
frame = cv2.medianBlur(frame, 11)
blank_image = np.zeros((480, 640, 3), np.uint8)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#hsv = cv2.cvtColor(hsv, cv2.COLOR_GRAY2HSV)


upperwhite = np.array([255, 0, 255])
lowerwhite = np.array([0, 0, 0])


ret, thresh = cv2.threshold(gray, 30, 200, cv2.THRESH_BINARY)
#res = cv2.bitwise_and(frame, frame, mask= mask)
cv2.imshow('thresh', thresh)
cv2.imshow('init frame', frame)
contour, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

print(hierarchy)

cv2.drawContours(blank_image, contour, cv2.FILLED, [0, 0, 255], 2)

for i, c in enumerate(contour):
    area = cv2.contourArea(c)
    areaArray.append(area)

print(areaArray)

sorteddata = sorted(zip(areaArray, contour), key=lambda x: x[0], reverse=True)

for i, c in enumerate(sorteddata):
    if i > 1:
        sorteddata.remove(sorteddata[i])

print(sorteddata)


#print(sorteddata)

for i, c in enumerate(areaArray):
    if i > 2:
        sorteddata.remove(sorteddata[i])

#print(sorteddata)

cv2.imshow('contours', blank_image)
#cv2.imshow('img', thresh)
#cv2.imshow('res', res)

cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("gray_peg.jpeg", thresh)
