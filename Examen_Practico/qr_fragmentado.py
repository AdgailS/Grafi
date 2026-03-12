import cv2 as cv
import numpy as np
import math


img1 = cv.imread('Imagenes/m2_mitad1.png', 0)
img2 = cv.imread('Imagenes/m2_mitad2.png', 0)

imagen_nueva = np.zeros((400, 400), dtype=np.uint8)

h1, w1 = img1.shape
h2, w2 = img2.shape

centro_x = 200
centro_y = 200


centro_img1_x = w1 // 2
centro_img1_y = h1 // 2

dx = centro_x - centro_img1_x
dy = centro_y - centro_img1_y

for i in range(h1):
    for j in range(w1):
        new_y = i + dy
        new_x = j + dx
        
        if 0 <= new_y < 400 and 0 <= new_x < 400:
            imagen_nueva[new_y, new_x] = img1[i, j]


cv.imshow('Imagen 1 en el centro', imagen_nueva)


#### IMAGEN 2


cx = w2 // 2
cy = h2 // 2

cx2 = (w2*2) // 2
cy2 = (h2*2) // 2

imagen_nueva2 = np.zeros((h2*2, w2*2), dtype=np.uint8)

angle = 180
theta = math.radians(angle)

cos_t = math.cos(theta)
sin_t = math.sin(theta)

xx, yy = img2.shape

for y_d in range(h2*2):
    for x_d in range(w2*2):
        x = x_d - cx2
        y = y_d - cy2
        
        x_src = x * cos_t - y * sin_t + cx
        y_src = x * sin_t + y * cos_t + cy

        x_src = int(x_src)
        y_src = int(y_src)

        if 0 <= x_src < w2 and 0 <= y_src < h2:
            imagen_nueva2[y_d, x_d] = img2[y_src, x_src]

cv.imshow("Original", img2)
cv.imshow("Imagen Rotada", imagen_nueva2)


cv.waitKey(0)
cv.destroyAllWindows()


