import math

import cv2 as cv
import numpy as np

img = cv.imread('Imagenes/tortuga.jpg', 0)

x, y = img.shape

translated_img = np.zeros((x, y), dtype=np.uint8)

# Definir el desplazamiento en x e y
dx, dy = 20, 20

# Trasladar la imagen
for i in range(x):
    for j in range(y):
        new_x = i + dx
        new_y = j + dy
        if 0 <= new_x < x and 0 <= new_y < y:
            translated_img[new_x, new_y] = img[i, j]
         
xx, yy = rotated_img.shape    #//////////////////////////////////////7
cx, cy = int(x  // 2), int(y  // 2)

scale = 1/5

# Escalar a 1/5
scaled_x = int(x * scale)
scaled_y = int(y * scale)

scaled_img = np.zeros((scaled_x, scaled_y), dtype=np.uint8)

for i in range(scaled_x):
    for j in range(scaled_y):
        orig_x = int(i / scale)
        orig_y = int(j / scale)

        if orig_x < x and orig_y < y:
            scaled_img[i, j] = translated_img[orig_x, orig_y]

# Definir el ángulo de rotación (en grados) y convertirlo a radianes
angle = 45
theta = math.radians(angle)

# Rotar la imagen
for i in range(x):
    for j in range(y):
        new_x = int((j - cx) * math.cos(theta) - (i - cy) * math.sin(theta) + cx)
        new_y = int((j - cx) * math.sin(theta) + (i - cy) * math.cos(theta) + cy)
        if 0 <= new_x < y and 0 <= new_y < x:
            rotated_img[new_y, new_x] = img[i, j] # type: ignore

# Mostrar la imagen original y la trasladada
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Trasladada', translated_img)
cv.waitKey(0)
cv.destroyAllWindows()



### TAREA: TRASLADAR 20, ESCALAR A 1/5 Y ROTAR 45 ##### TRASLADAR 40, ROTAR 45 SENTIDO HORARIO Y ESCALA 2, ROTA 90 SENTIDO ANTIHORARIO