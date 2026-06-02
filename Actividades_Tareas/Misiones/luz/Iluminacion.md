#  Análisis Comparativo: Iluminación, Normales y Materiales en OpenGL

Este documento detalla cómo cada uno de los archivos de código fuente aborda, resuelve o expande los requerimientos y checkpoints de la misión del Ojo 3D (luces, normales, materiales y transformaciones matriciales).

---

##  1. `antes_de_material.py`
**Estado:** *Incompleto / Punto de partida con errores de configuración.*

Este archivo representa el intento inicial de activar la iluminación antes de implementar el sistema de materiales personalizados.

* **Misión 1 (Activación de luces):** Activa correctamente los estados globales `GL_LIGHTING`, `GL_LIGHT0` y `GL_DEPTH_TEST`. Sin embargo, presenta un **error crítico** de sintaxis en la configuración:
    ```python
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_position[3])
    ```
    La función `glLightfv` espera un vector o arreglo de 4 valores (RGBA) para el color especular. Al pasarle únicamente un flotante indexado (`light_position[3]`, que vale `0.2`), el programa genera un fallo de segmentación o un comportamiento indefinido en el render.

* **Misión 2 (Normales):** Cumple con la misión de habilitar `gluQuadricNormals(quad, GLU_SMOOTH)` dentro de `draw_sphere()`. Esto le indica a GLU que calcule los vectores normales de la geometría de forma interpolada para que la luz no se vea facetada.

* **Misión 3 y 4 (Enfoque de color):** Activa `GL_COLOR_MATERIAL`. Intenta usar los comandos `glColor3f()` originales del ojo para definir los componentes difuso y ambiente bajo la luz, pero carece de brillo especular dinámico por cada capa.

---

## 2. `iluminacion1.py`

Este script es la implementación más avanzada en cuanto al manejo manual y detallado de componentes ópticas individuales, controlando la luz desde la perspectiva del objeto.

* **Uso estricto de Materiales (Misión 3):** A diferencia de usar el color del vértice, este archivo **deshabilita** `GL_COLOR_MATERIAL` en `setup_lighting()`. Define una función matemática/gráfica pura llamada `set_material()` que configura los cuatro componentes esenciales del pipeline fijo por cada esfera: `GL_AMBIENT`, `GL_DIFFUSE`, `GL_SPECULAR` y `GL_SHININESS`.

* **Diferenciación de texturas:** Consigue el comportamiento físico requerido mediante el parámetro de rugosidad (*shininess*):
    * **Esclerótica (Blanco):** `shininess=80` (Brillo pulido/fuerte de aspecto húmedo).
    * **Iris y Piel:** `shininess=32` (Brillo plástico/moderado estándar).
    * **Pupila:** `shininess=8` (Superficie mate que absorbe la luz casi por completo).

* **Posicionamiento de la luz (Misión 5 - Opción B):** La línea `glLightfv(GL_LIGHT0, GL_POSITION, light_position)` se ejecuta **después** de `glRotatef(rotation, 0, 1, 0)`.
    > **Efecto visual:** La luz rota solidaria junto con el ojo. Al girar la escena, el brillo especular (el punto blanco reflejado) se queda "pegado" en la misma zona de la esfera porque la fuente de luz se mueve al mismo tiempo que el objeto.

---

##  3. `luz_windows.py` y `luz_para_windows.py`*

Ambos archivos son idénticos en su lógica de iluminación, pero `luz_windows.py` es una versión optimizada que elimina por completo la dependencia de `GLUT` (reemplazándola con `GLU`), volviéndolo un entorno seguro para sistemas Windows sin librerías externas complejas.

Estos archivos expanden la **Misión 5** y el **Bonus** mediante un menú interactivo por teclado (teclas `0` a `4`) para alternar la naturaleza de la luz:

* **Modo 0 (Básica):** Cumple con la configuración estándar de componentes difusas y ambientales balanceadas.
* **Modo 1 (Múltiple - Requisito del Bonus):** Configura tres luces simultáneas (`LIGHT0`, `LIGHT1` y `LIGHT2`) con diferentes posiciones y colores (tonos cálidos y fríos) para eliminar las sombras totalmente negras de los costados del ojo, revelando el volumen oculto.
* **Modo 2 (Direccional):** Muestra el uso de un vector infinito utilizando un componente de posición $w = 0.0$. La luz ya no actúa como un punto local, sino como una **dirección de rayos paralelos** (idéntico a la luz del sol).
* **Modo 3 (Spotlight):** Agrega las funciones de cono de atenuación (`GL_SPOT_CUTOFF` y `GL_SPOT_EXPONENT`) creando un efecto de "linterna" o reflector cónico sobre el ojo.
* **Modo 4 (Colores):** Asigna vectores RGB puros a tres fuentes distintas (Rojo, Verde y Azul), demostrando cómo interactúan las luces de colores sobre materiales con `GL_COLOR_MATERIAL` activo.

---

## 4. `varios_ojos.py`

Este archivo no profundiza en nuevos parámetros de materiales (reutiliza una iluminación ambiental básica combinada con `GL_COLOR_MATERIAL`), sino que se enfoca en el control avanzado de la matriz `MODELVIEW` mediante la clonación de geometrías.

* **Multiplicación de Matrices:** Utiliza bucles anidados (`for`) y funciones trigonométricas (`math.cos`, `math.sin`) para clonar el modelo del ojo en patrones complejos: una cuadrícula de $3 \times 3$, un anillo perimetral estilo araña, y una **estructura floral con tres anillos concéntricos** (8, 12 y 16 ojos respectivamente).
* **Comportamiento lumínico en arreglos:** Al mantener una sola luz estática (`light_position` fija en el espacio), cada ojo clonado en el patrón recibe el ángulo de luz de manera distinta dependiendo de su coordenada de traslación en la pantalla. Esto genera un contraste orgánico donde unos ojos muestran brillos especulares intensos mientras que otros quedan en penumbra de acuerdo a su cercanía con la fuente.