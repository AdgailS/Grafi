import cv2
import numpy as np

# Leer la imagen
img = cv2.imread('frutas.png')

# Convertir la imagen al espacio de color HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


# Definir el rango inferior y superior para detectar verde
lower_yellow = np.array([35, 100, 100])  # Hue, Saturación, Brillo mínimos
upper_yellow = np.array([85, 255, 255])  # Hue, Saturación, Brillo máximos

# Crear una máscara que solo incluya los píxeles dentro del rango
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

# Aplicar la máscara a la imagen original
result = cv2.bitwise_and(img, img, mask=mask) #SE TRABAJA CON LA MASCARA

# Mostrar la imagen original y la imagen con el color detectado
cv2.imshow("Imagen Original", img)
cv2.imshow("Color Detectado", result)
cv2.imshow("Mascara", mask)
cv2.imshow("Img HSV", hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()