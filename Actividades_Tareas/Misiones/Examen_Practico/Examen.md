#  Reporte de Misión: Graficación Táctica
**Agente Especial:** Sánchez Hernández Estrella Abigail NC.24120345

---
#  Evidencias de Misión
## Mision 1. El Mensaje Subexpuesto
La idea de esta mision era descubrir el mensaje oculto usando operadores de división, para lo que hice: 
```
for y in range(h):
    for x in range(w):  
            pixel_original = img[y,x]
            nuevo_valor = int(pixel_original)*50
            img_final[y,x] = np.clip(nuevo_valor,0,255)
           

cv2.imshow('Original', img)
cv2.imshow('Revelada', img_final)

```
Dos for anidados que recorran los pixeles uno a uno y obtengan su valor en escala de grises, para que después estos mismos los multiplique por 50 y podamos tener un color mas cerca del blanco y por tanto más claro. 
```
img_final_CV = img * 50
img_final_CV = np.clip(img_final_CV, 0, 255).astype(np.uint8)

cv2.imshow('Con OPENCV', img_final_CV)
```
Usando OPENCV la lógica es la misma, solo que aprovehcando las ventajas que nos da la llibrería. 

![Evidencia misión 1](Imagenes/m1.png)

# Misión 2. El QR Fragmentado 
La idea en este ejercico es reacomodar y formar de nuevo la imagen que fue dividida, para lo que utilicé la matriz de transformacion y con warpAffine coloque la imagen 1 en el lienzo y después apliqué el cambio a modo de que aparezca en el centro. 

```
## IMAGEN 1 ##
M1 = np.float32([
    [1,0,0],
    [0,1,0]
])

mitad1 = cv.warpAffine(img1, M1, (400,400))

# 2. Traslada la mitad 1 y pégala
lienzo[0:h1,0:w1] = mitad1[0:h1,0:w1]
```
Para la imagen dos se crea la matriz de rotacion y se le dan los parametros necesarios, como el centro de la imagen y el angulo de rotación, después usando de nuevo warpAffine se coloca la imagen en nuestro lienzo y el qr queda compelto.

```
## IMAGEN 2 ##
centro = (w2//2, h2//2)

M2 = cv.getRotationMatrix2D(centro,180,1)

mitad2_rotada = cv.warpAffine(img2, M2, (w2,h2))


# 3. Rota la mitad 2, trasládala y pégala
lienzo[200:400, 0:400] = mitad2_rotada
```
![Evidencia misión 2](Imagenes/m2.png)

# Misión 3. El Sello Biométrico
Este ejercicio fue un poco mas sencillo, pues solo se necesitaba crear nuestro lienzo y dibujar sobre él siguiendo las indicaciones de posición. 
```
lienzo = np.zeros((500,500,3), dtype=np.uint8)
lienzo[:] = (50,20,20)   

cv.circle(lienzo, (250,250), 100, (0,255,255), 3)

cv.rectangle(lienzo, (200,200), (300,300), (0,0,255), -1)

cv.line(lienzo, (0,0), (500,500), (255,255,255), 2)
cv.line(lienzo, (0,500), (500,0), (255,255,255), 2)

```
![Evidencia misión 3](Imagenes/m3.png)

# Misión 4. La Frecuencia Térmica 
Para este ejercicio se tenían que aislar los pixeles color cyan para eliminar el ruido en la imagen y poder acceder al mensaje. Lo que hice fue cambiar la imagen al modelo HSV y configurar los rangos dados en el ejercicio, después cree la mascara y usé un kernel para eliminar el ruido.
```
img = cv2.imread('Imagenes/m4_ruido.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

rango_bajo = np.array([80,100,100])
rango_alto = np.array([100,255,255])

mascara = cv2.inRange(hsv, rango_bajo, rango_alto)

kernel = np.ones((3,3), np.uint8)
mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
```
![Evidencia misión 4](Imagenes/m4.png)


# Misión 5. La Antena Parabólica
La idea era dibujar con ecuaciones parametricas el recorrido necesario de un láser para disparar a una antena enemiga. Usando codigo visto en los apuntes y cambiando solo algunos valores logré programar este recorrido: 

```
imagen = np.zeros((500,500,3), dtype=np.uint8)

t = 0

while t <= 2*math.pi:

    x = int(250 + 150 * math.sin(3*t))
    y = int(250 + 150 * math.sin(2*t))

    cv2.circle(imagen, (x,y), 1, (0,0,150), -1)

    t += 0.01
```
![Evidencia misión 5](Imagenes/m5.png)

---
# Análisis del Analista (Reflexiones Finales)

1. **Sobre los Operadores Puntuales (Misión 1):** Matemáticamente, ¿qué pasaría si en lugar de multiplicar por 50, hubieras sumado 50 a cada píxel oscuro? ¿Se revelaría el texto igual de claro o la imagen perdería contraste?
> *Se lograría aclarar la imagen, pero sería muy poco en comparación a si se multiplica lo que causaría que no se distinga correctamente el mensaje*

2. **Sobre el Espacio HSV (Misión 4):** ¿Por qué el modelo de color BGR es ineficiente para la Recuperación de Información cuando buscamos "todos los tonos de azul celeste", y por qué el modelo HSV resuelve este problema con una sola variable?
> *Porque HSV separa las distintas formas del color como saturación, brillo y tipo de color*

3. **Sobre Ecuaciones Paramétricas (Misión 5):** ¿Por qué las ecuaciones paramétricas (usando el parámetro t) son mejores para dibujar formas cerradas y complejas en graficación por computadora que usar la clásica función $y=f(x)$?
> *Porque permiten expresar las coordenadas x e y con un mismo parámetro t y con la función clásica cada valor de x solo tiene un valor de y.*