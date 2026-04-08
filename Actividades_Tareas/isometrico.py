import cv2 as cv
import numpy as np
import math

def dibujar_casa(angulo_vista_grados, profundidad=120):
    casa = np.ones((600, 600, 3), dtype=np.uint8) * 255
    
    angulo_rad = math.radians(angulo_vista_grados)
    dx = int(profundidad * math.cos(angulo_rad))
    dy = int(profundidad * math.sin(angulo_rad))
    
    A = (200, 400)  
    B = (320, 400) 
    C = (320, 280)  
    D = (200, 280)  
    Pico_F = (260, 200) 
    
    E = (A[0] + dx, A[1] - dy)
    F = (B[0] + dx, B[1] - dy)
    G = (C[0] + dx, C[1] - dy)
    H = (D[0] + dx, D[1] - dy)
    Pico_T = (Pico_F[0] + dx, Pico_F[1] - dy)
    
    color_pared_frontal = (200, 180, 100)
    color_pared_lateral = (180, 160, 80)
    color_techo = (0, 155, 200)
    
    pts_frontal = np.array([A, B, C, D, Pico_F], np.int32)
    cv.fillPoly(casa, [pts_frontal], color_pared_frontal)
    
    pts_lateral = np.array([B, F, G, C], np.int32)
    cv.fillPoly(casa, [pts_lateral], color_pared_lateral)
    
    pts_techo = np.array([D, C, Pico_F], np.int32)
    cv.fillPoly(casa, [pts_techo], color_techo)
    
    pts_techo_lat = np.array([C, G, Pico_T, Pico_F], np.int32)
    cv.fillPoly(casa, [pts_techo_lat], color_techo)
    
    grosor = 2
    color_linea = (50, 50, 50)
    
    for inicio, fin in [(A,E), (B,F), (C,G), (D,H)]:
        cv.line(casa, inicio, fin, color_linea, grosor)
    
    for inicio, fin in [(E,F), (F,G), (G,H), (H,E)]:
        cv.line(casa, inicio, fin, color_linea, grosor)
    
    for inicio, fin in [(A,B), (B,C), (C,D), (D,A), (D,Pico_F), (C,Pico_F)]:
        cv.line(casa, inicio, fin, color_linea, grosor)
    
    cv.line(casa, H, Pico_T, color_linea, grosor)
    cv.line(casa, G, Pico_T, color_linea, grosor)
    cv.line(casa, Pico_F, Pico_T, color_linea, grosor)
    
    return casa

# Animaciòn
for ang in range(10, 71, 5):
    casa_anim = dibujar_casa(ang)
    cv.imshow('Animación - Cambiando enfoque', casa_anim)
    cv.waitKey(200) 

cv.destroyAllWindows()