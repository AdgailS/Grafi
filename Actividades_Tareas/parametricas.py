import numpy as np
import cv2

#  parámetros iniciales
width, height = 1000, 1000
img = np.ones((height, width, 3), dtype=np.uint8)*255

# centro
center_x, center_y = width // 2, height // 2

# Parámetros 

# rojo
a1, b1 = 150, 100
k1 = 4

# verde
a2 = 5

# azul
a3, b3 = 120, 120
k3 = 5

# amarillo
a4 = 150
n = 4  # num petalos

theta_increment = 0.03
max_theta = 2 * np.pi

theta = 0

while True:
  
    # Rojo
    for t in np.arange(0, theta, theta_increment):
        r = a1 + b1 * np.cos(k1 * t)
        x = int(center_x + r * np.cos(t))
        y = int(center_y + r * np.sin(t))
        cv2.circle(img, (x, y), 2, (0, 0, 255), -1)
    
    # Verde
    for t in np.arange(0, theta * 2, theta_increment):
        r = a2 * t
        x = int(center_x + r * np.cos(t))
        y = int(center_y + r * np.sin(t))
        cv2.circle(img, (x, y), 2, (0, 255, 0), -1)
    
    # Azul
    for t in np.arange(0, theta, theta_increment):
        r = a3 + b3 * np.cos(k3 * t)
        x = int(center_x + r * np.cos(t))
        y = int(center_y + r * np.sin(t))
        cv2.circle(img, (x, y), 2, (255, 0, 0), -1)
    
    # Amarillo
    for t in np.arange(0, theta, theta_increment):
        r = a4 * np.cos(n * t)
        x = int(center_x + r * np.cos(t))
        y = int(center_y + r * np.sin(t))
        cv2.circle(img, (x, y), 2, (0, 255, 255), -1)
    
    # Mostrar la imagen
    cv2.imshow("4 Curvas Parametricas", img)
    
    
    theta += theta_increment
  
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Para salir con ESC ?????????
    if cv2.waitKey(5) & 0xFF == 27:
        break

cv2.destroyAllWindows()