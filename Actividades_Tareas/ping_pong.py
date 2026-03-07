import cv2 as cv
import numpy as np 

img = np.ones((500,500), np.uint8)*255

for i in range (400):
    cv.circle(img, (i,i), 20, (i, 0, 0), -1) # las i hacen que vaya en linea
    #MODIFICAR EL CICLO, HACER SUMAS Y RESTAS A i
    cv.imshow('img', img)
    img = np.ones((500,500,3), np.uint8) *150
    cv.waitKey(10)

cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()