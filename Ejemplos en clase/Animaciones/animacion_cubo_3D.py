import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

# Variables globales
window = None
angle_x = 0
angle_y = 0
angle_z = 0

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def draw_cube():
    global angle_x, angle_y, angle_z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    glTranslatef(0.0, 0.0, -6)
    
    #  Rotar en los tres ejes
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)

    glBegin(GL_QUADS)
    # Cara superior
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)
    # Cara inferior
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    # Cara frontal
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    # Cara trasera
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1, -1, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    # Cara izquierda
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)
    # Cara derecha
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, -1)
    glEnd()

    glfw.swap_buffers(window)
    
    # Incrementar los tres ángulos
    angle_x += 0.8
    angle_y += 1.0
    angle_z += 1.2

def main():
    global window
    if not glfw.init():
        sys.exit()
    window = glfw.create_window(600, 600, "Cubo 3D Rotando (X, Y, Z)", None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)
    glViewport(0, 0, 600, 600)
    init()
    while not glfw.window_should_close(window):
        draw_cube()
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()