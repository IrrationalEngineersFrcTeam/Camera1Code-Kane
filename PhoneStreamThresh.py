import numpy as np
import cv2

cap = cv2.VideoCapture("http://192.168.1.201:8080/video")

while(True):

    ret, frame = cap.read()
    blank_image = np.zeros((640,480,3), np.uint8)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #hsv = cv2.cvtColor(hsv, cv2.COLOR_GRAY2HSV)

    """
    upperwhite = np.array([255, 0, 255])
    lowerwhite = np.array([0, 0, 0])
    """

    ret, thresh = cv2.threshold(gray, 30, 200, cv2.THRESH_BINARY)
    #res = cv2.bitwise_and(frame, frame, mask= mask)
    cv2.imshow('thresh', thresh)
    cv2.imshow('init frame', frame)
    contour, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    print(hierarchy)

    """
    for i in len(contour):
        size = cv2.contourArea(contour)
    """

    #print(contour)

    cv2.drawContours(blank_image, contour, cv2.FILLED, [0, 0, 255], 2)

    cv2.imshow('frame',frame)
    #cv2.imshow('img', thresh)
    #cv2.imshow('res', res)
    

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()