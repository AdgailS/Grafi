import cv2 as cv
import numpy as np

lienzo = np.zeros((500,500,3), dtype=np.uint8)
lienzo[:] = (50,20,20)   

cv.circle(lienzo, (250,250), 100, (0,255,255), 3)

cv.rectangle(lienzo, (200,200), (300,300), (0,0,255), -1)

cv.line(lienzo, (0,0), (500,500), (255,255,255), 2)
cv.line(lienzo, (0,500), (500,0), (255,255,255), 2)

cv.imshow("Sello", lienzo)

cv.waitKey(0)
cv.destroyAllWindows()