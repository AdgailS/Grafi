import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import sys

window = None

# --- VARIABLES GLOBALES DE LA CÁMARA ---
cam_x = 0.0
cam_y = 8.0   # Altura media
cam_z = 25.0  # Empezamos lejos para ver el vecindario
fov = 60.0    # Field of View (Campo de visión para el ZOOM)

def init():
    glClearColor(0.5, 0.8, 1.0, 1.0) # Cielo azul
    glEnable(GL_DEPTH_TEST)

def procesar_teclado(window):
    """Escanea las teclas para moverse y hacer zoom"""
    global cam_x, cam_y, cam_z, fov
    velocidad_movimiento = 0.3
    velocidad_zoom = 1.0
    
    # Moverse en el plano (Caminar)
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        cam_z -= velocidad_movimiento
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        cam_z += velocidad_movimiento
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        cam_x -= velocidad_movimiento
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        cam_x += velocidad_movimiento
        
    # Volar (Elevarse o descender)
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        cam_y += velocidad_movimiento
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        cam_y -= velocidad_movimiento

    # ZOOM ÓPTICO (Modificar el FOV)
    if glfw.get_key(window, glfw.KEY_Z) == glfw.PRESS:
        fov -= velocidad_zoom # Zoom IN (reduce el campo de visión)
        if fov < 10.0: fov = 10.0 # Límite máximo de zoom
    if glfw.get_key(window, glfw.KEY_X) == glfw.PRESS:
        fov += velocidad_zoom # Zoom OUT (amplía el campo de visión)
        if fov > 120.0: fov = 120.0 # Límite de gran angular

def draw_cube():
    """Paredes de la casa"""
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.7, 0.6)  # Color beige/crema para las paredes
    # Frente
    glVertex3f(-1, 0, 1); glVertex3f(1, 0, 1); glVertex3f(1, 1.5, 1); glVertex3f(-1, 1.5, 1)
    # Atrás
    glVertex3f(-1, 0, -1); glVertex3f(1, 0, -1); glVertex3f(1, 1.5, -1); glVertex3f(-1, 1.5, -1)
    # Izquierda
    glVertex3f(-1, 0, -1); glVertex3f(-1, 0, 1); glVertex3f(-1, 1.5, 1); glVertex3f(-1, 1.5, -1)
    # Derecha
    glVertex3f(1, 0, -1); glVertex3f(1, 0, 1); glVertex3f(1, 1.5, 1); glVertex3f(1, 1.5, -1)
    glEnd()

def draw_details():
    """Agrega puertas y ventanas"""
    glBegin(GL_QUADS)
    # Puerta (Madera oscura) en la derecha
    glColor3f(0.4, 0.2, 0.1)
    glVertex3f(0.2, 0, 1.01); glVertex3f(0.7, 0, 1.01)
    glVertex3f(0.7, 1.0, 1.01); glVertex3f(0.2, 1.0, 1.01)

    # Ventana (Celeste) en la izquierda
    glColor3f(0.6, 0.8, 0.9)
    glVertex3f(-0.7, 0.5, 1.01); glVertex3f(-0.2, 0.5, 1.01)
    glVertex3f(-0.2, 1.0, 1.01); glVertex3f(-0.7, 1.0, 1.01)
    glEnd()
    
    # Marcos de la ventana (Cruces negras)
    glLineWidth(3)
    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_LINES)
    glVertex3f(-0.45, 0.5, 1.02); glVertex3f(-0.45, 1.0, 1.02) # Vertical
    glVertex3f(-0.7, 0.75, 1.02); glVertex3f(-0.2, 0.75, 1.02) # Horizontal
    glEnd()

def draw_roof():
    """Techo con voladizo"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.7, 0.1, 0.1)  # Rojo oscuro
    # Usamos 1.2 y -1.2 para que el techo sobresalga de las paredes (que están en 1 y -1)
    # Frente
    glVertex3f(-1.2, 1.5, 1.2); glVertex3f(1.2, 1.5, 1.2); glVertex3f(0, 2.8, 0)
    # Atrás
    glVertex3f(-1.2, 1.5, -1.2); glVertex3f(1.2, 1.5, -1.2); glVertex3f(0, 2.8, 0)
    # Izquierda
    glVertex3f(-1.2, 1.5, -1.2); glVertex3f(-1.2, 1.5, 1.2); glVertex3f(0, 2.8, 0)
    # Derecha
    glVertex3f(1.2, 1.5, -1.2); glVertex3f(1.2, 1.5, 1.2); glVertex3f(0, 2.8, 0)
    glEnd()

def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.4, 0.3) # Un verde oscuro tipo pasto
    glVertex3f(-30, 0, 30); glVertex3f(30, 0, 30)
    glVertex3f(30, 0, -30); glVertex3f(-30, 0, -30)
    glEnd()

def draw_single_house():
    draw_cube()
    draw_details()
    draw_roof()

def render_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # --- ACTUALIZAR LENTE DE CÁMARA (Para el Zoom) ---
    # Tenemos que redefinir la perspectiva en cada frame para que el zoom se aplique
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, 800/600, 0.1, 100.0) 
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # --- POSICIÓN DE LA CÁMARA ---
    gluLookAt(cam_x, cam_y, cam_z,  
              cam_x, 0, cam_z - 10,  
              0, 1, 0)              

    draw_ground() 

    # --- DIBUJAR VECINDARIO ---
    # Casa 1 Central
    glPushMatrix()
    draw_single_house()
    glPopMatrix()

    # Casa 2 Derecha
    glPushMatrix()
    glTranslatef(5, 0, 0) 
    draw_single_house()
    glPopMatrix()

    # Casa 3 Izquierda
    glPushMatrix()
    glTranslatef(-5, 0, 0) 
    draw_single_house()
    glPopMatrix()
    
    # Fila trasera
    glPushMatrix()
    glTranslatef(0, 0, -6) 
    draw_single_house()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(5, 0, -6) 
    draw_single_house()
    glPopMatrix()

    glfw.swap_buffers(window)

def main():
    global window
    if not glfw.init():
        sys.exit()
    
    width, height = 800, 600
    window = glfw.create_window(width, height, "Vecindario Detallado - Dron de Reconocimiento", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    while not glfw.window_should_close(window):
        procesar_teclado(window)
        render_scene()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()