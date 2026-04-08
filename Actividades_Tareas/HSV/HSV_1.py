import cv2
import numpy as np

img = cv2.imread('Imagenes/frutas.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
kernel = np.ones((5,5), np.uint8)


lower_green = np.array([25, 100, 100])  
upper_green = np.array([35, 255, 255]) 

mascara = cv2.inRange(hsv, lower_green, upper_green)

resultado = cv2.bitwise_and(img, img, mask=mascara)

cv2.imshow("Imagen Original", img)
cv2.imshow("Color Detectado", resultado)
cv2.imshow("Img Blanco y Negro", mascara)
cv2.waitKey(0)
cv2.destroyAllWindows()