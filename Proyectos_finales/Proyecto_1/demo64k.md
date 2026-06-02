# Reporte de Proyecto Final: Demo de Animación y Geometría Procedural
**Estudiante:** Estrella Abigail  
**Materia:** Graficación / Visión por Computadora  
**Institución:** Instituto Tecnológico de Morelia  

---

## 1. Descripción del Proyecto
Para este proyecto se utilizaron las herramientas y conceptos vistos en clase con el objetivo de crear una demo de animación procedural de **60 segundos exactos a 30 FPS** (1800 cuadros en total). Toda la propuesta visual se genera en tiempo real frame a frame mediante código puro, utilizando las librerías `OpenCV` y `NumPy`. El script calcula matemáticamente las posiciones, tamaños y colores de cada elemento geométrico sin depender de imágenes o archivos de video externos.

---

## 2. Línea de Tiempo y Estructura de Escenas
El contenido del video está estructurado en 6 bloques de 10 segundos cada uno, controlados de forma exacta por una función central:

* **Escena 1: Introducción (`scene_credits`) [00s - 10s]:** Escena de presentación del proyecto con un fondo que cambia de color de forma suave (gradiente en el espacio de color HSV) y elementos en movimiento como estrellas titilantes y círculos concéntricos que se expanden mediante un ritmo senoidal controlado por el tiempo.

* **Escena 2: Lotus Orbital (`scene_lotus`) [10s - 20s]:** Curva geométrica compuesta por 20 pétalos circulares. Se aplicaron fórmulas de conversión de coordenadas polares a cartesianas para su distribución angular uniforme, añadiendo una modulación armónica que hace que el radio base experimente un efecto de latido o pulsación.

* **Escena 3: Rosa Polar (`scene_rose_polar`) [20s - 30s]:** Composición basada en una flor polar de 8 ejes con rotación angular constante sobre su propio centro. Se complementa con un anillo exterior dinámico formado por partículas que describen un movimiento oscilatorio periódico para simular un comportamiento ondulatorio.

* **Escena 4: Espirógrafo y Ondas (`scene_spirograph`) [30s - 40s]:** Simulación procedural de un sistema de espirógrafo clásico con ruedas concéntricas interconectadas y una estrella perimetral de 8 puntas que se deforma de acuerdo con el tiempo. En las cuatro esquinas de la pantalla aparecen círculos expansivos que simulan ondas de choque.

* **Escena 5: Campo Glitch de Primitivas (`scene_glitch`) [40s - 50s]:** En esta escena se generan múltiples figuras geométricas (círculos, cuadrados, triángulos y cruces) de tamaño reducido y dispersas por toda la pantalla de forma caótica. Las figuras aparecen fijas en un punto, se mantienen estáticas y, en su fase final, parpadean rápidamente y sufren un pequeño salto de píxeles en el eje horizontal para recrear un efecto de interferencia digital o *glitch*.

* **Escena 6: Composición Elíptica Final (`scene_final`) [50s - 60s]:** Flor central compuesta por 6 elipses rotadas a 60 grados, rodeada por un anillo exterior discontinuo de alta luminosidad y mini flores de encuadre en las esquinas. Al renderizado completo de la pantalla se le aplica una deformación elástica lateral de vaivén.

---

## 3. Implementación de Herramientas Vistas en Clase

### A. Transformaciones Matriciales Afines
De acuerdo con los temas de transformaciones bidimensionales analizados en el curso, se implementaron matrices de transformación de tamaño $2\times3$ procesadas a través de la función `cv2.warpAffine()`:

* **Rotación:** Aplicada para generar el giro controlado de las estructuras alrededor del centro de la pantalla.

* **Sesgo o Corte (Shear):** Utilizado en la escena final para desplazar horizontalmente los píxeles de la imagen en función de su coordenada vertical, logrando una distorsión elástica mediante la matriz:
$$\begin{bmatrix} 1 & factor \cdot \sin(t) & 0 \\ 0 & 1 & 0 \end{bmatrix}$$

* **Efecto Estela:** Se utilizó la función `cv2.addWeighted()` para promediar de manera acumulativa el frame original con su versión transformada, generando un efecto visual de persistencia o sombra en movimiento.

### B. Pipeline de Post-Procesado y Filtros
Una vez construida la geometría básica de cada frame, la imagen pasa por un proceso de filtrado secuencial para modificar su estética final:

1. **Máscara de Viñeta:** Se calcula la distancia cuadrática de los píxeles hacia el centro para reducir progresivamente la luminosidad en los bordes de la pantalla.

2. **Líneas de Escaneo (Scanlines):** Una función senoidal vertical altera el brillo fila por fila para emular la textura de los monitores CRT antiguos.

3. **Posterización:** Se reduce la paleta continua de colores dividiendo los canales de color en bloques discretos a través de operaciones enteras en NumPy, logrando un acabado estilo retro de 16 bits.

### C. Transiciones y Control Temporal
Para asegurar un flujo continuo y profesional entre las distintas etapas de la animación, se programaron los siguientes algoritmos de control:

* **Interpolación Cúbica (Smoothstep):** Utilizada para suavizar la aceleración y desaceleración de las escalas y los desvanecimientos.

* **Mezcla Cruzada (Crossfade):** En los últimos 0.5 segundos de cada bloque de tiempo, el código fusiona linealmente la escena saliente con la entrante.

* **Destello controlado (Flash):** Se añade un pico de luminancia blanca en el instante exacto del cambio de escena para ocultar la transición de forma dinámica.

* **Fundidos Globales (Fade-In / Fade-Out):** Transiciones de entrada y salida desde negro absoluto en los extremos del timeline general (primeros y últimos 1.5 segundos).

---
