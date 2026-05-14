import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import cv2
import numpy as np

# --- CONFIGURACIÓN ---
CAM_DISTANCE = 5.0
ANGLE_SPEED = 1.0
USE_LIGHTING = True
LIGHT_FIXED_TO_CAMERA = True  # True: Luz sigue a la cámara, False: Luz fija en el mundo

# Estado global
angle = 0.0
modo_orbita = 1  # 1: Objeto Rota, 2: Cámara Orbita

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
    """Dibuja el objeto y los ejes"""
    glDisable(GL_LIGHTING)
    glBegin(GL_LINES)
    glColor3f(1, 0, 0); glVertex3f(0, 0, 0); glVertex3f(2, 0, 0)
    glColor3f(0, 1, 0); glVertex3f(0, 0, 0); glVertex3f(0, 2, 0)
    glColor3f(0, 0, 1); glVertex3f(0, 0, 0); glVertex3f(0, 0, 2)
    glEnd()
    
    if USE_LIGHTING:
        glEnable(GL_LIGHTING)
    
    glColor3f(0.8, 0.4, 0.1) # Objeto color arcilla para ver sombras
    draw_sphere(1.2, 32, 32)

def setup_lighting():
    """Configura la posición de la luz"""
    if not USE_LIGHTING:
        glDisable(GL_LIGHTING)
        return
        
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    
    # Si LIGHT_FIXED_TO_CAMERA es True, la luz se define ANTES de las transformaciones de vista.
    # Si es False, se debe llamar DESPUÉS de las transformaciones en el bucle principal (dentro de cada modo).
    if LIGHT_FIXED_TO_CAMERA:
        light_pos = [1.0, 1.0, 1.0, 0.0] # Luz direccional desde la esquina superior de la pantalla
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

def render_mode_1(angle):
    """MODO 1: El objeto rota. Luz fija a la cámara."""
    glLoadIdentity()
    # Luz definida aquí (antes de transformaciones) -> Sigue a la cámara
    setup_lighting()
    
    glTranslatef(0, 0, -CAM_DISTANCE)
    glRotatef(angle, 0, 1, 0)
    draw_scene()

def render_mode_2(angle):
    """MODO 2: La cámara orbita. Luz fija en el mundo."""
    glLoadIdentity()
    
    # Para que la luz sea "fija en el mundo", la definimos DESPUÉS de rotar/trasladar la cámara
    # pero ANTES de dibujar los objetos del mundo.
    glRotatef(-angle, 0, 1, 0)
    glTranslatef(0, 0, -CAM_DISTANCE)
    
    global LIGHT_FIXED_TO_CAMERA
    old_val = LIGHT_FIXED_TO_CAMERA
    LIGHT_FIXED_TO_CAMERA = False # Forzamos luz de mundo para este modo
    
    # Definimos luz en coordenadas de mundo (0,5,0 es arriba en el centro)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 5.0, 0.0, 1.0]) 
    setup_lighting()
    
    LIGHT_FIXED_TO_CAMERA = old_val
    draw_scene()

def key_callback(window, key, scancode, action, mods):
    global modo_orbita, USE_LIGHTING
    if action == glfw.PRESS:
        if key == glfw.KEY_1:
            modo_orbita = 1
            print("Modo 1: Objeto Rota (Luz fija a Cámara)")
        elif key == glfw.KEY_2:
            modo_orbita = 2
            print("Modo 2: Cámara Orbita (Luz fija al Mundo)")
        elif key == glfw.KEY_L:
            USE_LIGHTING = not USE_LIGHTING
            print(f"Luz: {USE_LIGHTING}")
        elif key == glfw.KEY_S:
            if modo_orbita == 1:
                save_screenshot("m3_luz_objeto.png")
            else:
                save_screenshot("m3_luz_camara.png")
        elif key in [glfw.KEY_ESCAPE, glfw.KEY_Q]:
            glfw.set_window_should_close(window, True)

def main():
    global angle
    if not glfw.init(): return
    window = glfw.create_window(800, 600, "Misión 3: Brújula de Luces", None, None)
    if not window: glfw.terminate(); return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.05, 0.05, 0.05, 1.0)

    print("--- MISIÓN 3 ---")
    print("1: Modo Objeto Rota (Luz 'pega' siempre igual)")
    print("2: Modo Cámara Orbita (Luz viene de un punto fijo en el espacio)")
    print("S: Capturar segun modo")
    print("ESC: Salir")

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        
        if modo_orbita == 1:
            render_mode_1(angle)
        else:
            render_mode_2(angle)
            
        angle += ANGLE_SPEED
        glfw.swap_buffers(window); glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()