## MISIONES 11 DE MARZO DEL 2026

### Misión 1: El artefacto desplazado (Traslación)

### La Historia

Nuestros satélites han captado la ubicación de un vehículo sospechoso en una imagen de 800x600 píxeles. Sin embargo, un error en los sensores del satélite desplazó la imagen. El vehículo, que debería estar en el centro exacto, está pegado a la esquina superior izquierda.

### Método 1
 Para hacer esto utilice el mismo codigo visto en clase y solo cambié los valores en x y y, así como crear el lienzo o imagen base de 600x800 

```
translated_img = np.zeros((600, 800), dtype=np.uint8)
dx = 300
dy = 200
```
Con eso ya nos queda la imagen en el centro.

### Método 2
Para hecer esto solo realicé la matriz de traslación M mostrada en los apuntes y cambié tx y ty por los valores que ya le había dado a dx y dy. 
```
M = np.float32([
    [1, 0, dx],
    [0, 1, dy]
])
translated = cv.warpAffine(img, M, (800, 600))
```
### Preguntas
¿Notaste alguna diferencia de tiempo al procesar la imagen píxel por píxel con ciclos for (Modo Raw) en comparación con la función cv2.warpAffine de OpenCV? 

Sí, el modo raw es más lento.

¿Por qué crees que tu código manual tarda mucho más en ejecutarse?

El modo raw es más lento porque se ejecuta cada iteración de los ciclos y con la función es todo más optimizado. 

