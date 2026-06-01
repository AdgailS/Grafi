import time, math
import numpy as np
import cv2

########### MI TRABAJO ################
#----- LO QUE HACE FALTA-----
# TIEMPOS
# 2 ESCENAS FINALES, AAGREGAR MAS


W, H = 800, 600
FPS = 30
DURATION = 60.0 

angulos_up = [0.24, 0.21, 0.18, 0.15]
angulos_down = [0.22, 0.19, 0.16, 0.13, 0.10]

def clamp01(x): return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)
def smoothstep(a, b, x):
    x = clamp01((x - a) / (b - a))
    return x * x * (3 - 2 * x)

def hsv_to_bgr(h, s, v):
    hsv = np.uint8([[[h % 180, np.clip(s, 0, 255), np.clip(v, 0, 255)]]])
    return tuple(int(x) for x in cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0, 0])

# ------------------------------------------------------------
# FILTROS DE POST-PROCESADO (Requerimiento de la Rúbrica)
# ------------------------------------------------------------
def post_vignette(img, strength=0.7):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - W*0.5) / (W*0.5)
    ny = (yy - H*0.5) / (H*0.5)
    r2 = nx*nx + ny*ny
    mask = np.clip(1.0 - strength * r2, 0.0, 1.0)
    return (img.astype(np.float32) * mask[..., None]).astype(np.uint8)

def post_scanlines(img, strength=0.12):
    out = img.astype(np.float32)
    y = np.arange(H, dtype=np.float32)
    m = 1.0 - strength * (0.5 + 0.5 * np.sin(2 * np.pi * y / 3.0))
    out *= m[:, None, None]
    return np.clip(out, 0, 255).astype(np.uint8)

def post_posterize(img, q=32):
    q = max(1, int(q))
    return ((img // q) * q).astype(np.uint8)

# ------------------------------------------------------------
# FONDO SÓLIDO CON COLOR CAMBIANTE
# ------------------------------------------------------------
def background_solid(img, t, hue_base, sat=220, val=100):
    """Fondo sólido que cambia de color lentamente"""
    hue = (hue_base + int(t * 10)) % 180
    color = hsv_to_bgr(hue, sat, val)
    img[:] = color

def affine_rotate(img, angle):
    M = cv2.getRotationMatrix2D((W//2, H//2), angle, 1.0)
    return cv2.warpAffine(img, M, (W, H))

def affine_shear(img, amount):
    M = np.float32([[1, amount, 0],[0,1,0]])
    return cv2.warpAffine(img, M, (W, H))


def background_gradient(img, t, h0=130, h1=170):
    """Fondo dinámico procedural usando gradiente vertical en HSV"""
    hsv = np.zeros((H, W, 3), np.uint8)
    ys = np.linspace(0, 1, H, dtype=np.float32)
    hue = (h0 + (h1 - h0) * ys + 8 * np.sin(t * 0.5 + ys * 3.0)).astype(np.float32)
    hsv[:, :, 0] = np.clip(hue, 0, 179).astype(np.uint8)[:, None]
    hsv[:, :, 1] = 180
    hsv[:, :, 2] = (30 + 90 * (1 - ys)).astype(np.uint8)[:, None]
    img[:] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def draw_stars(img, t, rng_seed=42, num_stars=80):
    """Efecto global de fondo: Campo de estrellas titilantes"""
    rng = np.random.default_rng(rng_seed)
    xs = rng.integers(0, W, num_stars)
    ys = rng.integers(0, H, num_stars)
    sizes = rng.integers(1, 3, num_stars)
    for i in range(num_stars):
        # Brillo variable por el tiempo para simular titileo
        blink = int(150 + 105 * math.sin(t * 3.0 + i))
        cv2.circle(img, (int(xs[i]), int(ys[i])), int(sizes[i]), (blink, blink, blink), -1)
        
# ------------------------------------------------------------
# FONDOS DINÁMICOS ÚNICOS (Inspirados, no idénticos al Proyecto 1)
# ------------------------------------------------------------
def background_wave_mesh(img, t, base_hue=140):
    """Fondo dinámico: Malla de ondas cinéticas abstractas que mutan con el tiempo"""
    hsv = np.zeros((H, W, 3), np.uint8)
    yy, xx = np.mgrid[0:H:15, 0:W:15]
    
    # Ecuación de onda senoidal cruzada para distorsionar el fondo continuamente
    deformacion = np.sin(xx * 0.01 + t * 1.5) * np.cos(yy * 0.01 + t * 1.2)
    h_map = (base_hue + 25 * deformacion).astype(np.uint8)
    v_map = (45 + 50 * np.sin(yy * 0.02 + t)).astype(np.uint8)
    
    # Renderizar el entramado procedural base oscuro
    img[:] = hsv_to_bgr(base_hue, 160, 30) 
    for i in range(h_map.shape[0]):
        for j in range(h_map.shape[1]):
            pt_x = xx[i, j] + int(10 * np.sin(t + yy[i, j]))
            pt_y = yy[i, j] + int(10 * np.cos(t + xx[i, j]))
            color = hsv_to_bgr(int(h_map[i, j]), 200, int(v_map[i, j]))
            cv2.circle(img, (pt_x, pt_y), 1, color, -1)

def draw_cosmic_dust(img, t, seed=999):
    """Efecto ambiental: Partículas de polvo oscilando en microvórtices independientes"""
    rng = np.random.default_rng(seed)
    n = 60
    xs = rng.integers(0, W, n)
    ys = rng.integers(0, H, n)
    for i in range(n):
        dx = int(12 * math.sin(t * 2.0 + i))
        dy = int(12 * math.cos(t * 1.5 + i))
        val = int(130 + 125 * math.sin(t * 4.0 + i))
        cv2.circle(img, (int(xs[i] + dx) % W, int(ys[i] + dy) % H), 1, (val, val, val), -1)

def background_radial(img, t, hue_base):
    """Fondo 3: Ondas cinéticas concéntricas en constante expansión armónica"""
    hue = (hue_base + int(t * 6)) % 180
    img[:] = hsv_to_bgr(hue, 180, 40)
    cx, cy = W // 2, H // 2
    color_c = hsv_to_bgr((hue + 20) % 180, 150, 70)
    for r in range(60, 600, 70):
        dr = int(r + 20 * math.sin(t * 2.5 + r * 0.04))
        if dr > 0:
            cv2.circle(img, (cx, cy), dr, color_c, 1, cv2.LINE_AA)
            
# ------------------------------------------------------------
# ESCENAS
# ------------------------------------------------------------
def scene_credits(img, t):
    """Escena 1: Intro """
    
    background_gradient(img, t, h0=100, h1=140)
    draw_stars(img, t, rng_seed=111, num_stars=100)

    cx, cy = W // 2, H // 2
    for r in range(40, 240, 40):
        dinamic_r = r + int(15 * math.sin(t * 3.0 + r))
        col = hsv_to_bgr(150 + r // 5, 220, 100)
        cv2.circle(img, (cx, cy), dinamic_r, col, 1, cv2.LINE_AA)
    
    titulo = "DEMO FIGURAS GEOMETRICAS"
    subtitulo = "OpenCV + Matematicas"
    nombre = "Estrella Abigail"

    size1 = cv2.getTextSize(titulo, cv2.FONT_HERSHEY_SIMPLEX, 0.95, 2)[0]
    size2 = cv2.getTextSize(subtitulo, cv2.FONT_HERSHEY_SIMPLEX, 0.85, 2)[0]
    size3 = cv2.getTextSize(nombre, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.85, 2)[0]

    cv2.putText(img, titulo, ((W-size1[0])//2, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (245,245,245), 2, cv2.LINE_AA)
    cv2.putText(img, subtitulo, ((W-size2[0])//2, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (220,220,220), 2, cv2.LINE_AA)
    cv2.putText(img, nombre, ((W-size3[0])//2, 360), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.85, (220,220,220), 2, cv2.LINE_AA)
    
#------------------- LOTUS - CÍRCULOS ANIMADOS EN FORMA DE FLOR ----------------------
def scene_lotus(img, t, scale=1.7):
    """Escena 2: Multi-Lotus Orbital con Nodos Dinámicos Pulsantes"""
    
    background_wave_mesh(img, t, base_hue=25) 
    draw_cosmic_dust(img, t, seed=44)
    cx, cy = W // 2, H // 2
    petals = 20
    freq_pulsar = 1.2 + 0.2 * math.sin(t * 3.5) #### 3.5 A 2.5
    radio_base = int(80 * freq_pulsar)
    
    for i in range(petals):
        ang = 2 * np.pi * i / petals + (t * 0.4)
        x = int(cx + radio_base * np.cos(ang))
        y = int(cy + radio_base * np.sin(ang))
        
        color_line = hsv_to_bgr(int(20 + i * 3), 240, 230)
        cv2.circle(img, (x, y), int(60 * freq_pulsar), color_line, 1, cv2.LINE_AA)
        cv2.circle(img, (x, y), 3, (255, 255, 255), -1, cv2.LINE_AA)
        
    cv2.putText(img, "Curva 1: Lotus Orbital Encadenado", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 255, 220), 1, cv2.LINE_AA)
        
#------------------- ROSE POLAR - CÍRCULOS QUE SE DESINTEGRAN EN EL EXTERIOR ------------- YA COMPLETADO
def scene_rose_polar(img, t, scale=1):
    """Escena 3: Estructura de Rosa Polar con Vórtice de Dispersión"""
    background_wave_mesh(img, t, base_hue=95) 
    draw_cosmic_dust(img, t, seed=71)
    
    cx, cy = W // 2, H // 2
    R = int(110 + 20 * math.sin(t * 2.0))
    rotacion = t * 0.5
    
    for i in range(8):
        angle = i * math.pi * 2 / 8 + rotacion
        x = int(cx + R * math.cos(angle))
        y = int(cy + R * math.sin(angle))
        color = hsv_to_bgr(int(90 + i * 5), 230, 210)
        cv2.circle(img, (x, y), R, color, 1, cv2.LINE_AA)

    p_max = 120
    for i in range(p_max):
        ang_p = (i / p_max) * 2 * np.pi
        rad_p = 240 + 30 * math.sin(ang_p * 4 + t * 2.0)
        
        px = int(cx + rad_p * np.cos(ang_p + t * 0.2))
        py = int(cy + rad_p * np.sin(ang_p + t * 0.2))
        cv2.circle(img, (px, py), 2, hsv_to_bgr(110, 255, 255), -1)
        
    cv2.putText(img, "Curvas 2-3: Rosa Polar Bio-Morfica", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 255, 220), 1, cv2.LINE_AA)

#------------------- SPIROGRAPH - CÍRCULOS DENTRO DE CÍRCULOS CON LÍNEAS CONECTIVAS ----- AGREGAR ALGO EN MOVIMIENTO AL REDEDOR, ESQUINAS 
def scene_spirograph(img, t, scale=2):
    background_wave_mesh(img, t, base_hue=5) 

    cx, cy = W//2, H//2
    R = int(min(W, H) * 0.07 * scale)
    R2 = int(R * 1.732)
    rotacion_total = t * 0.2
    col = hsv_to_bgr(int(30 + 40*math.sin(t*0.5)), 210, 235)
    cv2.circle(img, (cx, cy), R, col, 2, cv2.LINE_AA)

    for i in range(6):
        angle = i * math.pi * 2 / 6 + rotacion_total
        x = int(cx + R * math.cos(angle))
        y = int(cy + R * math.sin(angle))
        cv2.circle(img, (x, y), R, col, 2, cv2.LINE_AA)

    for i in range(12):
        angle = i * math.pi * 2 / 12 + rotacion_total
        x = int(cx + R2 * math.cos(angle))
        y = int(cy + R2 * math.sin(angle))
        cv2.circle(img, (x, y), R, col, 1, cv2.LINE_AA)
    
    radio = R2 + R
    t_local = max(0.0, t - 30.0)
    rotacion = t_local * 0.8
    col_circulo = hsv_to_bgr(280, 255, 255)
    theta_max = min(2*np.pi, t_local * 1.8)
    paso = max(0.005, 0.08 - t_local * 0.01)

    if theta_max > 0:
        for ang in np.arange(0, theta_max, paso):
            x = int(cx + radio * np.cos(ang + rotacion))
            y = int(cy + radio * np.sin(ang + rotacion))
            cv2.circle(img, (x, y), 2, col_circulo, -1)

    col_magia = hsv_to_bgr(int(t * 25 % 180), 240, 255)
    
    # 1. GRAN ESTRELLA GEOMÉTRICA
    puntas = 8
    pts_estrella = []
    for i in range(puntas * 2):
        ang_e = i * (math.pi / puntas) - t * 0.6
        r_e = (radio + 130) if i % 2 == 0 else (radio + 40 + int(60 * math.sin(t * 3.5)))
        pts_estrella.append([int(cx + r_e * math.cos(ang_e)), int(cy + r_e * math.sin(ang_e))])
    
    cv2.polylines(img, [np.array(pts_estrella, np.int32)], True, col_magia, 2, cv2.LINE_AA)

    # 2. ONDAS DE CHOQUE EN LAS 4 ESQUINAS
    radio_pulso = int((t * 120) % 180) 
    for ex, ey in [(0, 0), (W, 0), (0, H), (W, H)]:
        cv2.circle(img, (ex, ey), radio_pulso, col_magia, 1, cv2.LINE_AA)
        cv2.circle(img, (ex, ey), max(0, radio_pulso - 60), col_magia, 1, cv2.LINE_AA)
        cv2.circle(img, (ex, ey), max(0, radio_pulso - 120), col_magia, 1, cv2.LINE_AA)

    cv2.putText(img, "Curva 4: Sistema de Espirografo y Ondas de Choque", 
                (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 255, 220), 1, cv2.LINE_AA)
    
    
#------------------- PARTICULAS - TRIÁNGULOS QUE ORBITAN Y SE DEFORMAN -------------
def scene_star(img, t, scale=1.7):
    """Escena 5: Tormenta densa de cuadros y rombos geométricos + Estrellas veloces"""
    background_gradient(img, t, h0=0, h1=30)
    
    # Fondo extra: Estrellas moviéndose horizontalmente rápidas
    num_fast_stars = 40
    state_rng = np.random.default_rng(555)
    st_xs = (state_rng.integers(0, W, num_fast_stars) + int(t * 180)) % W
    st_ys = state_rng.integers(0, H, num_fast_stars)
    for i in range(num_fast_stars):
        cv2.line(img, (st_xs[i], st_ys[i]), (st_xs[i] + 4, st_ys[i]), (200, 200, 255), 1, cv2.LINE_AA)

    # Campo denso de primitivas combinadas
    n_particles = 220
    for i in range(n_particles):
        seed_x = (i * 8.2)
        seed_y = (i * 11.7)
        
        x = int((seed_x + t * 50 + 60 * math.sin(t + seed_y)) % W)
        y = int((seed_y + t * 30 + 50 * math.cos(t * 0.6 + seed_x)) % H)
        
        size = int(6 + 5 * math.sin(t + i))
        color_p = hsv_to_bgr(int(t*12 + i), 230, 240)
        
        if i % 2 == 0:
            cv2.rectangle(img, (x - size, y - size), (x + size, y + size), color_p, -1)
        else:
            pts_p = np.array([[x, y - size], [x + size, y], [x, y + size], [x - size, y]], np.int32)
            cv2.fillPoly(img, [pts_p], color_p, cv2.LINE_AA)
            
    cv2.putText(img, "Primitivas Colectivas: Tormenta de Poligonos", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)
    
#------------------- FINAL - CÍRCULOS CON LÍNEAS DEFORMADAS Y EFECTO DE SHEAR -------------
def scene_final(img, t, scale=0.9): 
    background_radial(img, t, 140) 
    cx, cy = W // 2, H // 2
    R = int(120 * scale) 
    col = hsv_to_bgr(int(145 + 25 * np.sin(t * 0.5)), 220, 245) 
    deform = 1.0 + 0.08 * math.sin(t * 1.2) 

    r_esquina = int(45 + 6 * math.sin(t * 2.5)) # Círculos que pulsan en las esquinas
    col_esquina = hsv_to_bgr(int(140 + 10 * math.sin(t * 0.5)), 170, 150)
    esquinas = [(0, 0), (W, 0), (0, H), (W, H)]
    
    for ex, ey in esquinas:
        cv2.circle(img, (ex, ey), r_esquina, col_esquina, 1, cv2.LINE_AA)
        cv2.circle(img, (ex, ey), r_esquina + 15, col_esquina, 1, cv2.LINE_AA)
        # Líneas de encuadre (miras telescópicas)
        dx = 35 if ex == 0 else -35
        dy = 35 if ey == 0 else -35
        cv2.line(img, (ex, ey), (ex + dx, ey), col_esquina, 1, cv2.LINE_AA)
        cv2.line(img, (ex, ey), (ex, ey + dy), col_esquina, 1, cv2.LINE_AA)

    # --- LA FLOR ORIGINAL ---
    for i in range(6): 
        angle = i * math.pi * 2 / 6 + t * 0.35 
        x = int(cx + R / 1.8 * math.cos(angle)) 
        y = int(cy + R / 1.8 * math.sin(angle)) 
        axes = (int((R / 1.3) * deform), int(R / 6))
        cv2.ellipse(img, (x, y), axes, math.degrees(angle), 0, 360, col, 2, cv2.LINE_AA) 
    
    cv2.circle(img, (cx, cy), int(R / 3), col, 2, cv2.LINE_AA) 
        
    shear = affine_shear(img, 0.18 * math.sin(t)) 
    img[:] = cv2.addWeighted(img, 0.7, shear, 0.3, 0)

    cv2.putText(img, "Curva 5: Composicion Eliptica con Shear Dinamico", 
                (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                (240, 240, 240), 1, cv2.LINE_AA)
    
# ------------------------------------------------------------
# CONTROLADOR DE ESCENAS
# ------------------------------------------------------------
def render_scene(buf, scene_id, t, rng):
    if scene_id == 0: # BIEN 1
        scene_credits(buf, t)
    elif scene_id == 1: # BIEN 2
        scene_lotus(buf, t, scale=1.7)     
    elif scene_id == 2: # BIEN 3
        scene_rose_polar(buf, t, scale=1.7) 
    elif scene_id == 3: # BIEN 4
        scene_spirograph(buf, t, scale= 2)
    elif scene_id == 4: # FALLO
        scene_star(buf, t, scale= 2)
    elif scene_id == 5: # BIEN 5
        scene_final(buf, t, scale=1.9)
        
# ------------------------------------------------------------
# TIMELINE GENERAL - 6 escenas de 10 segundos = 60 segundos
# ------------------------------------------------------------
def timeline(t, rng, bufA, bufB):
    
    block = int(min(5, max(0, t // 10))) 
    t_in = t - block*10

    render_scene(bufA, block, t, rng)
    frame = bufA

    if block < 5 and t_in >= 9.5 : 
        render_scene(bufA, block, t, rng)
        render_scene(bufB, block+1, t, rng)
        a = smoothstep(9.5 , 10.0, t_in)
        frame = cv2.addWeighted(bufA, 1-a, bufB, a, 0)
        flash = smoothstep(9.7, 10.0, t_in)
        if flash > 0:
            frame = cv2.addWeighted(frame, 1.0, np.full_like(frame, 255), 0.1*flash, 0)

    # Fade in/out global
    fin = smoothstep(0.0, 1.5, t)
    fout = 1.0 - smoothstep(DURATION - 1.5, DURATION, t)
    f = fin * fout
    if f < 0.999:
        frame = (frame.astype(np.float32) * f).astype(np.uint8)
    return frame

def main():
    rng = np.random.default_rng(123)
    bufA = np.zeros((H, W, 3), np.uint8)
    bufB = np.zeros((H, W, 3), np.uint8)

    writer = cv2.VideoWriter('demo_final.mp4', cv2.VideoWriter_fourcc(*'mp4v'), FPS, (W,H))

    total_frames = int(DURATION * FPS)
    t0 = time.perf_counter()
    for i in range(total_frames):
        t = i / FPS
        frame = timeline(t, rng, bufA, bufB)
        frame = post_vignette(frame, 0.5)
        frame = post_scanlines(frame, 0.12)
        frame = post_posterize(frame, 24)
        writer.write(frame)
        cv2.imshow("Proyecto Final: demo procedural (OpenCV)", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    writer.release()
    print("Tiempo:", time.perf_counter() - t0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()