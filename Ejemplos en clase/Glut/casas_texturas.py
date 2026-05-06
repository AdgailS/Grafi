import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from PIL import Image
import sys

tex_pasto = None
tex_pared = None
tex_techo = None


def load_texture(path):

    img = Image.open(path).convert("RGB")
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.tobytes()

    tex_id = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    glBindTexture(GL_TEXTURE_2D, tex_id)

    # Filtrado
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Envoltura (tiling)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Subir la textura
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 img.width, img.height, 0,
                 GL_RGB, GL_UNSIGNED_BYTE, img_data)

    # Crear mipmaps
    glGenerateMipmap(GL_TEXTURE_2D)

    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id


def init():
    global tex_pasto, tex_pared, tex_techo

    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 800 / 600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    # Cargar texturas
    tex_pasto = load_texture("Imagenes/pasto.jpg")
    tex_pared = load_texture("Imagenes/piso.jpg")
    tex_techo = load_texture("Imagenes/techogit .jpg")


def draw_ground():
    glBindTexture(GL_TEXTURE_2D, tex_pasto)

    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)

    scale = 5

    glTexCoord2f(0, 0);       glVertex3f(-10, 0, 10)
    glTexCoord2f(scale, 0);   glVertex3f( 10, 0, 10)
    glTexCoord2f(scale, scale);glVertex3f( 10, 0,-10)
    glTexCoord2f(0, scale);   glVertex3f(-10, 0,-10)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)


# ------------------------------------------------------------
# Casa con textura de pared
# ------------------------------------------------------------
def draw_cube():
    glBindTexture(GL_TEXTURE_2D, tex_pared)

    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)

    # Frente
    glTexCoord2f(0, 0); glVertex3f(-1, 0, 1)
    glTexCoord2f(1, 0); glVertex3f( 1, 0, 1)
    glTexCoord2f(1, 1); glVertex3f( 1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1, 1)

    # Atrás
    glTexCoord2f(0, 0); glVertex3f(-1, 0,-1)
    glTexCoord2f(1, 0); glVertex3f( 1, 0,-1)
    glTexCoord2f(1, 1); glVertex3f( 1, 1,-1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1,-1)

    # Izquierda
    glTexCoord2f(0, 0); glVertex3f(-1, 0,-1)
    glTexCoord2f(1, 0); glVertex3f(-1, 0, 1)
    glTexCoord2f(1, 1); glVertex3f(-1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1,-1)

    # Derecha
    glTexCoord2f(0, 0); glVertex3f( 1, 0,-1)
    glTexCoord2f(1, 0); glVertex3f( 1, 0, 1)
    glTexCoord2f(1, 1); glVertex3f( 1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f( 1, 1,-1)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)


# ------------------------------------------------------------
# Techo con textura propia
# ------------------------------------------------------------
def draw_roof():
    glBindTexture(GL_TEXTURE_2D, tex_techo)

    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 1)

    glTexCoord2f(0, 0);    glVertex3f(-1, 1, 1)
    glTexCoord2f(1, 0);    glVertex3f( 1, 1, 1)
    glTexCoord2f(0.5, 1);  glVertex3f( 0, 2, 0)

    glTexCoord2f(0, 0);    glVertex3f(-1, 1,-1)
    glTexCoord2f(1, 0);    glVertex3f( 1, 1,-1)
    glTexCoord2f(0.5, 1);  glVertex3f( 0, 2, 0)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)


# ------------------------------------------------------------
# Escena principal
# ------------------------------------------------------------
def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(4, 4, 8, 0, 1, 0, 0, 1, 0)

    draw_ground()
    draw_cube()
    draw_roof()

    glfw.swap_buffers(window)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    global window

    if not glfw.init():
        sys.exit()

    window = glfw.create_window(800, 600, "Casa con Varias Texturas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, 800, 600)

    init()

    while not glfw.window_should_close(window):
        draw_scene()
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()