import math
import cv2 as cv
import numpy as np

##### TRASLADAR 40, ROTAR 45 SENTIDO HORARIO Y ESCALA 2, ROTA 90 SENTIDO ANTIHORARIO

img = cv.imread('Imagenes/manzana.jpg', 0)
x, y = img.shape

# TRASLADAR 40
dx, dy = 40, 40
translated = np.zeros((x, y), dtype=np.uint8)
for i in range(x):
    for j in range(y):
        new_x, new_y = i + dx, j + dy
        if new_x < x and new_y < y:
            translated[new_x, new_y] = img[i, j]

# ROTAR 45° HORARIO
theta = math.radians(-45)
rotated1 = np.zeros((x, y), dtype=np.uint8)
cx, cy = x//2, y//2
for i in range(x):
    for j in range(y):
        ox = int((j-cy)*math.cos(theta) + (i-cx)*math.sin(theta) + cx)
        oy = int(-(j-cy)*math.sin(theta) + (i-cx)*math.cos(theta) + cy)
        if 0 <= ox < y and 0 <= oy < x:
            rotated1[i, j] = translated[oy, ox]

# ESCALAR A 2
scale = 2
sx, sy = x*2, y*2
scaled = np.zeros((sx, sy), dtype=np.uint8)
for i in range(sx):
    for j in range(sy):
        ox, oy = i//2, j//2
        if ox < x and oy < y:
            scaled[i, j] = rotated1[ox, oy]

# ROTAR 90° ANTIHORARIO (intercambiando filas y columnas)
final = np.zeros((sy, sx), dtype=np.uint8)
for i in range(sy):
    for j in range(sx):
        final[i, j] = scaled[sx - j - 1, i]

cv.imshow('Resultado', final)
cv.waitKey(0)