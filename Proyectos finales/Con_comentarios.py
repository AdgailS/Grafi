# ------------------------------------------------------------
# IMPORTACIONES
# ------------------------------------------------------------

# time -> medir tiempo de ejecución y controlar animaciones
# math -> funciones matemáticas como sin(), cos(), pi
import time, math

# numpy -> arreglos y operaciones matemáticas rápidas
import numpy as np

# cv2 -> OpenCV para dibujar imágenes, texto, filtros y mostrar ventana
import cv2


# ------------------------------------------------------------
# CONFIGURACIÓN GENERAL DEL VIDEO / DEMO
# ------------------------------------------------------------

# Resolución de la ventana
W, H = 800, 600

# Frames por segundo
FPS = 30

# Duración total del demo en segundos
DURATION = 60.0


# ------------------------------------------------------------
# FUNCIONES MATEMÁTICAS AUXILIARES
# ------------------------------------------------------------

def clamp01(x):
    """
    Limita un valor entre 0 y 1.
    
    Si x < 0 -> devuelve 0
    Si x > 1 -> devuelve 1
    En otro caso devuelve x
    """
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


def smoothstep(a, b, x):
    """
    Interpolación suave.
    
    Muy usada en animación y transiciones.
    Hace que el movimiento empiece y termine suave.
    """
    
    # Normaliza x entre 0 y 1
    x = clamp01((x - a) / (b - a))

    # Fórmula smoothstep
    return x * x * (3 - 2 * x)


def poly_param(fx, fy, t0, t1, n, cx, cy, sx, sy):
    """
    Genera puntos de una curva paramétrica.
    
    fx y fy son funciones matemáticas.
    
    Ejemplo:
        x = sin(t)
        y = cos(t)
    
    Luego:
    - se escalan
    - se centran
    - se convierten a enteros para dibujar
    """

    # Valores de t distribuidos uniformemente
    ts = np.linspace(t0, t1, n, dtype=np.float32)

    # Coordenadas X
    xs = fx(ts) * sx + cx

    # Coordenadas Y
    ys = fy(ts) * sy + cy

    # Convierte a formato compatible con OpenCV
    return np.round(np.stack([xs, ys], 1)).astype(np.int32).reshape((-1, 1, 2))


def hsv_to_bgr(h, s, v):
    """
    Convierte color HSV a BGR.
    
    OpenCV trabaja en BGR.
    
    HSV:
        H -> tono/color
        S -> saturación
        V -> brillo
    """

    hsv = np.uint8([[[h % 180,
                      np.clip(s, 0, 255),
                      np.clip(v, 0, 255)]]])

    return tuple(int(x) for x in cv2.cvtColor(
        hsv,
        cv2.COLOR_HSV2BGR
    )[0, 0])


# ------------------------------------------------------------
# EFECTOS POST-PROCESADO
# ------------------------------------------------------------

def post_vignette(img, strength=0.7):
    """
    Efecto viñeta.
    
    Oscurece bordes de la imagen.
    Da apariencia cinematográfica.
    """

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

    # Coordenadas normalizadas
    nx = (xx - W*0.5) / (W*0.5)
    ny = (yy - H*0.5) / (H*0.5)

    # Distancia radial
    r2 = nx*nx + ny*ny

    # Más oscuro hacia bordes
    mask = np.clip(1.0 - strength * r2, 0.0, 1.0)

    # Aplicar máscara
    out = (img.astype(np.float32) * mask[..., None]).astype(np.uint8)

    return out


def post_scanlines(img, strength=0.22):
    """
    Simula líneas de monitor antiguo CRT.
    """

    out = img.astype(np.float32)

    y = np.arange(H, dtype=np.float32)

    # Patrón sinusoidal
    m = 1.0 - strength * (
        0.5 + 0.5*np.sin(2*np.pi*y/3.0)
    )

    out *= m[:, None, None]

    return np.clip(out, 0, 255).astype(np.uint8)


def post_posterize(img, q=32):
    """
    Reduce cantidad de colores.
    
    Da estilo artístico/cartoon.
    """

    q = max(1, int(q))

    return ((img // q) * q).astype(np.uint8)


# ------------------------------------------------------------
# FONDO GRADIENTE HSV
# ------------------------------------------------------------

def background_hsv_gradient(img, t, hue0=10, hue1=140):
    """
    Genera fondo dinámico con degradado HSV.
    
    Cambia colores con el tiempo.
    """

    hsv = np.zeros((H, W, 3), np.uint8)

    ys = np.linspace(0, 1, H, dtype=np.float32)

    # Variación de color animada
    hue = (
        hue0
        + (hue1 - hue0) * ys
        + 10*np.sin(t*0.4 + ys*2.0)
    ).astype(np.float32)

    hsv[:, :, 0] = np.clip(hue, 0, 179).astype(np.uint8)[:, None]

    hsv[:, :, 1] = 200

    hsv[:, :, 2] = (
        40 + 120*(1 - ys)
    ).astype(np.uint8)[:, None]

    # Convertir HSV -> BGR
    img[:] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


# ------------------------------------------------------------
# ESCENA 0 - PORTADA / CRÉDITOS
# ------------------------------------------------------------

def scene_credits(img, t):

    # Fondo dinámico
    background_hsv_gradient(img, t, hue0=165, hue1=105)

    # Generador aleatorio fijo
    rng = np.random.default_rng(1)

    # Posiciones de estrellas
    xs = rng.integers(0, W, 380)
    ys = rng.integers(0, int(H*0.65), 380)

    # Dibujar estrellas blancas
    img[ys, xs] = (255, 255, 255)

    # Blur suave
    img[:] = cv2.GaussianBlur(img, (0,0), 0.6)

    # Texto principal
    cv2.putText(
        img,
        "DEMO PROCEDURAL (GRAFICACION)",
        (42, 260),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.95,
        (245,245,245),
        2,
        cv2.LINE_AA
    )

    # Subtítulo
    cv2.putText(
        img,
        "OpenCV + Matematicas",
        (42, 310),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.85,
        (220,220,220),
        2,
        cv2.LINE_AA
    )


# ------------------------------------------------------------
# ESCENA 1 - CURVAS LISSAJOUS
# ------------------------------------------------------------

def scene_lissajous(img, t):

    background_hsv_gradient(img, t, hue0=18, hue1=60)

    # Parámetros animados
    a = 3 + 0.7 * math.sin(t*0.6)
    b = 2 + 0.7 * math.cos(t*0.8)

    delta = math.pi/2 + 0.4*math.sin(t*0.3)

    # Ecuaciones paramétricas
    fx = lambda x: np.sin(a*x + delta)
    fy = lambda x: np.sin(b*x)

    # Generación de puntos
    pts = poly_param(
        fx, fy,
        0, 2*math.pi,
        900,
        W*0.5, H*0.45,
        260, 180
    )

    # Color dinámico
    col = hsv_to_bgr(
        int(20 + 30*np.sin(t*0.8)),
        210,
        240
    )

    # Dibujar curva
    cv2.polylines(
        img,
        [pts],
        False,
        col,
        2,
        cv2.LINE_AA
    )


# ------------------------------------------------------------
# ESCENA 2 - ROSA POLAR
# ------------------------------------------------------------

def scene_rose_polar(img, t):

    background_hsv_gradient(img, t, hue0=120, hue1=165)

    # Número de pétalos
    k = 5

    theta0 = t * 0.6

    # Fórmula polar
    fx = lambda th: np.cos(k*th) * np.cos(th + theta0)
    fy = lambda th: np.cos(k*th) * np.sin(th + theta0)

    pts = poly_param(
        fx, fy,
        0, 2*math.pi,
        1200,
        W*0.5, H*0.45,
        240, 240
    )

    col = hsv_to_bgr(
        int(145 + 25*np.sin(t*0.5)),
        220,
        245
    )

    cv2.polylines(
        img,
        [pts],
        False,
        col,
        2,
        cv2.LINE_AA
    )

    # Círculos pulsantes
    for i in range(6):

        r = int(
            18 + 10*np.sin(t*2.0 + i)
        )

        cv2.circle(
            img,
            (int(W*0.18 + i*110), int(H*0.78)),
            max(1, r),
            (230,230,230),
            1,
            cv2.LINE_AA
        )


# ------------------------------------------------------------
# ESCENA 3 - SPIROGRAPH
# ------------------------------------------------------------

def scene_spirograph(img, t):

    background_hsv_gradient(img, t, hue0=80, hue1=20)

    # Parámetros matemáticos
    R, r, d = 8.0, 3.0, 5.0

    w = (R - r) / r

    # Fórmulas de hipotrocoide
    fx = lambda x: (
        (R-r)*np.cos(x)
        + d*np.cos(w*x + 0.4*np.sin(t*0.7))
    )

    fy = lambda x: (
        (R-r)*np.sin(x)
        - d*np.sin(w*x + 0.4*np.cos(t*0.6))
    )

    pts = poly_param(
        fx, fy,
        0, 14*math.pi,
        1600,
        W*0.5, H*0.46,
        26, 26
    )

    col = hsv_to_bgr(
        int(10 + 140*(0.5+0.5*np.sin(t*0.4))),
        240,
        240
    )

    cv2.polylines(
        img,
        [pts],
        False,
        col,
        2,
        cv2.LINE_AA
    )

    # Efecto scanlines
    img[:] = post_scanlines(img, 0.18)


# ------------------------------------------------------------
# ESCENA 4 - PARTÍCULAS
# ------------------------------------------------------------

def scene_particles(img, t, rng):

    background_hsv_gradient(img, t, hue0=150, hue1=100)

    # Número de partículas
    n = 1200

    # Posiciones aleatorias
    xs = rng.random(n) * W
    ys = rng.random(n) * H

    # Movimiento procedural
    xs = (
        xs
        + 110*np.sin(ys/55.0 + t*1.7)
        + 40*np.cos(t*0.7)
    ) % W

    ys = (
        ys
        + 85*np.cos(xs/75.0 + t*1.2)
        + 30*np.sin(t*0.9)
    ) % H

    # Brillo animado
    v = (
        0.5 + 0.5*math.sin(t*1.9)
    )

    col = hsv_to_bgr(
        int(95 + 40*math.sin(t*0.8)),
        210,
        int(210 + 40*v)
    )

    # Dibujar partículas
    img[
        ys.astype(np.int32),
        xs.astype(np.int32)
    ] = col

    # Blur para glow
    img[:] = cv2.GaussianBlur(img, (0,0), 1.1)


# ------------------------------------------------------------
# ESCENA 5 - FUEGO PROCEDURAL
# ------------------------------------------------------------

def scene_fire(img, t, state):

    heat = state["heat"]
    rng = state["rng"]

    # Enfriamiento gradual
    heat[:] = (heat * 0.93).astype(np.float32)

    # Inyección de calor
    base_n = 1400

    xs = rng.integers(0, W, base_n)
    ys = rng.integers(int(H*0.82), H, base_n)

    heat[ys, xs] += rng.random(base_n) * (
        0.8 + 0.6*(0.5+0.5*math.sin(t*2.0))
    )

    # Difusión térmica
    heat[:] = cv2.GaussianBlur(heat, (0, 0), 2.2)

    # Movimiento hacia arriba
    heat[:-2, :] = heat[2:, :]

    heat[-2:, :] *= 0.0

    # Conversión a color
    h = (20 - 20*np.clip(heat, 0, 1)).astype(np.uint8)
    s = (220 - 80*np.clip(heat, 0, 1)).astype(np.uint8)
    v = (60 + 195*np.clip(heat, 0, 1)).astype(np.uint8)

    hsv = np.dstack([h, s, v]).astype(np.uint8)

    img[:] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Base negra
    cv2.rectangle(
        img,
        (0, int(H*0.83)),
        (W, H),
        (10, 10, 10),
        -1
    )

    # Chispas
    sparks = 160

    sx = rng.integers(0, W, sparks)
    sy = rng.integers(int(H*0.55), int(H*0.9), sparks)

    img[sy, sx] = (255, 255, 255)

    img[:] = cv2.GaussianBlur(img, (0,0), 0.6)


# ------------------------------------------------------------
# CONTROLADOR DE ESCENAS
# ------------------------------------------------------------

def render_scene(buf, scene_id, t, rng, fire_state):

    if scene_id == 0:
        scene_credits(buf, t)

    elif scene_id == 1:
        scene_lissajous(buf, t)

    elif scene_id == 2:
        scene_rose_polar(buf, t)

    elif scene_id == 3:
        scene_spirograph(buf, t)

    elif scene_id == 4:
        scene_particles(buf, t, rng)

    else:
        scene_fire(buf, t, fire_state)


# ------------------------------------------------------------
# TIMELINE GENERAL
# ------------------------------------------------------------

def timeline(t, rng, bufA, bufB, fire_state):

    # Divide demo en bloques de 10 segundos
    block = int(min(5, max(0, t // 10)))

    # Tiempo interno del bloque
    t_in = t - block*10

    # Render escena actual
    render_scene(bufA, block, t, rng, fire_state)

    frame = bufA

    # TRANSICIONES
    if block < 5 and t_in >= 8.8:

        render_scene(bufA, block, t, rng, fire_state)
        render_scene(bufB, block+1, t, rng, fire_state)

        # Interpolación suave
        a = smoothstep(8.8, 10.0, t_in)

        # Mezcla de escenas
        frame = cv2.addWeighted(
            bufA, 1-a,
            bufB, a,
            0
        )

        # Flash blanco
        flash = smoothstep(9.6, 10.0, t_in)

        if flash > 0:

            frame = cv2.addWeighted(
                frame,
                1.0,
                np.full_like(frame, 255),
                0.12*flash,
                0
            )

    # Fade in y fade out
    fin = smoothstep(0.0, 1.5, t)

    fout = 1.0 - smoothstep(
        DURATION - 1.5,
        DURATION,
        t
    )

    f = fin * fout

    if f < 0.999:
        frame = (
            frame.astype(np.float32) * f
        ).astype(np.uint8)

    return frame


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():

    # RNG global
    rng = np.random.default_rng(123)

    # Buffers de imagen
    bufA = np.zeros((H, W, 3), np.uint8)
    bufB = np.zeros((H, W, 3), np.uint8)

    # Estado persistente para fuego
    fire_state = {
        "heat": np.zeros((H, W), np.float32),
        "rng": np.random.default_rng(999),
    }

    # Número total de frames
    total_frames = int(DURATION * FPS)

    t0 = time.perf_counter()

    # Loop principal
    for i in range(total_frames):

        # Tiempo actual
        t = i / FPS

        # Generar frame
        frame = timeline(
            t,
            rng,
            bufA,
            bufB,
            fire_state
        )

        # Postprocesado global
        frame = post_vignette(frame, 0.72)
        frame = post_scanlines(frame, 0.16)
        frame = post_posterize(frame, 24)

        # Mostrar ventana
        cv2.imshow(
            "Proyecto Final: demo procedural (OpenCV)",
            frame
        )

        # ESC para salir
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Tiempo total
    print("Tiempo:", time.perf_counter() - t0)

    cv2.destroyAllWindows()


# ------------------------------------------------------------
# PUNTO DE ENTRADA
# ------------------------------------------------------------

if __name__ == "__main__":
    main()