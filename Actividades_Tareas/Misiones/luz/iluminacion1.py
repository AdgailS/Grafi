import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

rotation = 0.0

def set_material(ambient, diffuse, specular, shininess, face=GL_FRONT):
    """Configura las propiedades del material para una superficie"""
    glMaterialfv(face, GL_AMBIENT, ambient)
    glMaterialfv(face, GL_DIFFUSE, diffuse)
    glMaterialfv(face, GL_SPECULAR, specular)
    glMaterialf(face, GL_SHININESS, shininess)

def draw_sphere(radius, slices=30, stacks=30):
    """Función auxiliar para dibujar esferas usando GLU"""
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

def draw_eye():
    # Piel
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    set_material(
        ambient=[0.2, 0.15, 0.15, 1.0],
        diffuse=[0.85, 0.67, 0.65, 1.0],
        specular=[0.3, 0.3, 0.3, 1.0],
        shininess=32  # plástico 
    )
    draw_sphere(0.54)
    glPopMatrix()

    # Esclerótica 
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    set_material(
        ambient=[0.4, 0.4, 0.4, 1.0],
        diffuse=[1.0, 1.0, 1.0, 1.0],
        specular=[0.8, 0.8, 0.8, 1.0],
        shininess=80  # pulido
    )
    draw_sphere(0.6)
    glPopMatrix()

    # Iris
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    set_material(
        ambient=[0.2, 0.2, 0.25, 1.0],
        diffuse=[0.2, 0.3, 0.8, 1.0],
        specular=[0.4, 0.4, 0.5, 1.0],
        shininess=32  # brillo
    )
    draw_sphere(0.55)
    glPopMatrix()

    # Pupila 
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    set_material(
        ambient=[0.05, 0.05, 0.05, 1.0],
        diffuse=[0.05, 0.05, 0.05, 1.0],
        specular=[0.05, 0.05, 0.05, 1.0],
        shininess=8  # mate
    )
    draw_sphere(0.4)
    glPopMatrix()

def setup_lighting():
    """Configura iluminación básica"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    
    # Deshabilitar GL_COLOR_MATERIAL para usar nuestros materiales personalizados
    glDisable(GL_COLOR_MATERIAL)
    
    # Luz ambiental tenue
    ambient_light = [0.2, 0.2, 0.2, 1.0]
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_light)
    
    # Luz principal
    light_position = [2.0, 3.0, 4.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    # Componentes de la luz
    light_ambient = [0.3, 0.3, 0.3, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

def main():
    global rotation

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Ojo 3D con Materiales", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    
    # Configurar vista y proyección
    glClearColor(0.54, 0.72, 0.84, 1.0)
    setup_lighting()
    
    # Habilitar smooth shading
    glShadeModel(GL_SMOOTH)

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