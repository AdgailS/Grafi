import numpy as np  
import cv2 as cv 

# Crea una imagen de 500x500 píxeles
img = np.ones((500, 500, 3),  dtype=np.uint8)*255 


#Varios circulos (centro y petalos)
circulos = [
    {"centro": (258, 250), "radio": 50, "color": [0, 100, 200]},  # Café
    {"centro": (300, 185), "radio": 50, "color": [30, 200, 255]}, 
    {"centro": (330, 260), "radio": 50, "color": [30, 200, 255]},    
    {"centro": (270, 320), "radio": 50, "color": [30, 200, 255]},     
    {"centro": (185, 280), "radio": 50, "color": [30, 200, 255]}, 
    {"centro": (210, 190), "radio": 50, "color": [30, 200, 255]}  
]

for fila in range(500):
    for columna in range(500):
        for circulo in circulos:
            centro_x, centro_y = circulo["centro"]
            dx = columna - centro_x
            dy = fila - centro_y
            radio = circulo["radio"]
            
            if (dx*dx + dy*dy) < radio*radio:
                img[fila, columna] = circulo["color"]
                break  

cv.imshow('Flor', img)
cv.waitKey()
cv.destroyAllWindows()