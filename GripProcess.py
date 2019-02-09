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

    height, width, _ = frame.shape
    min_x, min_y = width, height
    max_x = max_y = 0

    # computes the bounding box for the contour, and draws it on the frame,
    for contour, hier in zip(grip.filter_contours_output, grip.contour_hierarchy):
        (x,y,w,h) = cv2.boundingRect(contour)
        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y)
        if w > 80 and h > 80:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)

        if max_x - min_x > 0 and max_y - min_y > 0:
            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
