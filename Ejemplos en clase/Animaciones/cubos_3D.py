import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

window = None

angulos_c1 = [0.0, 0.0, 0.0]
angulos_c2 = [0.0, 0.0, 0.0]
angulos_c3 = [0.0, 0.0, 0.0]
angulos_c4 = [0.0, 0.0, 0.0]

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(60, 1, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def dibujar_geometria_cubo():
    
    glBegin(GL_QUADS)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1, 1, -1); glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1); glVertex3f(1, 1, 1)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1, -1, 1); glVertex3f(-1, -1, 1)
    glVertex3f(-1, -1, -1); glVertex3f(1, -1, -1)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(1, 1, 1); glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1); glVertex3f(1, -1, 1)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1, -1, -1); glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1); glVertex3f(1, 1, -1)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(-1, 1, 1); glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1); glVertex3f(-1, -1, 1)
    # Cara derecha (Cyan)
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(1, 1, -1); glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1); glVertex3f(1, -1, -1)
    glEnd()

def renderizar_escena():
    global angulos_c1, angulos_c2, angulos_c3, angulos_c4
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    glTranslatef(0.0, 0.0, -12.0)

    # cubo 1
    glPushMatrix() # Guardar estado
    glTranslatef(-2.5, 2.5, 0.0) # Posicionar
    glRotatef(angulos_c1[0], 1, 0, 0)
    glRotatef(angulos_c1[1], 0, 1, 0)
    glRotatef(angulos_c1[2], 0, 0, 1)
    dibujar_geometria_cubo()
    glPopMatrix()  # Restaurar estado


    # CUBO 2: 
    glPushMatrix()
    glTranslatef(2.5, 2.5, 0.0)
    glRotatef(angulos_c2[1], 0, 1, 0) # Solo gira como un trompo
    dibujar_geometria_cubo()
    glPopMatrix()

    # CUBO 3: 
    glPushMatrix()
    glTranslatef(-2.5, -2.5, 0.0)
    glRotatef(angulos_c3[0], 1, 0, 1) # Gira en un eje diagonal
    dibujar_geometria_cubo()
    glPopMatrix()

    
    # CUBO 4: 

    glPushMatrix()
    glTranslatef(2.5, -2.5, 0.0)
    glRotatef(angulos_c4[2], 1, 1, 1) 
    dibujar_geometria_cubo()
    glPopMatrix()

    
    glfw.swap_buffers(window)
    

    angulos_c1[0] += 0.8; angulos_c1[1] += 1.0; angulos_c1[2] += 1.2
    angulos_c2[1] += 3.0  # Muy rápido
    angulos_c3[0] += 1.5  
    angulos_c4[2] -= 0.5  # Inverso y lento

def main():
    global window
    if not glfw.init():
        sys.exit()
    
    window = glfw.create_window(800, 800, "Escuadron de 4 Cubos Multi-Rotacion", None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)
    glViewport(0, 0, 800, 800)
    init()
    
    while not glfw.window_should_close(window):
        renderizar_escena()
        glfw.poll_events()
        
    glfw.terminate()

if __name__ == "__main__":
    main()