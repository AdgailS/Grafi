# Actividades para alumnos (entregables)

## Actividad A — Medición del marcador
1. Mide el lado del cuadrado negro en cm.

2. Pon MARKER_LENGTH_M en metros.
3. Explica en 3 líneas qué pasa si pones el doble del valor real.

####  Respuesta: El programa creerá que el marcador es más grande de lo real, entonces el objeto 3D aparecerá más lejos o mal alineado respecto al marcador lo que hace que la posición y escala de la realidad aumentada  se vean incorrectas.

## Actividad B — Tetera vs esfera
1. Captura pantalla con la tetera y otra con la esfera (tecla T).

2. ¿Qué librería dibuja cada una? (GLUT vs GLU)
#### Resuesta: La esfera la dibuja GLU, la tetera no lo pude visualizar por el error 
```
OSError: exception: access violation reading 0x00000000000000C1
```


## Actividad C — Ejes OpenCV (solo visión, opcional)
1. Añade temporalmente en el bucle, antes de OpenGL, para ver ejes en una ventana OpenCV:

```
if corners is not None:
    rvec, tvec = estimate_pose(corners, camera_matrix, dist_coeffs)
    dbg = frame.copy()
    cv2.drawFrameAxes(dbg, camera_matrix, dist_coeffs, rvec, tvec, MARKER_LENGTH_M * 0.5)
    cv2.imshow("debug ejes", dbg)
    cv2.waitKey(1)
```
2. Compara: los ejes RGB deben coincidir con la orientación del objeto OpenGL.


## Actividad D — Calibración (mejora la alineación)
Si tienes tablero chessboard, calibra y guarda:

1. Esqueleto: tras calibrateCamera, guardar:

 np.savez("camera_ar.npz", camera_matrix=K dist_coeffs=dist, image_size=(w,h))

2. Coloca camera_ar.npz junto al .py. Sin archivo, el programa usa intrínsecos aproximados.