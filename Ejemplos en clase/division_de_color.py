
import cv2 as cv
import numpy as np

img1 = cv.imread('tortuga.jpg' )
x,y,z = img1.shape
print(x,y,z)
img2 = np.zeros((x,y), np.uint8)

b,g,r = cv.split(img1)

mr= cv.merge([img2, img2, r])
mg= cv.merge([img2, g , img2])
mb= cv.merge([b, img2, img2])

nueva1 = cv.merge([r,g,b])
nueva2= cv.merge([g,b,r])
nueva3 = cv.merge([b,r,g])

cv.imshow('n2', nueva1)
cv.imshow('n2', nueva2)
cv.imshow('n3', nueva3)

cv.imshow('b', mb)
cv.imshow('g', mg)
cv.imshow('r', mr)

cv.imshow('img', img1)

cv.waitKey(1)
cv.destroyAllWindows()