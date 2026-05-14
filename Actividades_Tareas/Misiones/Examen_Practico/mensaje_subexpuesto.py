import cv2
import numpy as np

img = cv2.imread('Imagenes/m1_oscura.png', cv2.IMREAD_GRAYSCALE)

h, w = img.shape

img_final = np.zeros((h, w), dtype=np.uint8)

# --- MODO RAW ---
       
for y in range(h):
    for x in range(w):  
            pixel_original = img[y,x]
            nuevo_valor = int(pixel_original)*50
            img_final[y,x] = np.clip(nuevo_valor,0,255)
           

cv2.imshow('Original', img)
cv2.imshow('Revelada', img_final)


# --- MODO OPENCV ---
img_final_CV = img * 50
img_final_CV = np.clip(img_final_CV, 0, 255).astype(np.uint8)

cv2.imshow('Con OPENCV', img_final_CV)


cv2.waitKey(0)
cv2.destroyAllWindows()
