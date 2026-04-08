import cv2 as cv
import numpy as np
import math


# Cargar la imagen
img_qr = cv.imread('Imagenes/qr_rotado.jpg', 0)
h, w = img_qr.shape

# ==========================================
# MÉTODO 1: MODO RAW (Trigonometría)
# ==========================================
# 1. Crea un lienzo vacío de 500x500


rotated_img = np.zeros((h*2, w*2), dtype=np.uint8)

#CENTRO ORIGINAL
cx = w // 2
cy = h // 2

#CENTRO NUEVO
cx2 = (w*2) // 2
cy2 = (h*2) // 2


# 2. Usa las fórmulas de senos y cosenos para mapear los píxeles (¡Cuidado con los huecos negros si mapeas hacia adelante!)

angle = -45
theta = math.radians(angle)

cos_t = math.cos(theta)
sin_t = math.sin(theta)

xx, yy = rotated_img.shape

for y_d in range(h*2):
    for x_d in range(w*2):
        x = x_d - cx2
        y = y_d - cy2
        
        x_src = x * cos_t - y * sin_t + cx
        y_src = x * sin_t + y * cos_t + cy

        x_src = int(x_src)
        y_src = int(y_src)

        if 0 <= x_src < w and 0 <= y_src < h:
            rotated_img[y_d, x_d] = img_qr[y_src, x_src]

cv.imshow("Original", img_qr)
cv.imshow("Imagen Rotada (modo raw)", rotated_img)

# ==========================================
# MÉTODO 2: MODO OPENCV
# ==========================================
# 1. Obtén la matriz con cv2.getRotationMatrix2D

alto, ancho = img_qr.shape[:2]

# DEFINIR CENTRO AGAIN
centro = (alto / 2, ancho / 2)

rotacion = cv.getRotationMatrix2D(center=centro, angle= -45, scale=1)

# 2. Aplica cv2.warpAffine
imagen_rotada = cv.warpAffine(img_qr, rotacion, (ancho, alto))


cv.imshow("Imagen rotada Open CV", imagen_rotada)

cv.waitKey(0)
cv.destroyAllWindows()
