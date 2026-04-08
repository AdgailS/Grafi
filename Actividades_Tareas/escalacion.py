import math
import cv2 as cv
import numpy as np


### TAREA 1: TRASLADAR 20, ESCALAR A 1/5 Y ROTAR 45 

img = cv.imread('Imagenes/manzana.jpg', 0)
x, y = img.shape

# TRASLADAR 20
dx, dy = 20, 20
translated = np.zeros((x, y), dtype=np.uint8)
for i in range(x):
    for j in range(y):
        new_x, new_y = i + dx, j + dy
        if 0 <= new_x < x and 0 <= new_y < y:
            translated[new_x, new_y] = img[i, j]

# ESCALAR A 1/5
scale = 1/5
sx, sy = int(x * scale), int(y * scale)
scaled = np.zeros((sx, sy), dtype=np.uint8)
for i in range(sx):
    for j in range(sy):
        orig_x, orig_y = int(i / scale), int(j / scale)
        if orig_x < x and orig_y < y:
            scaled[i, j] = translated[orig_x, orig_y]

# ROTAR 45°
angle = 45
theta = math.radians(angle)
rotated = np.zeros((sx, sy), dtype=np.uint8)
cx, cy = sx // 2, sy // 2
for i in range(sx):
    for j in range(sy):
        orig_x = int((j - cy) * math.cos(theta) + (i - cx) * math.sin(theta) + cx)
        orig_y = int(-(j - cy) * math.sin(theta) + (i - cx) * math.cos(theta) + cy)
        if 0 <= orig_x < sy and 0 <= orig_y < sx:
            rotated[i, j] = scaled[orig_y, orig_x]

cv.imshow('Resultado', rotated)
cv.waitKey(0)
cv.destroyAllWindows()