import cv2
import numpy as np

# Leer imagen
img = cv2.imread('Imagenes/frutas.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Rangos de colores
colores = {
    "Rojo": [([0,100,100], [10,255,255]), ([160,100,100], [179,255,255])],
    "Verde": [([35,100,100], [85,255,255])],
    "Amarillo": [([20,100,100], [30,255,255])]
}

print("\n" + "="*50)
print(f"{'Color':<12} {'Regiones':<12} {'Observación'}")
print("="*50)

for nombre, rangos in colores.items():
    # Crear máscara del color
    mascara = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for bajo, alto in rangos:
        mascara |= cv2.inRange(hsv, np.array(bajo), np.array(alto))
    
    # Limpiar ruido
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    
    # Contar regiones (componentes conectados)
    num, _, stats, _ = cv2.connectedComponentsWithStats(mascara, connectivity=8)
    
    # Contar regiones con área >= 500
    regiones = sum(1 for i in range(1, num) if stats[i, cv2.CC_STAT_AREA] >= 500)
    
    # Determinar observación
    if regiones == 0:
        obs = "Sin regiones"
    elif regiones == 1:
        obs = "Una región estable"
    else:
        obs = f"{regiones} regiones detectadas"
    
    print(f"{nombre:<12} {regiones:<12} {obs}")

print("="*50)

# Mostrar imágenes
cv2.waitKey(0)
cv2.destroyAllWindows()