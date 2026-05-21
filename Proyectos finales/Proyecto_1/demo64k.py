import time, math
import numpy as np
import cv2

########### MI TRABAJO ################################
## //// LO QUE FALTA
# //// CAMBIAR FONDOS 
# /// AJUSTAR CIRCULO EXTERIOR FLOWER OF LIFE
# /// SRI YANTRA NO QUEDO
# ///  ROSA POLAR CHIQUITA/ CIRCULO EXTERIOR
# /// FRUIT OF LIFE NI SE MUESTRA
W, H = 800, 600
FPS = 30
DURATION = 70.0

angulos_up = [0.24, 0.21, 0.18, 0.15]
angulos_down = [0.22, 0.19, 0.16, 0.13, 0.10]

def clamp01(x): return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)
def smoothstep(a, b, x):
    x = clamp01((x - a) / (b - a))
    return x * x * (3 - 2 * x)

def poly_param(fx, fy, t0, t1, n, cx, cy, sx, sy): #//////////777 CURVA PARAMÉTRICA
    ts = np.linspace(t0, t1, n, dtype=np.float32)
    xs = fx(ts) * sx + cx
    ys = fy(ts) * sy + cy
    return np.round(np.stack([xs, ys], 1)).astype(np.int32).reshape((-1, 1, 2))

def hsv_to_bgr(h, s, v):  #///////////7 CAMBIA HSV A BGR
    # OpenCV: H en [0,179], S,V en [0,255] 
    hsv = np.uint8([[[h % 180, np.clip(s, 0, 255), np.clip(v, 0, 255)]]])
    return tuple(int(x) for x in cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0, 0])


# ------------------------------------------------------------
# EFECTOS POST-PROCESADO
# ------------------------------------------------------------
def post_vignette(img, strength=0.7):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - W*0.5) / (W*0.5)
    ny = (yy - H*0.5) / (H*0.5)
    r2 = nx*nx + ny*ny
    mask = np.clip(1.0 - strength * r2, 0.0, 1.0)
    out = (img.astype(np.float32) * mask[..., None]).astype(np.uint8)
    return out

def post_scanlines(img, strength=0.22): #/////////////// LINEAS DE MONITOR
    out = img.astype(np.float32)
    y = np.arange(H, dtype=np.float32)
    m = 1.0 - strength * (0.5 + 0.5*np.sin(2*np.pi*y/3.0))
    out *= m[:, None, None]
    return np.clip(out, 0, 255).astype(np.uint8)

def post_posterize(img, q=32): #///////////////////////// estilo artístico/cartoon.
    q = max(1, int(q))
    return ((img // q) * q).astype(np.uint8)


# ------------------------------------------------------------
# FONDO GRADIENTE HSV
# ------------------------------------------------------------
def background_hsv_gradient(img, t, hue0=10, hue1=140): #////////////////////////////
    # Degradado vertical en HSV para cambiar “ambiente” por escena
    hsv = np.zeros((H, W, 3), np.uint8) #// IMAGEN EN NEGRO
    ys = np.linspace(0, 1, H, dtype=np.float32) #// POSCICION DEL PIXEL
    hue = (hue0 + (hue1 - hue0) * ys + 10*np.sin(t*0.4 + ys*2.0)).astype(np.float32) ###// DEGRADADO
    hsv[:, :, 0] = np.clip(hue, 0, 179).astype(np.uint8)[:, None] #// ANIMACION
    hsv[:, :, 1] = 200 #/// COLOR
    hsv[:, :, 2] = (40 + 120*(1 - ys)).astype(np.uint8)[:, None] #// BRILLO
    img[:] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR) #// BGR



def scene_credits(img, t):
    background_hsv_gradient(img, t, hue0=165, hue1=105)
    rng = np.random.default_rng(1)
    xs = rng.integers(0, W, 380)
    ys = rng.integers(0, int(H*0.65), 380)
    img[ys, xs] = (255, 255, 255)
    img[:] = cv2.GaussianBlur(img, (0,0), 0.6)

    titulo = "DEMO FIGURAS GEOMETRICAS"
    subtitulo = "OpenCV + Matematicas"
    nombre = "Estrella Abigail"

    size1 = cv2.getTextSize(titulo, cv2.FONT_HERSHEY_SIMPLEX, 0.95, 2)[0]
    size2 = cv2.getTextSize(subtitulo, cv2.FONT_HERSHEY_SIMPLEX, 0.85, 2)[0]
    size3 = cv2.getTextSize(nombre, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.85, 2)[0]

    cv2.putText(img, titulo, ((W-size1[0])//2, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (245,245,245), 2, cv2.LINE_AA)
    cv2.putText(img, subtitulo, ((W-size2[0])//2, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (220,220,220), 2, cv2.LINE_AA)
    cv2.putText(img, nombre, ((W-size3[0])//2, 360), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.85, (220,220,220), 2, cv2.LINE_AA)

#///////////////// FRAME 1 /////////////////////////////
# ============================================================
# TORUS / LOTUS
# ============================================================

def scene_lotus(img, t, scale = 1.7): #/////////////// TERMINADA LOTUS OF LIFE /// CHECAR FONDO
    background_hsv_gradient(img, t, 160, 30)
    color = hsv_to_bgr(30, 240, 255)
    center = (400,300)
    petals = 24
    radio = int(90 * scale)
    
    for i in range(petals):
        ang = 2*np.pi*i/petals + t*0.2
        x = int(center[0] + radio * np.cos(ang))
        y = int(center[1] + radio * np.sin(ang))
        cv2.circle(img, (x,y), radio, color, 1, cv2.LINE_AA)
        
#///////////////// FRAME 2 /////////////////////////////
def scene_rose_polar(img, t, scale = 0.9): ##///////////////// SEED OF LIFE //// 2/3 BIEN
    background_hsv_gradient(img, t, hue0=100, hue1=60)

    cx, cy = W//2, H//2
    R = int(min(W, H) * 0.10 * scale)
    pulsacion = 1.0 + 0.05 * math.sin(t*2.0)
    col = hsv_to_bgr(int(45 + 30*math.sin(t*0.6)), 230, 245)
    cv2.circle(img, (cx, cy), int(R*pulsacion), col, 3, cv2.LINE_AA)

    for i in range(6):
        angle = i * math.pi * 2 / 6 + t*0.25
        x = int(cx + R * math.cos(angle))
        y = int(cy + R * math.sin(angle))
        cv2.circle(img, (x, y), int(R*pulsacion), col, 2, cv2.LINE_AA)

        
#///////////////// FRAME 3 /////////////////////////////
def scene_spirograph(img, t, scale = 0.9):
    background_hsv_gradient(img, t, hue0=50, hue1=10)

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

    cv2.circle(img, (cx, cy), int(R2+R), col, 2, cv2.LINE_AA)
    

#///////////////// FRAME 4 /////////////////////////////
def scene_particles(img, t, rng, scale = 0.9): #/////////// SRI YANTRA // INTENTO DE :(/// CHECAR SI SE ARREGLA
    background_hsv_gradient(img, t, hue0=140, hue1=180)

    cx, cy = W//2, H//2
    radios_up = [0.24, 0.21, 0.18, 0.15]
    radios_down = [0.22, 0.19, 0.16, 0.13, 0.10]
    zoom = 1.0 + 0.04 * math.sin(t*1.5)

    def triangulo(rotation, pointing_up, radio_val):
        R = int(min(W, H) * radio_val * scale * zoom)
        pts = []

        for i in range(3):
            angle = rotation + i * 2 * math.pi / 3

            if not pointing_up:
                angle += math.pi
                
            x = int(cx + R * math.cos(angle))
            y = int(cy + R * math.sin(angle))

            pts.append([x, y])
        return np.array([pts], np.int32)

    for i in range(4):
        rot = math.radians(angulos_up[i] * 100) + t*0.03
        pts = triangulo(rot, True, radios_up[i])
        col = hsv_to_bgr(300 + 20*i, 220, 240)
        cv2.polylines(img, pts, True, col, 2, cv2.LINE_AA)

    for i in range(5):
        rot = math.radians(angulos_down[i] * 100) - t*0.03
        pts = triangulo(rot, False, radios_down[i])
        col = hsv_to_bgr(60 + 15*i, 220, 240)
        cv2.polylines(img, pts, True, col, 2, cv2.LINE_AA)
        
        
#///////////////////// FRAME 5 /////////////////////////// ROSA POLAR
def scene_final(img, t, scale = 0.9):
    background_hsv_gradient(img, t, hue0=120, hue1=165)

    cx, cy = W//2, H//2

    R = int(120 * scale)

    col = hsv_to_bgr(int(145 + 25*np.sin(t*0.5)), 220, 245)

    deform = 1.0 + 0.08 * math.sin(t*1.2)

    for i in range(6):
        angle = i * math.pi * 2 / 6 + t * 0.35

        x = int(cx + R/1.8 * math.cos(angle))
        y = int(cy + R/1.8 * math.sin(angle))

        axes = (int((R/1.3)*deform), int(R/4))

        cv2.ellipse(img, (x, y), axes, math.degrees(angle), 0, 360, col, 2, cv2.LINE_AA)

    cv2.circle(img, (cx, cy), int(R/3), col, 2, cv2.LINE_AA)
    cv2.circle(img, (cx, cy), int(R * 1.15), col, 2, cv2.LINE_AA)
    
#///////////////// FRAME 6 /////////////////////////////
def scene_fire(img, t, state, scale = 0.9): #////FRUIT OF LIFE //// esta mal
    background_hsv_gradient(img, t, hue0=40, hue1=80)
 


# ------------------------------------------------------------
# CONTROLADOR DE ESCENAS
# ------------------------------------------------------------
def render_scene(buf, scene_id, t, rng, fire_state):
    if scene_id == 0:
        scene_credits(buf, t)
    elif scene_id == 1:
        scene_lotus(buf, t, scale = 1.4)     
    elif scene_id == 2:
        scene_rose_polar(buf, t, scale = 1.4) 
    elif scene_id == 3:
        scene_spirograph(buf, t, scale = 1.7) ##/// TAMAÑO
    elif scene_id == 4:
        scene_particles(buf, t, rng, scale = 1.5 )
    elif scene_id == 5:
        scene_final(buf, t, scale= 1.9)
    else:
        scene_fire(buf, t, fire_state, scale= 1.5)
        
        
# ------------------------------------------------------------
# TIMELINE GENERAL
# ------------------------------------------------------------
def timeline(t, rng, bufA, bufB, fire_state):
    # 6 escenas (0..5) con 5 transiciones entre ellas
    # Duración 60s -> 6 bloques de 10s
    block = int(min(6, max(0, t // 10)))
    t_in = t - block*10

    # Render escena base
    render_scene(bufA, block, t, rng, fire_state)
    frame = bufA

    # 5 transiciones: de s a s+1 en los últimos 1.2s de cada bloque
    if block < 6 and t_in >= 8.8: #/////////// 6 ESCENAS
        render_scene(bufA, block, t, rng, fire_state)
        render_scene(bufB, block+1, t, rng, fire_state)
        a = smoothstep(8.8, 10.0, t_in)
        frame = cv2.addWeighted(bufA, 1-a, bufB, a, 0)
        # pequeño “flash” al final de transición
        flash = smoothstep(9.6, 10.0, t_in)
        if flash > 0:
            frame = cv2.addWeighted(frame, 1.0, np.full_like(frame, 255), 0.12*flash, 0)

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

    fire_state = {
        "heat": np.zeros((H, W), np.float32),
        "rng": np.random.default_rng(999),
    }

    total_frames = int(DURATION * FPS)
    t0 = time.perf_counter()
    for i in range(total_frames):
        t = i / FPS
        frame = timeline(t, rng, bufA, bufB, fire_state)
        frame = post_vignette(frame, 0.72)
        frame = post_scanlines(frame, 0.16)
        frame = post_posterize(frame, 24)
        cv2.imshow("Proyecto Final: demo procedural (OpenCV)", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    print("Tiempo:", time.perf_counter() - t0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()