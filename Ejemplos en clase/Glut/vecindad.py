import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluCylinder, gluSphere
import sys

window = None

# --- VARIABLES GLOBALES DE LA CÁMARA ---
cam_x = 0.0
cam_y = 8.0   # Altura media
cam_z = 25.0  # Empezamos lejos para ver el vecindario
fov = 60.0    # Field of View (Campo de visión para el ZOOM)

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Cielo azul
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

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
        fov -= velocidad_zoom  # Zoom IN (reduce el campo de visión)
        if fov < 10.0: fov = 10.0  # Límite máximo de zoom
    if glfw.get_key(window, glfw.KEY_X) == glfw.PRESS:
        fov += velocidad_zoom  # Zoom OUT (amplía el campo de visión)
        if fov > 120.0: fov = 120.0  # Límite de gran angular

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
    glVertex3f(-0.45, 0.5, 1.02); glVertex3f(-0.45, 1.0, 1.02)  # Vertical
    glVertex3f(-0.7, 0.75, 1.02); glVertex3f(-0.2, 0.75, 1.02)  # Horizontal
    glEnd()

def draw_roof():
    """Techo con voladizo"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.7, 0.1, 0.1)  # Rojo oscuro
    # Usamos 1.2 y -1.2 para que el techo sobresalga de las paredes
    # Frente
    glVertex3f(-1.2, 1.5, 1.2); glVertex3f(1.2, 1.5, 1.2); glVertex3f(0, 2.8, 0)
    # Atrás
    glVertex3f(-1.2, 1.5, -1.2); glVertex3f(1.2, 1.5, -1.2); glVertex3f(0, 2.8, 0)
    # Izquierda
    glVertex3f(-1.2, 1.5, -1.2); glVertex3f(-1.2, 1.5, 1.2); glVertex3f(0, 2.8, 0)
    # Derecha
    glVertex3f(1.2, 1.5, -1.2); glVertex3f(1.2, 1.5, 1.2); glVertex3f(0, 2.8, 0)
    glEnd()

def draw_trunk():
    """Dibuja el tronco del árbol como un cilindro"""
    glPushMatrix()
    glColor3f(0.6, 0.3, 0.1)  # Marrón para el tronco
    glRotatef(-90, 1, 0, 0)  # Rotar para orientar el cilindro verticalmente
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.3, 0.3, 1.5, 16, 16)  # Radio inferior, radio superior, altura
    glPopMatrix()

def draw_foliage():
    """Dibuja las hojas del árbol como una esfera"""
    glPushMatrix()
    glColor3f(0.1, 0.7, 0.1)  # Verde para las hojas
    glTranslatef(0.0, 1.5, 0.0)  # Posicionar encima del tronco
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.8, 16, 16)  # Radio de la esfera
    glPopMatrix()
    
    # Segunda capa de follaje (más pequeña encima)
    glPushMatrix()
    glColor3f(0.2, 0.8, 0.2)  # Verde más claro
    glTranslatef(0.0, 2.2, 0.0)
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.6, 16, 16)
    glPopMatrix()

def draw_tree(x, z):
    """Dibuja un árbol completo en la posición (x, z)"""
    glPushMatrix()
    glTranslatef(x, 0, z)
    draw_trunk()
    draw_foliage()
    glPopMatrix()

def draw_ground():
    """Dibuja un plano para representar el suelo"""
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.5, 0.2)  # Verde césped
    glVertex3f(-30, 0, 30); glVertex3f(30, 0, 30)
    glVertex3f(30, 0, -30); glVertex3f(-30, 0, -30)
    
    # Calle principal (gris)
    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(-4, 0.01, 30); glVertex3f(4, 0.01, 30)
    glVertex3f(4, 0.01, -30); glVertex3f(-4, 0.01, -30)
    glEnd()

def draw_single_house(x, z):
    """Dibuja una casa en la posición (x, z)"""
    glPushMatrix()
    glTranslatef(x, 0, z)
    draw_cube()
    draw_details()
    draw_roof()
    glPopMatrix()

def render_scene():
    """Renderiza toda la escena con casas y árboles"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # --- ACTUALIZAR LENTE DE CÁMARA (Para el Zoom) ---
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, 800/600, 0.1, 100.0) 
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # --- POSICIÓN DE LA CÁMARA ---
    gluLookAt(cam_x, cam_y, cam_z,  
              cam_x, 0, cam_z - 10,  
              0, 1, 0)              

    draw_ground()  # Dibujar el suelo

    # --- DIBUJAR VECINDARIO DE CASAS ---
    # Fila delantera (z = 0)
    draw_single_house(0, 0)    # Casa central
    draw_single_house(5, 0)    # Casa derecha
    draw_single_house(-5, 0)   # Casa izquierda
    
    # Fila trasera (z = -6)
    draw_single_house(0, -6)   # Casa central trasera
    draw_single_house(5, -6)   # Casa derecha trasera
    draw_single_house(-5, -6)  # Casa izquierda trasera

    # --- DIBUJAR 4 ÁRBOLES EN LÍNEA HORIZONTAL (en el eje X) ---
    # Posiciones: todos a la misma profundidad (Z = -3), variando en X
    draw_tree(-6, -3)   # Árbol 1: extremo izquierdo
    draw_tree(-2, -3)   # Árbol 2: izquierda media
    draw_tree(2, -3)    # Árbol 3: derecha media
    draw_tree(6, -3)    # Árbol 4: extremo derecho

    glfw.swap_buffers(window)

def main():
    global window
    if not glfw.init():
        sys.exit()
    
    width, height = 800, 600
    window = glfw.create_window(width, height, "Vecindario con 4 Árboles en Línea Horizontal", None, None)
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