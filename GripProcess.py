import cv2
import numpy as np

from grip import GripPipeline

grip = GripPipeline()

cap = cv2.VideoCapture("http://192.168.2.2:1181/stream.mjpg")
blank_image = np.zeros((480, 640, 3), np.uint8)

while True:
    ret, frame = cap.read()
    grip.process(frame)

    cv2.drawContours(blank_image, grip.find_contours_output, cv2.FILLED, [0, 0, 255], 2)

    cv2.imshow("source", frame)
    cv2.imshow("frame", blank_image)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break