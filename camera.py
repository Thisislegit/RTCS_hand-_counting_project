import cv2
import numpy as np
import time


cv2.namedWindow('Mywindow')
cameraCapture = cv2.VideoCapture(0)
#cameraCapture.set(3,64)
#cameraCapture.set(4,64)
success, image = cameraCapture.read(0)

while success and cv2.waitKey(1) == -1:
	image = cv2.resize(image, (64, 64),interpolation=cv2.INTER_AREA)
	cv2.imshow('Mywindow',image)
	print(image.shape)
	time.sleep(1)
	success, image = cameraCapture.read(0)
	cv2.waitKey(30)
	success, image = cameraCapture.read(0)
    

cv2.destroyWindow('Mywindow')
cv2.destroyWindow('ColorWindow')
cameraCapture.release()
