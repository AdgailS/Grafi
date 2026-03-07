# TAREAS GRAFICACIÓN
## Tarea 1. Imagen con puntillismo 
Mi idea principal fue hacer el dibujo de una flor de 5 petalos y para comenzar importé las librerías necesarias y cree la imagen de 500x500 pixeles

```
import numpy as np  
import cv2 as cv 

img = np.ones((500, 500, 3),  dtype=np.uint8)*255 
```
Despues cree una lista de diccionarios donde guardo las caracteristicas de cada uno de mis circulos. Para hacer esto dividí la imagen en 4 cuadrantes y fui calculando donde devería quedar cada uno, quedando "centro" con las coordenadas en x y en y.

```circulos = [
    {"centro": (258, 250), "radio": 50, "color": [0, 100, 200]},  # Café
    {"centro": (300, 185), "radio": 50, "color": [30, 200, 255]}, 
    {"centro": (330, 260), "radio": 50, "color": [30, 200, 255]},    
    {"centro": (270, 320), "radio": 50, "color": [30, 200, 255]},     
    {"centro": (185, 280), "radio": 50, "color": [30, 200, 255]}, 
    {"centro": (210, 190), "radio": 50, "color": [30, 200, 255]}   ] 
```
En los for se recorren los pixeles por fila y columna para ver cuales se van a pintar, dentro de estos se optienen los datos del círculo como las coordenadas del centro, la distancia del pixel del centro y el tamaño del círculo. Después, en el if utilizo la ecuación del circulo para ver si el pixel cumple la condición y está dentro del circulo.
```
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
```
Al final, como en todos los ejercicios solo se muestra la imagen.



## Tarea 2. Ejercicios de HSV con imagen de frutas 



## Tarea 3. Escalación de imagenes 
