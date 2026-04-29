import cv2
import mediapipe as mp
import math
import numpy as np

def dibujar_flor(frame, cx, cy, distancia):
    """Dibuja una flor cuyo tamaño varia en la posicion de los dedos"""
    
    
    tamano = max(30, min(int(distancia * 1.5), 300))  # Tamaño entre 30 y 300
    tamano_petalo = tamano // 3
    tamano_centro = tamano // 4
    
    # Colores
    color_petalo = (255, 100, 200)  
    color_centro = (0, 255, 255)    
    color_tallo = (0, 200, 0)       
    color_contorno = (0, 0, 0)    
    
    grosor = max(2, tamano // 40)
    
    # Tallo
    inicio_tallo = (cx, cy + tamano // 2)
    fin_tallo = (cx, cy + tamano)
    cv2.line(frame, inicio_tallo, fin_tallo, color_tallo, grosor * 2)
    
    # Hojas
    altura_hoja = cy + int(tamano * 0.7)
    
    #  izquierda
    puntos_hoja_izq = np.array([
        [cx, altura_hoja],
        [cx - tamano//3, altura_hoja - tamano//4],
        [cx, altura_hoja - tamano//6]
    ], np.int32)
    cv2.fillPoly(frame, [puntos_hoja_izq], color_tallo)
    
    # derecha
    puntos_hoja_der = np.array([
        [cx, altura_hoja],
        [cx + tamano//3, altura_hoja - tamano//4],
        [cx, altura_hoja - tamano//6]
    ], np.int32)
    cv2.fillPoly(frame, [puntos_hoja_der], color_tallo)
    
    # Pétalos
    angulos = [0, 60, 120, 180, 240, 300]  # 60 grados entre cada uno
    
    for angulo in angulos:
        rad = math.radians(angulo)
        # Posicion
        petalo_cx = cx + int(tamano_petalo * math.cos(rad))
        petalo_cy = cy + int(tamano_petalo * math.sin(rad))
        
        # que sean alargados 
        ejes_petalo = (tamano_petalo, tamano_petalo // 2)
        cv2.ellipse(frame, (petalo_cx, petalo_cy), ejes_petalo, 
                    angulo, 0, 360, color_petalo, -1)
        cv2.ellipse(frame, (petalo_cx, petalo_cy), ejes_petalo, 
                    angulo, 0, 360, color_contorno, grosor)
    
    # centro
    cv2.circle(frame, (cx, cy), tamano_centro, color_centro, -1)
    cv2.circle(frame, (cx, cy), tamano_centro, color_contorno, grosor)
    
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE, 
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),       # Pulgar
    (0, 5), (5, 6), (6, 7), (7, 8),       # Índice
    (5, 9), (9, 10), (10, 11), (11, 12),  # Medio
    (9, 13), (13, 14), (14, 15), (15, 16),# Anular
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # Meñique
]

cap = cv2.VideoCapture(0)
distancia = 50

with HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        
        results = landmarker.detect(mp_image)
        
        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                keypoints = []
              
                for landmark in hand_landmarks:
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    keypoints.append((cx, cy))
                    # ELIMINADO: ya no se dibujan los círculos azules en los puntos
                
                for connection in HAND_CONNECTIONS:
                    start_idx = connection[0]
                    end_idx = connection[1]
                    cv2.line(frame, keypoints[start_idx], keypoints[end_idx], (0, 255, 0), 2)
                
                if len(keypoints) >= 9: 
                    x1, y1 = keypoints[4]  # Pulgar
                    x2, y2 = keypoints[8]  # Índice
                    
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    # ELIMINADOS: ya no se dibujan los círculos rojos en pulgar e índice
                    
                    distancia = math.hypot(x2 - x1, y2 - y1)
                    cx_medio, cy_medio = (x1 + x2) // 2, (y1 + y2) // 2
                    cv2.putText(frame, f"{int(distancia)} px", (cx_medio, cy_medio), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        
        # flor en el centro
        centro_x = int(w / 2)
        centro_y = int(h / 2)
        
        dibujar_flor(frame, centro_x, centro_y, distancia)
      
        cv2.imshow("Flor", frame)
        
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

cap.release()
cv2.destroyAllWindows()