import time, math
import numpy as np
import cv2

W, H = 800, 600
FPS = 30
DURATION = 60.0 

def clamp01(x): 
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

def smoothstep(a, b, x):
    x = clamp01((x - a) / (b - a))
    return x * x * (3 - 2 * x)

def hsv_to_bgr(h, s, v):
    hsv = np.uint8([[[h % 180, np.clip(s, 0, 255), np.clip(v, 0, 255)]]])
    return tuple(int(x) for x in cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0, 0])


# TRANSFORMACIONES MATRICIALES
def affine_shear(img, amount):
    M = np.float32([[1, amount, 0], [0, 1, 0]])
    return cv2.warpAffine(img, M, (W, H))

# FILTROS DE POST-PROCESADO
def post_vignette(img, strength=0.7):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - W * 0.5) / (W * 0.5)
    ny = (yy - H * 0.5) / (H * 0.5)
    r2 = nx * nx + ny * ny
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


# FONDOS DINÁMICOS PROCEDURALES
def background_solid(img, t, hue_base, sat=220, val=100):
    """Fondo sólido que cambia de color lentamente"""
    hue = (hue_base + int(t * 10)) % 180
    color = hsv_to_bgr(hue, sat, val)
    img[:] = color

def background_gradient(img, t, h0=130, h1=170):
    """Fondo dinámico procedural usando gradiente vertical en HSV"""
    hsv = np.zeros((H, W, 3), np.uint8)
    ys = np.linspace(0, 1, H, dtype=np.float32)
    hue = (h0 + (h1 - h0) * ys + 8 * np.sin(t * 0.5 + ys * 3.0)).astype(np.float32)
    hsv[:, :, 0] = np.clip(hue, 0, 179).astype(np.uint8)[:, None]
    hsv[:, :, 1] = 180
    hsv[:, :, 2] = (30 + 90 * (1 - ys)).astype(np.uint8)[:, None]
    img[:] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def background_wave_mesh(img, t, base_hue=140):
    """Fondo dinámico: Malla de ondas cinéticas abstractas que mutan con el tiempo"""
    hsv = np.zeros((H, W, 3), np.uint8)
    yy, xx = np.mgrid[0:H:15, 0:W:15]
    
    deformacion = np.sin(xx * 0.01 + t * 1.5) * np.cos(yy * 0.01 + t * 1.2)
    h_map = (base_hue + 25 * deformacion).astype(np.uint8)
    v_map = (45 + 50 * np.sin(yy * 0.02 + t)).astype(np.uint8)
    
    img[:] = hsv_to_bgr(base_hue, 160, 30) 
    for i in range(h_map.shape[0]):
        for j in range(h_map.shape[1]):
            pt_x = xx[i, j] + int(10 * np.sin(t + yy[i, j]))
            pt_y = yy[i, j] + int(10 * np.cos(t + xx[i, j]))
            color = hsv_to_bgr(int(h_map[i, j]), 200, int(v_map[i, j]))
            cv2.circle(img, (pt_x, pt_y), 1, color, -1)

def background_radial(img, t, hue_base):
    """Fondo dinámico: Ondas cinéticas concéntricas en constante expansión armónica"""
    hue = (hue_base + int(t * 6)) % 180
    img[:] = hsv_to_bgr(hue, 180, 40)
    cx, cy = W // 2, H // 2
    color_c = hsv_to_bgr((hue + 20) % 180, 150, 70)
    for r in range(60, 600, 70):
        dr = int(r + 20 * math.sin(t * 2.5 + r * 0.04))
        if dr > 0:
            cv2.circle(img, (cx, cy), dr, color_c, 1, cv2.LINE_AA)

def draw_stars(img, t, rng_seed=42, num_stars=80):
    """Efecto ambiental de fondo: Campo de estrellas titilantes"""
    rng = np.random.default_rng(rng_seed)
    xs = rng.integers(0, W, num_stars)
    ys = rng.integers(0, H, num_stars)
    sizes = rng.integers(1, 3, num_stars)
    for i in range(num_stars):
        blink = int(150 + 105 * math.sin(t * 3.0 + i))
        cv2.circle(img, (int(xs[i]), int(ys[i])), int(sizes[i]), (blink, blink, blink), -1)

def draw_cosmic_dust(img, t, seed=999):
    """Efecto ambiental de fondo: Partículas de polvo oscilando en microvórtices"""
    rng = np.random.default_rng(seed)
    n = 60
    xs = rng.integers(0, W, n)
    ys = rng.integers(0, H, n)
    for i in range(n):
        dx = int(12 * math.sin(t * 2.0 + i))
        dy = int(12 * math.cos(t * 1.5 + i))
        val = int(130 + 125 * math.sin(t * 4.0 + i))
        cv2.circle(img, (int(xs[i] + dx) % W, int(ys[i] + dy) % H), 1, (val, val, val), -1)


# ESCENAS DEL TIMELINE

#------ Escena 1: Introducción y títulos del proyecto ------
def scene_credits(img, t):
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

    cv2.putText(img, titulo, ((W - size1[0]) // 2, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (245, 245, 245), 2, cv2.LINE_AA)
    cv2.putText(img, subtitulo, ((W - size2[0]) // 2, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (220, 220, 220), 2, cv2.LINE_AA)
    cv2.putText(img, nombre, ((W - size3[0]) // 2, 360), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.85, (220, 220, 220), 2, cv2.LINE_AA)
    
  #----- ESCENA 2: Lotus Orbital ------  
def scene_lotus(img, t, scale=1.7):
    background_wave_mesh(img, t, base_hue=25) 
    draw_cosmic_dust(img, t, seed=44)
    
    cx, cy = W // 2, H // 2
    petals = 20
    freq_pulsar = 1.2 + 0.2 * math.sin(t * 3.5)
    radio_base = int(80 * freq_pulsar)
    
    for i in range(petals):
        ang = 2 * np.pi * i / petals + (t * 0.4)
        x = int(cx + radio_base * np.cos(ang))
        y = int(cy + radio_base * np.sin(ang))
        
        color_line = hsv_to_bgr(int(20 + i * 3), 240, 230)
        cv2.circle(img, (x, y), int(60 * freq_pulsar), color_line, 1, cv2.LINE_AA)
        cv2.circle(img, (x, y), 3, (255, 255, 255), -1, cv2.LINE_AA)
        
    cv2.putText(img, "Curva 1: Lotus Orbital ", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 255, 220), 1, cv2.LINE_AA)

 # ---- ESCENA 3: Rosa Polar  ------   
def scene_rose_polar(img, t, scale=1):
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
        
    cv2.putText(img, "Curva 2: Rosa Polar con Anillo Exterior ", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 255, 220), 1, cv2.LINE_AA)

# ---- ESCENA 4: Espirógrafo con Ondas de Choque ------
def scene_spirograph(img, t, scale=1.3):
    background_wave_mesh(img, t, base_hue=5) 

    cx, cy = W // 2, H // 2
    R = int(min(W, H) * 0.07 * scale)
    R2 = int(R * 1.732)
    rotacion_total = t * 0.2
    col = hsv_to_bgr(int(30 + 40 * math.sin(t * 0.5)), 210, 235)
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
    theta_max = min(2 * np.pi, t_local * 1.8)
    paso = max(0.005, 0.08 - t_local * 0.01)

    if theta_max > 0:
        for ang in np.arange(0, theta_max, paso):
            x = int(cx + radio * np.cos(ang + rotacion))
            y = int(cy + radio * np.sin(ang + rotacion))
            cv2.circle(img, (x, y), 2, col_circulo, -1)

    col_magia = hsv_to_bgr(int(t * 25 % 180), 240, 255)
    
    puntas = 8
    pts_estrella = []
    for i in range(puntas * 2):
        ang_e = i * (math.pi / puntas) - t * 0.6
        r_e = (radio + 130) if i % 2 == 0 else (radio + 40 + int(60 * math.sin(t * 3.5)))
        pts_estrella.append([int(cx + r_e * math.cos(ang_e)), int(cy + r_e * math.sin(ang_e))])
    
    cv2.polylines(img, [np.array(pts_estrella, np.int32)], True, col_magia, 2, cv2.LINE_AA)

    radio_pulso = int((t * 120) % 180) 
    for ex, ey in [(0, 0), (W, 0), (0, H), (W, H)]:
        cv2.circle(img, (ex, ey), radio_pulso, col_magia, 1, cv2.LINE_AA)
        cv2.circle(img, (ex, ey), max(0, radio_pulso - 60), col_magia, 1, cv2.LINE_AA)
        cv2.circle(img, (ex, ey), max(0, radio_pulso - 120), col_magia, 1, cv2.LINE_AA)

    cv2.putText(img, "Curva 4: Sistema de Espirografo y Ondas", 
                (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 255, 220), 1, cv2.LINE_AA)

#---- ESCENA 4: Campo Glitch de Primitivas Geométricas ------
def scene_glitch(img, t, scale=1.3):
    background_solid(img, t, 140, 200, 20) 
    
    num_figuras = 180  
    lifespan = 0.85 
    
    for i in range(num_figuras):
        t_active = t + (i * 0.317) 
        cycle = int(t_active // lifespan)
        p = (t_active % lifespan) / lifespan
        
        seed = i * 789 + cycle * 314
        px = (seed * 137) % W
        py = (seed * 149) % H
        tipo_figura = seed % 4
        hue = (seed * 47) % 180
        size = 4 + (seed % 10) 
        
        is_visible = False
        offset_x = 0 
        
        if p < 0.65:
            is_visible = True
        elif p < 0.95:
            if (int(p * 150) + seed) % 3 == 0:
                is_visible = True
                offset_x = (seed % 15) - 7 
        
        if not is_visible:
            continue
            
        color = hsv_to_bgr(hue, 240, 255)
        
        x = px + offset_x
        y = py
        
        # Renderizado
        if tipo_figura == 0:
            cv2.circle(img, (x, y), size, color, -1)
        elif tipo_figura == 1:
            cv2.rectangle(img, (x - size, y - size), (x + size, y + size), color, -1)
        elif tipo_figura == 2:
            pts = np.array([[x, y - int(size*1.2)], [x + size, y + size], [x - size, y + size]], np.int32)
            cv2.fillPoly(img, [pts], color)
        elif tipo_figura == 3:
            # Cruz de píxeles gruesa
            cv2.line(img, (x - size, y), (x + size, y), color, max(1, size//2))
            cv2.line(img, (x, y - size), (x, y + size), color, max(1, size//2))

    cv2.putText(img, "Primitivas: Campo Glitch", 
                (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 255, 200), 1, cv2.LINE_AA)
    
# ---- ESCENA 5: Estrella de 5 puntas ------
def scene_final(img, t, scale=0.9): 
    background_radial(img, t, 140) 
    cx, cy = W // 2, H // 2
    R = int(120 * scale) 
    col = hsv_to_bgr(int(145 + 25 * np.sin(t * 0.5)), 220, 245) 
    deform = 1.0 + 0.08 * math.sin(t * 1.2) 

    # Flores miniatura en las esquinas con mayor grosor y brillo para que resalten
    r_esquina = int(28 + 4 * math.sin(t * 2.0))
    col_esquina = hsv_to_bgr(int(140 + 10 * math.sin(t * 0.5)), 220, 245)
    esquinas = [(45, 45), (W - 45, 45), (45, H - 45), (W - 45, H - 45)]
    
    for ex, ey in esquinas:
        for j in range(4):
            ang_e = j * math.pi / 2 + t * 0.6
            ex_p = int(ex + (r_esquina / 2) * math.cos(ang_e))
            ey_p = int(ey + (r_esquina / 2) * math.sin(ang_e))
            cv2.ellipse(img, (ex_p, ey_p), (r_esquina, r_esquina // 4), math.degrees(ang_e), 0, 360, col_esquina, 2, cv2.LINE_AA)
        cv2.circle(img, (ex, ey), r_esquina // 3, col_esquina, -1, cv2.LINE_AA)

    # Anillo exterior discontinuo con mayor grosor de puntos y alta luminosidad
    r_orbita = int(R * 1.45)
    col_orbita = hsv_to_bgr(int(145 + 15 * math.sin(t)), 240, 255)
    for a_idx in range(16):
        ang_o = a_idx * (2 * math.pi / 16) - t * 0.4
        ox = int(cx + r_orbita * math.cos(ang_o))
        oy = int(cy + r_orbita * math.sin(ang_o))
        cv2.circle(img, (ox, oy), 4, col_orbita, -1, cv2.LINE_AA)

    # Flor central principal (mantiene intacta su escala y posición)
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
    if scene_id == 0: 
        scene_credits(buf, t)
    elif scene_id == 1: 
        scene_lotus(buf, t, scale=1.7)     
    elif scene_id == 2: 
        scene_rose_polar(buf, t, scale=1.7) 
    elif scene_id == 3: 
        scene_spirograph(buf, t, scale=2)
    elif scene_id == 4: 
        scene_glitch(buf, t, scale=2)
    elif scene_id == 5: 
        scene_final(buf, t, scale=1.9)

# ------------------------------------------------------------
# TIMELINE Y ACOPLE GENERAL
# ------------------------------------------------------------
def timeline(t, rng, bufA, bufB):
    block = int(min(5, max(0, t // 10))) 
    t_in = t - block * 10

    render_scene(bufA, block, t, rng)
    frame = bufA

    if block < 5 and t_in >= 9.5: 
        render_scene(bufA, block, t, rng)
        render_scene(bufB, block + 1, t, rng)
        a = smoothstep(9.5, 10.0, t_in)
        frame = cv2.addWeighted(bufA, 1 - a, bufB, a, 0)
        flash = smoothstep(9.7, 10.0, t_in)
        if flash > 0:
            frame = cv2.addWeighted(frame, 1.0, np.full_like(frame, 255), 0.1 * flash, 0)

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

    writer = cv2.VideoWriter('demo_final.mp4', cv2.VideoWriter_fourcc(*'mp4v'), FPS, (W, H))

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
    print("Tiempo total de renderizado:", time.perf_counter() - t0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()