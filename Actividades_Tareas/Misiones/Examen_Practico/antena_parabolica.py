import cv2
import numpy as np
import math

imagen = np.zeros((500,500,3), dtype=np.uint8)

t = 0

while t <= 2*math.pi:

    x = int(250 + 150 * math.sin(3*t))
    y = int(250 + 150 * math.sin(2*t))

    cv2.circle(imagen, (x,y), 1, (0,0,150), -1)

    t += 0.01

cv2.imshow("Recorrido", imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()