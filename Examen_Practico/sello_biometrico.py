import numpy as np
import cv2 as cv

img = np.ones((500,500,3), dtype=np.uint8)*255


# CUERPO
cv.line(img,(100,300),(300,300),(0,0,0),2)

cv.rectangle(img, (10,10), (200,100), (34,56,100), -1)
cv.circle(img, (250,250), 3, (23, 43, 144), -1 )
cv.line(img, (255,255), (200,100), (23, 244, 144), 4)
