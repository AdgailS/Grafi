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


## Tarea 4. Animación con ecuaciones paramétricas 
Para generar esta animación solo tomé como base el codigo que nos había proporcionado en los apuntes y busqué imagenes el google con los dibujos que se podrían realizar, donde encontré los datos para realizar el espirar y las flores, a las cuales solo les cambié los valores de a, b y k para realizar distintos tamaños y cambiar la cantidad de petalos. 

```
mg = np.ones((height, width, 3), dtype=np.uint8)*255

# centro
center_x, center_y = width // 2, height // 2

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

```

Para realizar todas las animaciones en una sola imagen saqué el centro de la imagen para que puedan partir desde ahí y en un bucle while y dentro de este puse un for para cada ecuación.
```
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
```
### Tarea 5. Dibujo con ecuaciones paramétricas
Como dibujo decidí hacer el contorno de un pollito (me arrepentí), para el cual usé solo lineas y un circulo para el ojo. Mi trabajo principan fue dividir la imagen como una cuadrilla para saber donde iniciaba y terminba cada punto e ir uniendolos.
```
import numpy as np
import cv2 as cv

img = np.ones((400,400,3), dtype=np.uint8)*255


# CUERPO
cv.line(img,(100,300),(300,300),(0,0,0),2) 
cv.line(img,(300,300),(340,270),(0,0,0),2) 
cv.line(img,(340,270),(340,180),(0,0,0),2) 
cv.line(img,(340,180),(300,210),(0,0,0),2) 
cv.line(img,(300,210),(260,180),(0,0,0),2)   
cv.line(img,(260,180),(180,180),(0,0,0),2) 
cv.line(img,(180,180),(220,150),(0,0,0),2) 
cv.line(img,(220,150),(180,90),(0,0,0),2) #8
cv.line(img,(180,90),(100,90),(0,0,0),2) 
cv.line(img,(100,90),(60,120),(0,0,0),2) 
cv.line(img,(60,120),(20,135),(0,0,0),2) 
cv.line(img,(20,135),(60,150),(0,0,0),2) 
cv.line(img,(60,150),(100,180),(0,0,0),2) #13
cv.line(img,(100,180),(60,210),(0,0,0),2) 
cv.line(img,(60,210),(60,270),(0,0,0),2) 
cv.line(img,(60,270),(100,300),(0,0,0),2) 
cv.line(img,(60,120),(60,150),(0,0,0),2) 

cv.circle(img,(100,135),10,(0,0,0),-1) # OJO

#PATAS
cv.line(img,(140,300),(140,360),(0,0,0),2)
cv.line(img,(140,360),(100,360),(0,0,0),2) 
cv.line(img,(220,300),(220,360),(0,0,0),2) 
cv.line(img,(220,360),(260,360),(0,0,0),2) 

#ALA
cv.line(img,(140,210),(140,240),(0,0,0),2) 
cv.line(img,(140,240),(180,270),(0,0,0),2) 
cv.line(img,(180,270),(260,270),(0,0,0),2) 
cv.line(img,(260,270),(300,240),(0,0,0),2) 
cv.line(img,(300,240),(260,210),(0,0,0),2) 
cv.line(img,(260,210),(220,210),(0,0,0),2) 

cv.imshow("Pollo",img)
cv.waitKey(0)
cv.destroyAllWindows()
```


### Tarea 6. Ping Pong 
La idea del ejercicio era hacer que la pelota se mueva en (x,y) y que cuando se toque una pared se invierta la dirección para dar la ilusión de que rebota.
Primero definí la posicion inicial para que sea el centro (x,y), la velocidad para cada uno (dx,dy) y el tamaño de la pelota
```
x = 250
y = 250

dx = 4
dy = 3

radio = 20

```
Despues para el rebote hice dx =  dx para horizontal y  dy = −dy para vertical y los puse dentro de los if que sirven para saber cuando la pelota llega a uno de los bordes. 
```
while True:

    img = np.ones((height, width, 3), np.uint8) * 255

    cv.circle(img, (x, y), radio, (0, 0, 255), -1)

    x = x + dx
    y = y + dy

    if x + radio >= width or x - radio <= 0:
        dx = -dx

    if y + radio >= height or y - radio <= 0:
        dy = -dy

    cv.imshow("Ping Pong", img)
```


### Tarea 7. Filtro con nariz, orejas, cejas y bigote 

En base al codigo de ejemplo y siguiendo las mismas instrucciones agregué solo distintos elemtos para cada parte de la cara que queriá representar, usando lineas para las cejas, una elipse completa (-1) para la nariz, dos rin relleno para el bigote y otras dos rellenas para las orejas.

```     # CEJAS
        img = cv.line(img, (x + int(w*0.2), y + int(h*0.20)), (x + int(w*0.4), y + int(h*0.20)), (0,0,0), 3) #izquierda
        img = cv.line(img, (x + int(w*0.6), y + int(h*0.20)), (x + int(w*0.8), y + int(h*0.20)), (0,0,0), 3) #derecha
        # NARIZ
        cv.ellipse(img, (x + int(w*0.5), y + int(h*0.55)), (12,18), 0, 0, 360, (0,0,255), -1)
        # BIGOTE 
        cv.ellipse(img, (x + int(w*0.45), y + int(h*0.70)), (20,8), 0, 0, 180, (0,0,0), 3)
        cv.ellipse(img, (x + int(w*0.55), y + int(h*0.70)), (20,8), 0, 0, 180, (0,0,0), 3)
        # OREJA IZQUIERDA
        cv.ellipse(img, (x - 15, y + int(h*0.5)), (25,40), 0, 0, 360, (150,180,255), -1)
        # OREJA DERECHA
        cv.ellipse(img, (x + w + 15, y + int(h*0.5)), (25,40), 0, 0, 360, (150,180,255), -1)
```

