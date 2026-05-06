import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

rotation = 0.0

def draw_sphere(radius, slices=30, stacks=30):
    """Función auxiliar para dibujar esferas usando GLU"""
    quad = gluNewQuadric()
    gluQuadricNormals(quad,GLU_SMOOTH)
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

def draw_eye():
    glPushMatrix()

    glColor3f(0.85, 0.67, 0.65)  # “piel”
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54)
    glPopMatrix()

    glColor3f(1, 1, 1)  # blanco
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6)
    glPopMatrix()

    glColor3f(0.84, 0.85, 0.92)  # iris
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55)
    glPopMatrix()

    glColor3f(0, 0, 0)  # pupila
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    draw_sphere(0.4)
    glPopMatrix()

    glPopMatrix()

def setup_lighting():
    """Configura iluminación básica (en el código base está incompleto)"""
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    
    light_position = [1.0, 1.0, 1.0, 0.2]
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_position[3])

def main():
    global rotation

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Dos Esferas Simples", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glClearColor(0.54, 0.72, 0.84, 1.0)
    setup_lighting()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -5)

        rotation += 0.1
        glRotatef(rotation, 0, 1, 0)

        draw_eye()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()