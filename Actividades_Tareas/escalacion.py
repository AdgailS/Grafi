import math

import cv2 as cv
import numpy as np

# Cargar la imagen en escala de grises
img = cv.imread('Imagenes/tortuga.jpg', 0)

# Obtener el tamaño de la imagen
x, y = img.shape

# Crear una imagen vacía para la traslación
translated_img = np.zeros((x, y), dtype=np.uint8)

# Definir el desplazamiento en x e y
dx, dy = 100, 50

# Trasladar la imagen
for i in range(x):
    for j in range(y):
        new_x = i + 20
        new_y = j + 30
        if 0 <= new_x < x and 0 <= new_y < y:
            translated_img[new_x, new_y] = img[i, j]
            
xx, yy = rotated_img.shape # type: ignore
# Calcular el centro de la imagen
cx, cy = int(x  // 2), int(y  // 2)

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