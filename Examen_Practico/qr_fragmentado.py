import cv2 as cv
import numpy as np

img1 = cv.imread('Imagenes/m2_mitad1.png', 0)
img2 = cv.imread('Imagenes/m2_mitad2.png', 0)

# 1. Crea lienzo de 400x400
lienzo = np.zeros((400,400), dtype=np.uint8)

h1, w1 = img1.shape
h2, w2 = img2.shape


## IMAGEN 1 ##
M1 = np.float32([
    [1,0,0],
    [0,1,0]
])

mitad1 = cv.warpAffine(img1, M1, (400,400))


# 2. Traslada la mitad 1 y pégala
lienzo[0:h1,0:w1] = mitad1[0:h1,0:w1]


## IMAGEN 2 ##
centro = (w2//2, h2//2)

M2 = cv.getRotationMatrix2D(centro,180,1)

mitad2_rotada = cv.warpAffine(img2, M2, (w2,h2))


# 3. Rota la mitad 2, trasládala y pégala
lienzo[200:400, 0:400] = mitad2_rotada


cv.imshow("QR reconstruido", lienzo)

cv.waitKey(0)
cv.destroyAllWindows()


