import cv2 as cv
import numpy as np

# ==========================================
# MÉTODO 1: MODO RAW (Manipulación de Píxeles)
# ==========================================

# Cargar imagen
img = cv.imread('Imagenes/vehiculo.jpg', 0)

# Obtener el tamaño de la imagen
h, w = img.shape

# Crear una imagen vacía para la traslación
# 1. Crea un lienzo negro vacío (np.zeros) de 600x800
translated_img = np.zeros((600, 800), dtype=np.uint8)

# Definir el desplazamiento en x e y /
# 2. Mueve los píxeles al nuevo lienzo sumando 300 en X y 200 en Y
dx = 300
dy = 200

# Trasladar la imagen
for i in range(h):
    for j in range(w):
        new_y = i + dy
        new_x = j + dx

        if 0 <= new_y < 600 and 0 <= new_x < 800:
            translated_img[new_y, new_x] = img[i, j]


# Mostrar la imagen original y la trasladada
cv.imshow("Original", img)
cv.imshow("Trasladada RAW", translated_img)

# ==========================================
# MÉTODO 2: MODO OPENCV (Matriz de Transformación)
# ==========================================
# 1. Crea la matriz de traslación 'M' en NumPy

M = np.float32([
    [1, 0, dx],
    [0, 1, dy]
])

# 2. Aplica cv2.warpAffine a la imagen original
translated = cv.warpAffine(img, M, (800, 600))

cv.imshow("Traslacion OpenCV", translated)
cv.waitKey(0)
cv.destroyAllWindows()




