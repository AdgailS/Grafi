import time, math
import numpy as np
import cv2

########### MI TRABAJO ################################
## //// LO QUE FALTA
# /// FRUIT OF LIFE - COMPLETADO

W, H = 800, 600
FPS = 30
DURATION = 80.0  # 8 escenas de 10 segundos

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
# EFECTOS POST-PROCESADO
# ------------------------------------------------------------
def post_vignette(img, strength=0.5):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - W*0.5) / (W*0.5)
    ny = (yy - H*0.5) / (H*0.5)
    r2 = nx*nx + ny*ny
    mask = np.clip(1.0 - strength * r2, 0.0, 1.0)
    out = (img.astype(np.float32) * mask[..., None]).astype(np.uint8)
    return out

def post_scanlines(img, strength=0.12):
    out = img.astype(np.float32)
    y = np.arange(H, dtype=np.float32)
    m = 1.0 - strength * (0.5 + 0.5*np.sin(2*np.pi*y/3.0))
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

# ------------------------------------------------------------
# ESCENAS
# ------------------------------------------------------------
def scene_credits(img, t):
    background_solid(img, t, 165, 200, 100)
    
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
def scene_lotus(img, t, scale= 3):
    background_solid(img, t, 140, 220, 85)
    cx, cy = W//2, H//2
    # Valor fijo para que la estrella no se deforme
    k = 1.6
    r = 55
    R = r * k
    # Efecto de respiración
    escala = 1.0 + 0.08 * math.sin(t * 2)
    pts = []

    for a in np.linspace(0, 20*np.pi, 2500):
        x = (R-r)*np.cos(a) + r*np.cos(((R-r)/r)*a)
        y = (R-r)*np.sin(a) - r*np.sin(((R-r)/r)*a)
        pts.append([int(cx + x * 2.5 * escala),int(cy + y * 2.5 * escala)])

    pts = np.array([pts], np.int32)

    color = hsv_to_bgr(int(120 + 50*np.sin(t*0.7)), 255, 255)

    cv2.polylines(img, pts, True, color, 2, cv2.LINE_AA)

    # Punto central brillante
    cv2.circle( img, (cx, cy), 5, color, -1, cv2.LINE_AA)

    # Rotación suave de toda la escena
    rot = affine_rotate(img, t * 12)

    img[:] = cv2.addWeighted(img, 0.6, rot, 0.4, 0)

    # Shear suave para cumplir transformación afín
    shear = affine_shear( img, 0.08 * math.sin(t))

    img[:] = cv2.addWeighted( img, 0.8, shear, 0.2, 0)

#------------------- ROSE POLAR - CÍRCULOS QUE SE DESINTEGRAN EN EL EXTERIOR ------------- YA COMPLETADO
def scene_rose_polar(img, t, scale=1):
    background_solid(img, t, 100, 210, 85)
    
    cx, cy = W//2, H//2
    R = int(min(W, H) * 0.12 * scale)
    radio = int(R * 2.2)
    rotacion = t * 0.3
    pulsacion = 1.0 + 0.04 * math.sin(t*2.0)

    col = hsv_to_bgr(int(45 + 30*math.sin(t*0.6)), 230, 245)
    col_circulo = hsv_to_bgr(180, 255, 255)

    cv2.circle(img, (cx, cy), int(R*pulsacion), col, 2, cv2.LINE_AA)

    for i in range(6):
        angle = i * math.pi * 2 / 6 + rotacion
        x = int(cx + R * math.cos(angle))
        y = int(cy + R * math.sin(angle))
        cv2.circle(img, (x, y), int(R*pulsacion), col, 2, cv2.LINE_AA)

    paso = 0.01
    t_local = max(0, t - 20)
    duracion = 3
    progreso = (t_local % duracion) / duracion
    borrado = progreso * 2*np.pi

    for ang in np.arange(0, 2*np.pi + paso, paso):
        x = int(cx + radio * np.cos(ang))
        y = int(cy + radio * np.sin(ang))

        if ang > borrado: 
            cv2.circle(img, (x, y), 2, col_circulo, -1)
        else:
            dx = np.cos(ang)
            dy = np.sin(ang)
            fuerza = min((borrado - ang) * 5, 10)
            px = int(x + dx * fuerza)
            py = int(y + dy * fuerza)
            px += np.random.randint(-2, 3)
            py += np.random.randint(-2, 3)
            cv2.circle(img, (px, py), 1, col_circulo, -1)

#------------------- SPIROGRAPH - CÍRCULOS DENTRO DE CÍRCULOS CON LÍNEAS CONECTIVAS ------------- YA COMPLETADO
def scene_spirograph(img, t, scale=0.9):
    background_solid(img, t, 30, 210, 90)

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
    t_local = t - 30
    rotacion = t_local * 0.8
    col_circulo = hsv_to_bgr(280, 255, 255)
    theta_max = min(2*np.pi, t_local * 1.8)
    paso = max(0.005, 0.08 - t_local * 0.01)

    for ang in np.arange(0, theta_max, paso):
        x = int(cx + radio * np.cos(ang + rotacion))
        y = int(cy + radio * np.sin(ang + rotacion))
        cv2.circle(img, (x, y), 2, col_circulo, -1)
        
        
#------------------- PARTICULAS - TRIÁNGULOS QUE ORBITAN Y SE DEFORMAN -------------
def scene_particles(img, t, rng, scale=1):
    background_solid(img, t, 220, 220, 75)

    cx, cy = W//2, H//2
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
        pts = triangulo(rot, True, angulos_up[i])
        col = hsv_to_bgr(300 + 20*i, 220, 240)
        cv2.polylines(img, pts, True, col, 2, cv2.LINE_AA)

    for i in range(5):
        rot = math.radians(angulos_down[i] * 100) - t*0.03
        pts = triangulo(rot, False, angulos_down[i])
        col = hsv_to_bgr(60 + 15*i, 220, 240)
        cv2.polylines(img, pts, True, col, 2, cv2.LINE_AA)
    
#------------------- FINAL - CÍRCULOS CON LÍNEAS DEFORMADAS Y EFECTO DE SHEAR -------------
def scene_final(img, t, scale=0.9): 
    background_solid(img, t, 140, 220, 85) 
    cx, cy = W//2, H//2 
    R = int(120 * scale) 
    col = hsv_to_bgr(int(145 + 25*np.sin(t*0.5)), 220, 245) 
    deform = 1.0 + 0.08 * math.sin(t*1.2) 
    
    for i in range(6): 
        angle = i * math.pi * 2 / 6 + t * 0.35 
    
    x = int(cx + R/1.8 * math.cos(angle)) 
    y = int(cy + R/1.8 * math.sin(angle)) 
    axes = (int((R/1.3)*deform), int(R/6)) 
    cv2.ellipse(img, (x, y), axes, math.degrees(angle), 0, 360, col, 2, cv2.LINE_AA) 
    cv2.circle(img, (cx, cy), int(R/3), col, 2, cv2.LINE_AA) 
    
    shear = affine_shear(img, 0.18 * math.sin(t)) 
    img[:] = cv2.addWeighted(img,0.7,shear,0.3,0)

#------------------- FRUIT OF LIFE - 13 CÍRCULOS INTERCONECTADOS FORMANDO UNA FLOR DE LA VIDA -------------
def scene_fruit_of_life(img, t, scale=1.1):
    """Fruit of Life - 13 círculos interconectados formando una flor de la vida"""
    background_solid(img, t, 320, 230, 80)
    cx, cy = W//2, H//2
    R = int(100 * scale)
    
    # Colores que cambian con el tiempo
    col_principal = hsv_to_bgr(int(45 + 20*math.sin(t*0.5)), 255, 245)
    col_secundario = hsv_to_bgr(int(180 + 30*math.sin(t*0.7)), 240, 230)
    col_terciario = hsv_to_bgr(int(300 + 25*math.sin(t*0.6)), 235, 240)
    
    # Centro
   # cv2.circle(img, (cx, cy), R, col_principal, 2, cv2.LINE_AA)
   # cv2.circle(img, (cx, cy), int(R*0.25), col_principal, -1)
    
    # Primer anillo (6 círculos alrededor del centro)
    angulos = [0, 60, 120, 180, 240, 300]
    radio_anillo1 = R
    
    for ang in angulos:
        ang_rad = math.radians(ang)
        x = int(cx + radio_anillo1 * math.cos(ang_rad))
        y = int(cy + radio_anillo1 * math.sin(ang_rad))
        cv2.circle(img, (x, y), R, col_secundario, 2, cv2.LINE_AA)
    
    # Segundo anillo (6 círculos adicionales)
    radio_anillo2 = R * 1.732  # sqrt(3) * R
    for ang in angulos:
        ang_rad = math.radians(ang + 30)
        x = int(cx + radio_anillo2 * math.cos(ang_rad))
        y = int(cy + radio_anillo2 * math.sin(ang_rad))
        cv2.circle(img, (x, y), R, col_terciario, 2, cv2.LINE_AA)
    
    # Líneas conectivas animadas
    """""
    for i in range(12):
        ang = i * 30
        ang_rad = math.radians(ang + t * 20)
        radio_linea = R * 1.2
        x1 = int(cx + radio_linea * math.cos(ang_rad - 0.3))
        y1 = int(cy + radio_linea * math.sin(ang_rad - 0.3))
        x2 = int(cx + radio_linea * math.cos(ang_rad + 0.3))
        y2 = int(cy + radio_linea * math.sin(ang_rad + 0.3))
        
        color_linea = hsv_to_bgr((320 + i * 15 + int(t*30)) % 180, 240, 250)
        cv2.line(img, (x1, y1), (x2, y2), color_linea, 1, cv2.LINE_AA)
    """

    # Partículas decorativas que orbitan
    for i in range(36):
        ang_part = i * 10 + t * 50
        ang_rad = math.radians(ang_part)
        radio_part = R * 2.2
        x = int(cx + radio_part * math.cos(ang_rad))
        y = int(cy + radio_part * math.sin(ang_rad))
        
        # Brillo pulsante
        brillo = 200 + 55 * math.sin(t*3 + i)
        color_part = hsv_to_bgr((ang_part + int(t*50)) % 180, 255, brillo)
        cv2.circle(img, (x, y), 3, color_part, -1)
        
    rot = affine_rotate(img, t*12)
    img[:] = cv2.addWeighted(img,0.6,rot,0.4,0)
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
        scene_spirograph(buf, t, scale=1.7)
    elif scene_id == 4:
        scene_particles(buf, t, rng, scale=1.7)
    elif scene_id == 5:
        scene_final(buf, t, scale=1.9)
    elif scene_id == 6:
        scene_fruit_of_life(buf, t, scale=1.2)

# ------------------------------------------------------------
# TIMELINE GENERAL - 7 escenas de 10 segundos = 70 segundos
# ------------------------------------------------------------
def timeline(t, rng, bufA, bufB):
    # 7 escenas (0..6) con transiciones entre ellas
    block = int(min(7, max(0, t // 10)))
    t_in = t - block*10

    render_scene(bufA, block, t, rng)
    frame = bufA

    # Transiciones entre escenas
    if block < 7 and t_in >= 8.8:
        render_scene(bufA, block, t, rng)
        render_scene(bufB, block+1, t, rng)
        a = smoothstep(8.8, 10.0, t_in)
        frame = cv2.addWeighted(bufA, 1-a, bufB, a, 0)
        flash = smoothstep(9.6, 10.0, t_in)
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