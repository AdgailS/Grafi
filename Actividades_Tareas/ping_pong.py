import cv2 as cv
import numpy as np

width, height = 500, 500

# INICIO EN EL CENTRO
x = 250
y = 250

# POSICINES X Y Y
dx = 4
dy = 3

radio = 20

while True:

    img = np.ones((height, width, 3), np.uint8) * 255

    # DIBUJAR PELOTA
    cv.circle(img, (x, y), radio, (0, 0, 255), -1)

    # MOVER PELOTA
    x = x + dx
    y = y + dy

    # PARA QUE REBOTE A LOS LADOS
    if x + radio >= width or x - radio <= 0:
        dx = -dx

    # PARA QUE REBOTE ARRIBA Y ABAJO
    if y + radio >= height or y - radio <= 0:
        dy = -dy

    cv.imshow("Ping Pong", img)

    if cv.waitKey(10) == 27:  # ESC para salir
        break

cv.destroyAllWindows()