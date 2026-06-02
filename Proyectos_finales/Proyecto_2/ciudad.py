import pygame
import cv2
import mediapipe as mp
import math
import numpy as np
import os  # <-- Corregido: Necesario para solucionar el bug de rutas en Windows
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


WIDTH = 1280
HEIGHT = 720
FPS = 60

# Variables de animación.
fountain_angle = 0.0
water_bob = 0.0

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),       # Pulgar
    (0, 5), (5, 6), (6, 7), (7, 8),       # Índice
    (5, 9), (9, 10), (10, 11), (11, 12)   # Medio
]

# Posición inicial de la cámara.
camera_x = 0.0
camera_y = 8.0
camera_z = 28.0

# Rotación de cámara.
yaw = -90.0
pitch = -18.0

# Variables para control con mouse.
mouse_dragging = False
last_mouse_x = 0
last_mouse_y = 0

# Variables para control con mano usando MediaPipe.
hand_yaw_offset = 0.0
hand_pitch_offset = 0.0

# Variable de animación.
fountain_angle = 0.0
water_bob = 0.0


# ============================================================
# CONFIGURACIÓN MEDIAPIPE (CON PARCHE DE RUTAS PARA WINDOWS)
# ============================================================

# Parche automático: Forzamos a MediaPipe a buscar los modelos en la raíz de su carpeta de módulos
mp_path = os.path.dirname(mp.__file__)
modules_path = os.path.join(mp_path, 'modules')
if os.path.exists(modules_path) and modules_path not in os.environ.get('PATH', ''):
    os.environ['PATH'] = modules_path + os.pathsep + os.environ.get('PATH', '')

# Inicialización segura ante cambios de versión
try:
    import mediapipe.python.solutions.hands as mp_hands
except ImportError:
    mp_hands = mp.solutions.hands

# Inicializamos el detector con la variable global correcta
hands_detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

cap = cv2.VideoCapture(0)

# ============================================================
# INICIALIZACIÓN DE OPENGL
# ============================================================

def init_opengl():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    glShadeModel(GL_SMOOTH)

    # Color del cielo.
    glClearColor(0.57, 0.78, 0.95, 1.0)

    # Luz principal.
    glLightfv(GL_LIGHT0, GL_POSITION, (12.0, 24.0, 10.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.38, 0.38, 0.38, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.90, 0.90, 0.88, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.40, 0.40, 0.40, 1.0))

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, WIDTH / HEIGHT, 0.1, 250.0)

    glMatrixMode(GL_MODELVIEW)


# ============================================================
# CÁMARA CON GLULOOKAT
# ============================================================

def set_camera():
    glLoadIdentity()

    final_yaw = yaw + hand_yaw_offset
    final_pitch = pitch + hand_pitch_offset

    rad_yaw = math.radians(final_yaw)
    rad_pitch = math.radians(final_pitch)

    direction_x = math.cos(rad_pitch) * math.cos(rad_yaw)
    direction_y = math.sin(rad_pitch)
    direction_z = math.cos(rad_pitch) * math.sin(rad_yaw)

    look_x = camera_x + direction_x
    look_y = camera_y + direction_y
    look_z = camera_z + direction_z

    gluLookAt(
        camera_x, camera_y, camera_z,
        look_x, look_y, look_z,
        0, 1, 0
    )


# ============================================================
# PRIMITIVAS 3D
# ============================================================

def draw_cube(x, y, z, sx, sy, sz, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    glColor3f(*color)

    glBegin(GL_QUADS)

    # Frente
    glNormal3f(0, 0, 1)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    # Atrás
    glNormal3f(0, 0, -1)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)

    # Arriba
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    # Abajo
    glNormal3f(0, -1, 0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    # Derecha
    glNormal3f(1, 0, 0)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)

    # Izquierda
    glNormal3f(-1, 0, 0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    glEnd()
    glPopMatrix()


def draw_pyramid(x, y, z, sx, sy, sz, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    glColor3f(*color)

    glBegin(GL_TRIANGLES)

    # Cara frontal
    glNormal3f(0, 0.7, 1)
    glVertex3f(0, 0.5, 0)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    # Cara derecha
    glNormal3f(1, 0.7, 0)
    glVertex3f(0, 0.5, 0)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)

    # Cara trasera
    glNormal3f(0, 0.7, -1)
    glVertex3f(0, 0.5, 0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)

    # Cara izquierda
    glNormal3f(-1, 0.7, 0)
    glVertex3f(0, 0.5, 0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    glEnd()

    # Base
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glEnd()

    glPopMatrix()


def draw_sphere(x, y, z, radius, color, slices=24, stacks=24):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)

    quad = gluNewQuadric()
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

    glPopMatrix()


def draw_cylinder(x, y, z, radius, height, color, slices=24):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(*color)

    quad = gluNewQuadric()
    gluCylinder(quad, radius, radius, height, slices, 4)
    gluDeleteQuadric(quad)

    glPopMatrix()


def draw_cone(x, y, z, radius, height, color, slices=24):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(*color)

    quad = gluNewQuadric()
    gluCylinder(quad, radius, 0.0, height, slices, 4)
    gluDeleteQuadric(quad)

    glPopMatrix()


# ============================================================
# OBJETOS DECORATIVOS
# ============================================================

def draw_tree(x, z, scale=1.0):
    draw_cylinder(x, 0.0, z, 0.16 * scale, 1.35 * scale, (0.34, 0.18, 0.07))
    draw_sphere(x, 1.55 * scale, z, 0.65 * scale, (0.08, 0.48, 0.18))
    draw_sphere(x - 0.35 * scale, 1.32 * scale, z + 0.10 * scale, 0.45 * scale, (0.07, 0.40, 0.15))
    draw_sphere(x + 0.35 * scale, 1.32 * scale, z - 0.10 * scale, 0.45 * scale, (0.10, 0.55, 0.18))


def draw_lamp_post(x, z):
    draw_cylinder(x, 0.0, z, 0.06, 2.1, (0.08, 0.08, 0.08), slices=12)
    draw_sphere(x, 2.18, z, 0.22, (1.0, 0.88, 0.45), slices=16, stacks=16)
    draw_cone(x, 2.35, z, 0.25, 0.32, (0.08, 0.08, 0.08), slices=16)


def draw_bench(x, z, rotation=0):
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(rotation, 0, 1, 0)

    draw_cube(0, 0.45, 0, 1.6, 0.18, 0.35, (0.45, 0.23, 0.10))
    draw_cube(0, 0.85, -0.20, 1.6, 0.18, 0.18, (0.45, 0.23, 0.10))
    draw_cube(-0.65, 0.22, 0, 0.16, 0.45, 0.16, (0.12, 0.12, 0.12))
    draw_cube(0.65, 0.22, 0, 0.16, 0.45, 0.16, (0.12, 0.12, 0.12))

    glPopMatrix()


def draw_fountain():
    global fountain_angle, water_bob

    # Base circular simulada con cilindros.
    draw_cylinder(0, 0.05, 0, 1.75, 0.35, (0.42, 0.42, 0.42), slices=36)
    draw_cylinder(0, 0.36, 0, 1.35, 0.18, (0.60, 0.60, 0.58), slices=36)

    # Agua del estanque.
    draw_cylinder(0, 0.54, 0, 1.12, 0.08, (0.20, 0.62, 0.90), slices=36)

    # Columna central.
    draw_cylinder(0, 0.55, 0, 0.28, 1.10, (0.55, 0.55, 0.53), slices=24)

    # Plato superior.
    draw_cylinder(0, 1.60, 0, 0.75, 0.15, (0.62, 0.62, 0.60), slices=32)

    # Agua animada rotando.
    glPushMatrix()
    glTranslatef(0, 1.85 + water_bob, 0)
    glRotatef(fountain_angle, 0, 1, 0)

    draw_sphere(0, 0.0, 0, 0.22, (0.28, 0.75, 1.0), slices=16, stacks=16)

    for i in range(8):
        angle = math.radians(i * 45)
        x = math.cos(angle) * 0.65
        z = math.sin(angle) * 0.65
        draw_sphere(x, -0.25, z, 0.12, (0.28, 0.75, 1.0), slices=12, stacks=12)

    glPopMatrix()

# ============================================================
# CASAS Y EDIFICIOS
# ============================================================

def draw_house(x, z, wall_color, roof_color, rotation=0, size=1.0):
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(rotation, 0, 1, 0)
    glScalef(size, size, size)

    # Cuerpo principal.
    draw_cube(0, 1.1, 0, 3.0, 2.2, 2.8, wall_color)

    # Techo.
    draw_pyramid(0, 2.9, 0, 3.5, 1.5, 3.4, roof_color)

    # Puerta.
    draw_cube(0, 0.75, 1.43, 0.72, 1.35, 0.08, (0.28, 0.13, 0.05))

    # Ventanas.
    draw_cube(-0.90, 1.35, 1.45, 0.55, 0.55, 0.08, (0.55, 0.82, 0.96))
    draw_cube(0.90, 1.35, 1.45, 0.55, 0.55, 0.08, (0.55, 0.82, 0.96))

    # Marcos.
    draw_cube(-0.90, 1.35, 1.50, 0.68, 0.08, 0.05, (0.95, 0.95, 0.85))
    draw_cube(0.90, 1.35, 1.50, 0.68, 0.08, 0.05, (0.95, 0.95, 0.85))

    # Chimenea.
    draw_cube(0.95, 3.25, -0.35, 0.38, 0.80, 0.38, (0.45, 0.12, 0.08))

    glPopMatrix()


def draw_store(x, z, wall_color, rotation=0):
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(rotation, 0, 1, 0)

    draw_cube(0, 1.0, 0, 3.7, 2.0, 3.0, wall_color)
    draw_cube(0, 2.25, 0, 4.0, 0.45, 3.2, (0.78, 0.20, 0.16))

    # Toldo.
    draw_cube(0, 1.95, 1.65, 3.9, 0.20, 0.45, (0.95, 0.82, 0.30))
    draw_cube(-1.0, 1.95, 1.68, 0.45, 0.24, 0.50, (0.95, 0.35, 0.25))
    draw_cube(0.0, 1.95, 1.68, 0.45, 0.24, 0.50, (0.95, 0.35, 0.25))
    draw_cube(1.0, 1.95, 1.68, 0.45, 0.24, 0.50, (0.95, 0.35, 0.25))

    draw_cube(0, 0.75, 1.53, 0.75, 1.30, 0.08, (0.30, 0.15, 0.06))
    draw_cube(-1.10, 1.15, 1.55, 0.75, 0.65, 0.08, (0.55, 0.82, 0.96))
    draw_cube(1.10, 1.15, 1.55, 0.75, 0.65, 0.08, (0.55, 0.82, 0.96))

    glPopMatrix()


def draw_church():
    # Plataforma.
    draw_cube(0, 0.15, -29.0, 8.8, 0.30, 7.0, (0.46, 0.46, 0.44))

    # Nave principal.
    draw_cube(0, 2.0, -29.0, 7.0, 4.0, 5.5, (0.84, 0.78, 0.65))

    # Techo principal.
    draw_pyramid(0, 4.7, -29.0, 7.8, 2.1, 6.3, (0.46, 0.10, 0.08))

    # Fachada frontal más alta.
    draw_cube(0, 2.7, -25.8, 7.6, 5.4, 0.75, (0.88, 0.82, 0.69))

    # Campanario.
    draw_cube(0, 5.1, -25.4, 2.4, 5.0, 2.3, (0.80, 0.74, 0.62))

    # Cúpula/techo del campanario.
    draw_pyramid(0, 8.15, -25.4, 3.1, 2.4, 3.1, (0.42, 0.08, 0.07))

    # Cruz.
    draw_cube(0, 9.75, -25.4, 0.16, 1.10, 0.16, (0.12, 0.10, 0.08))
    draw_cube(0, 9.90, -25.4, 0.75, 0.16, 0.16, (0.12, 0.10, 0.08))

    # Puerta principal.
    draw_cube(0, 1.25, -25.35, 1.35, 2.3, 0.12, (0.27, 0.12, 0.04))
    draw_sphere(0, 2.35, -25.28, 0.68, (0.27, 0.12, 0.04), slices=18, stacks=18)

    # Ventanas frontales.
    draw_cube(-2.25, 2.4, -25.30, 0.78, 1.15, 0.12, (0.48, 0.78, 0.95))
    draw_cube(2.25, 2.4, -25.30, 0.78, 1.15, 0.12, (0.48, 0.78, 0.95))

    # Ventana del campanario.
    draw_cube(0, 5.65, -24.20, 0.78, 1.0, 0.12, (0.35, 0.18, 0.07))

    # Campana.
    draw_sphere(0, 5.2, -24.08, 0.35, (0.95, 0.70, 0.22), slices=16, stacks=16)

    # Columnas.
    draw_cylinder(-3.25, 0.2, -25.25, 0.18, 4.2, (0.72, 0.67, 0.56), slices=16)
    draw_cylinder(3.25, 0.2, -25.25, 0.18, 4.2, (0.72, 0.67, 0.56), slices=16)


# ============================================================
# SUELO, PLAZA Y CALLES
# ============================================================

def draw_ground():
    draw_cube(0, -0.12, -5, 90, 0.12, 90, (0.28, 0.62, 0.28))


def draw_roads():
    road_color = (0.30, 0.30, 0.30)
    road_line = (0.86, 0.82, 0.64)

    # Calle principal hacia la iglesia.
    draw_cube(0, 0.01, -7, 6.0, 0.06, 48.0, road_color)

    # Calle horizontal frente a la plaza.
    draw_cube(0, 0.02, 5.5, 50.0, 0.06, 5.3, road_color)

    # Calle horizontal trasera.
    draw_cube(0, 0.02, -14.5, 44.0, 0.06, 4.5, road_color)

    # Calles laterales.
    draw_cube(-17, 0.02, -6, 4.5, 0.06, 36.0, road_color)
    draw_cube(17, 0.02, -6, 4.5, 0.06, 36.0, road_color)

    # Líneas decorativas centrales.
    for z in range(-28, 16, 6):
        draw_cube(0, 0.07, z, 0.25, 0.04, 2.3, road_line)

    for x in range(-22, 25, 7):
        draw_cube(x, 0.08, 5.5, 2.5, 0.04, 0.20, road_line)
        draw_cube(x, 0.08, -14.5, 2.5, 0.04, 0.20, road_line)


def draw_plaza():
    # Base de la plaza.
    draw_cube(0, 0.06, -2.5, 15.0, 0.12, 15.0, (0.56, 0.56, 0.54))

    # Andadores internos.
    draw_cube(0, 0.12, -2.5, 14.2, 0.05, 2.0, (0.68, 0.66, 0.60))
    draw_cube(0, 0.13, -2.5, 2.0, 0.05, 14.2, (0.68, 0.66, 0.60))

    # Esquinas verdes de jardín.
    draw_cube(-4.5, 0.15, -7.0, 4.5, 0.08, 4.5, (0.18, 0.52, 0.22))
    draw_cube(4.5, 0.15, -7.0, 4.5, 0.08, 4.5, (0.18, 0.52, 0.22))
    draw_cube(-4.5, 0.15, 2.0, 4.5, 0.08, 4.5, (0.18, 0.52, 0.22))
    draw_cube(4.5, 0.15, 2.0, 4.5, 0.08, 4.5, (0.18, 0.52, 0.22))

    # Bordes de plaza.
    draw_cube(0, 0.22, 5.0, 15.3, 0.25, 0.35, (0.38, 0.38, 0.36))
    draw_cube(0, 0.22, -10.0, 15.3, 0.25, 0.35, (0.38, 0.38, 0.36))
    draw_cube(-7.5, 0.22, -2.5, 0.35, 0.25, 15.3, (0.38, 0.38, 0.36))
    draw_cube(7.5, 0.22, -2.5, 0.35, 0.25, 15.3, (0.38, 0.38, 0.36))

    # Fuente central.
    draw_fountain()

    # Bancas.
    draw_bench(-4.8, -2.5, 90)
    draw_bench(4.8, -2.5, -90)
    draw_bench(0, 2.7, 180)
    draw_bench(0, -7.7, 0)

    # Faroles.
    draw_lamp_post(-6.3, 3.8)
    draw_lamp_post(6.3, 3.8)
    draw_lamp_post(-6.3, -8.8)
    draw_lamp_post(6.3, -8.8)


# ============================================================
# DISTRIBUCIÓN DEL PUEBLO
# ============================================================

def draw_all_houses():
    # Colores low-poly.
    cream = (0.92, 0.76, 0.48)
    salmon = (0.92, 0.48, 0.36)
    blue = (0.50, 0.70, 0.88)
    green = (0.55, 0.78, 0.52)
    purple = (0.75, 0.55, 0.80)
    orange = (0.92, 0.62, 0.34)
    white = (0.88, 0.84, 0.76)
    yellow = (0.95, 0.80, 0.38)

    roof_red = (0.58, 0.12, 0.08)
    roof_brown = (0.42, 0.20, 0.10)

    # Casas laterales simétricas cerca de la plaza.
    draw_house(-12.5, -8.5, cream, roof_red, rotation=90)
    draw_house(12.5, -8.5, salmon, roof_red, rotation=-90)

    draw_house(-12.5, -2.0, blue, roof_brown, rotation=90)
    draw_house(12.5, -2.0, green, roof_brown, rotation=-90)

    draw_house(-12.5, 4.5, purple, roof_red, rotation=90)
    draw_house(12.5, 4.5, orange, roof_red, rotation=-90)

    # Casas más externas.
    draw_house(-23.0, -18.0, white, roof_red, rotation=0, size=1.1)
    draw_house(-14.5, -21.5, yellow, roof_brown, rotation=0)

    draw_house(23.0, -18.0, yellow, roof_red, rotation=0, size=1.1)
    draw_house(14.5, -21.5, white, roof_brown, rotation=0)

    draw_house(-24.0, 9.0, green, roof_red, rotation=180)
    draw_house(-15.5, 12.0, salmon, roof_brown, rotation=180)

    draw_house(24.0, 9.0, blue, roof_red, rotation=180)
    draw_house(15.5, 12.0, cream, roof_brown, rotation=180)

    # Tienditas cerca de la calle principal.
    draw_store(-6.5, 10.5, (0.92, 0.68, 0.40), rotation=180)
    draw_store(6.5, 10.5, (0.62, 0.78, 0.88), rotation=180)


def draw_all_trees():
    tree_positions = [
        (-7, -8), (7, -8), (-6, 3), (6, 3),
        (-20, -11), (-20, -5), (-20, 2), (-20, 8),
        (20, -11), (20, -5), (20, 2), (20, 8),
        (-29, -22), (-25, -12), (-28, 2), (-29, 14),
        (29, -22), (25, -12), (28, 2), (29, 14),
        (-8, -20), (8, -20), (-5, -24), (5, -24)
    ]

    for x, z in tree_positions:
        draw_tree(x, z, scale=1.0)


def draw_all_lamps():
    lamp_positions = [
        (-3.8, 8.0), (3.8, 8.0),
        (-3.8, -13.0), (3.8, -13.0),
        (-15.0, 6.0), (15.0, 6.0),
        (-15.0, -15.0), (15.0, -15.0),
        (-17.0, -24.0), (17.0, -24.0)
    ]

    for x, z in lamp_positions:
        draw_lamp_post(x, z)


def draw_scene():
    draw_ground()
    draw_roads()
    draw_plaza()
    draw_church()
    draw_all_houses()
    draw_all_trees()
    draw_all_lamps()


# ============================================================
# CONTROL CON TECLADO
# ============================================================

def update_keyboard(keys):
    global camera_x, camera_y, camera_z

    speed = 0.28
    vertical_speed = 0.18

    rad = math.radians(yaw)

    forward_x = math.cos(rad)
    forward_z = math.sin(rad)

    right_x = math.cos(rad + math.pi / 2)
    right_z = math.sin(rad + math.pi / 2)

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        camera_x += forward_x * speed
        camera_z += forward_z * speed

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        camera_x -= forward_x * speed
        camera_z -= forward_z * speed

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        camera_x -= right_x * speed
        camera_z -= right_z * speed

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        camera_x += right_x * speed
        camera_z += right_z * speed

    if keys[pygame.K_q]:
        camera_y += vertical_speed

    if keys[pygame.K_e]:
        camera_y -= vertical_speed
        if camera_y < 2.0:
            camera_y = 2.0


# ============================================================
# CONTROL CON MEDIAPIPE
# LANDMARK 8 = PUNTA DEL DEDO ÍNDICE
# ============================================================

def update_mediapipe():
    global hand_yaw_offset, hand_pitch_offset, camera_z

    ret, frame = cap.read()

    if not ret:
        hand_yaw_offset *= 0.90
        hand_pitch_offset *= 0.90
        return

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands_detector.process(rgb_frame)

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        
        # Guardar solo los puntos necesarios (hasta el dedo medio, landmark 12 es suficiente)
        keypoints = []
        for i, landmark in enumerate(hand_landmarks.landmark):
            if i <= 12:  # Solo procesamos los primeros 13 puntos (0 al 12)
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                keypoints.append((cx, cy))
            else:
                keypoints.append((0, 0)) # Relleno para mantener consistencia de índices
            
        # 1. Dibujar el esqueleto limitado a 3 dedos
        for connection in HAND_CONNECTIONS:
            start_idx = connection[0]
            end_idx = connection[1]
            if keypoints[start_idx] != (0,0) and keypoints[end_idx] != (0,0):
                cv2.line(frame, keypoints[start_idx], keypoints[end_idx], (0, 255, 0), 2)
        
        # 2. Control de Zoom y Línea Roja (Pulgar [4] e Índice [8])
        x1, y1 = keypoints[4]
        x2, y2 = keypoints[8]
        
        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
        
        # Calcular distancia matemática
        distancia_dedos = math.hypot(x2 - x1, y2 - y1)
        cx_medio, cy_medio = (x1 + x2) // 2, (y1 + y2) // 2
        
        # Mapear la distancia de pixeles (ej. de 30px a 200px) al rango Z de la cámara (ej. de 40.0 lejano a 5.0 cercano)
        # Ajusta los números si quieres que el zoom sea más o menos sensible
        camera_z = float(np.interp(distancia_dedos, [40, 220], [45.0, 5.0]))
        
        # Mostrar la distancia en pantalla
        cv2.putText(frame, f"Zoom: {int(distancia_dedos)} px", (cx_medio, cy_medio), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

        # 3. Control de rotación (Mantiene tu lógica original con el índice)
        index_tip = hand_landmarks.landmark[8]
        hand_yaw_offset = (index_tip.x - 0.5) * 45.0
        hand_pitch_offset = -(index_tip.y - 0.5) * 28.0

    else:
        hand_yaw_offset *= 0.92
        hand_pitch_offset *= 0.92

    # Mostrar la cámara con los 3 dedos detectados
    cv2.imshow("Deteccion de Manos - Vista de Camara", frame)
    cv2.waitKey(1)

# ============================================================
# CONTROL CON RATÓN
# ============================================================

def handle_mouse_event(event):
    global mouse_dragging
    global last_mouse_x
    global last_mouse_y
    global yaw
    global pitch

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            mouse_dragging = True
            last_mouse_x, last_mouse_y = event.pos

    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            mouse_dragging = False

    elif event.type == pygame.MOUSEMOTION:
        if mouse_dragging:
            mouse_x, mouse_y = event.pos

            dx = mouse_x - last_mouse_x
            dy = mouse_y - last_mouse_y

            sensitivity = 0.25

            yaw += dx * sensitivity
            pitch -= dy * sensitivity

            if pitch > 45:
                pitch = 45

            if pitch < -80:
                pitch = -80

            last_mouse_x = mouse_x
            last_mouse_y = mouse_y


# ============================================================
# ANIMACIÓN
# ============================================================

def update_animation():
    global fountain_angle
    global water_bob

    fountain_angle += 1.8

    if fountain_angle >= 360:
        fountain_angle = 0

    water_bob = math.sin(math.radians(fountain_angle * 2)) * 0.08


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    pygame.init()

    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Proyecto 3 - Ciudad Entorno 3D Mejorado")

    clock = pygame.time.Clock()

    init_opengl()

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            handle_mouse_event(event)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False

        update_keyboard(keys)
        update_mediapipe()
        update_animation()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        set_camera()
        draw_scene()

        pygame.display.flip()

    # ... (Final de tu ciclo while running en main)
    cap.release()
    hands_detector.close()
    cv2.destroyAllWindows()  # <--- Limpieza total de ventanas de OpenCV
    pygame.quit()
    
    cap.release()
    # Corregido: Se cambió 'hands.close()' por 'hands_detector.close()'
    hands_detector.close()
    pygame.quit()

if __name__ == "__main__":
    main()