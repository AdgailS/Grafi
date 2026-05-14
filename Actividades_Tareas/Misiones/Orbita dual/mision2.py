import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import cv2
import numpy as np

# --- CONFIGURACIÓN ---
ORBIT_RADIUS = 5.0
ANGLE_SPEED = 1.0
USE_LIGHTING = True

# Estado global
angle = 0.0
modo_visualizacion = 3  # Por defecto en modo LookAt para Misión 2

def save_screenshot(filename):
    """Captura el frame actual y lo guarda en Orbita_Dual/"""
    width, height = 800, 600
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_BGR, GL_UNSIGNED_BYTE)
    image = np.frombuffer(data, dtype=np.uint8).reshape(height, width, 3)
    image = cv2.flip(image, 0)
    cv2.imwrite(f"Orbita_Dual/{filename}", image)
    print(f"Captura guardada: Orbita_Dual/{filename}")

def draw_sphere(radius, slices, stacks):
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)

def draw_scene():
    """Dibuja el mundo (ejes + objeto)"""
    glDisable(GL_LIGHTING)
    glBegin(GL_LINES)
    glColor3f(1, 0, 0); glVertex3f(0, 0, 0); glVertex3f(2, 0, 0) # X
    glColor3f(0, 1, 0); glVertex3f(0, 0, 0); glVertex3f(0, 2, 0) # Y
    glColor3f(0, 0, 1); glVertex3f(0, 0, 0); glVertex3f(0, 0, 2) # Z
    glEnd()
    
    if USE_LIGHTING:
        glEnable(GL_LIGHTING)
    
    glColor3f(0.5, 0.5, 0.9) # Esfera azulada
    draw_sphere(1.2, 32, 32)

def setup_lighting():
    if not USE_LIGHTING:
        glDisable(GL_LIGHTING)
        return
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])

def render_with_lookat(angle_deg):
    """
    MISIÓN 2: El Ojo Declarativo
    Usa gluLookAt para orbitar la cámara.
    Eje Y fijo, radio 5.
    """
    glLoadIdentity()
    
    # Convertir a radianes para math.cos/sin
    rad = math.radians(angle_deg)
    
    # Calcular posición del ojo (Eye) en órbita circular XZ
    eyeX = ORBIT_RADIUS * math.cos(rad)
    eyeZ = ORBIT_RADIUS * math.sin(rad)
    eyeY = 2.0  # Un poco de altura para mejor perspectiva (fija)
    
    # Objetivo (Center): Origen (0,0,0)
    # Arriba (Up): (0,1,0)
    gluLookAt(eyeX, eyeY, eyeZ,  # Dónde está la cámara
              0.0, 0.0, 0.0,     # A qué mira
              0.0, 1.0, 0.0)     # Qué dirección es "arriba"
    
    draw_scene()

def key_callback(window, key, scancode, action, mods):
    global modo_visualizacion, USE_LIGHTING
    if action == glfw.PRESS:
        if key == glfw.KEY_3:
            modo_visualizacion = 3
            print("Modo 3: gluLookAt Activo")
        elif key == glfw.KEY_L:
            USE_LIGHTING = not USE_LIGHTING
            print(f"Iluminación: {USE_LIGHTING}")
        elif key == glfw.KEY_S:
            if modo_visualizacion == 3:
                save_screenshot("m2_lookat_orbita.png")
        elif key in [glfw.KEY_ESCAPE, glfw.KEY_Q]:
            glfw.set_window_should_close(window, True)

def main():
    global angle
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Misión 2: Ojo Declarativo (gluLookAt)", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    print("--- MISIÓN 2: gluLookAt ---")
    print("Controles:")
    print("3: Activar renderizado con gluLookAt")
    print("S: Capturar 'm2_lookat_orbita.png'")
    print("L: Alternar luces")
    print("ESC/Q: Salir")

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        setup_lighting()
        
        if modo_visualizacion == 3:
            render_with_lookat(angle)
            
        angle += ANGLE_SPEED
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()