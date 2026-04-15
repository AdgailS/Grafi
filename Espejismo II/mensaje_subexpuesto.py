import cv2
import numpy as np

img = cv2.imread("Imagenes/m1_oscura.png", cv2.IMREAD_GRAYSCALE)

# Convertir para evitar overflow
img_int = img.astype(np.int32)

# FASE 1
recuperado = np.clip(img_int * 50, 0, 255).astype(np.uint8)
cv2.imwrite("m1_recuperado_x50.png", recuperado)

# FASE 2
recuperado2 = np.clip(img_int * 50 + 20, 0, 255).astype(np.uint8)
cv2.imwrite("m1_recuperado_x50_mas20.png", recuperado2)