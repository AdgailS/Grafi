import numpy as np
import cv2 as cv

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt2.xml')
cap = cv.VideoCapture(0)
x=y=w=h= 0 
count = 0
while True:
    ret, img = cap.read()
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)
    for(x,y,w,h) in rostros:
        res = int((w+h)/8)
        #img = cv.rectangle(img, (x,y), (x+w, y+h), (234, 23,23), 5)
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 21, (0, 0, 0), 2 )
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 21, (0, 0, 0), 2 )
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 20, (255, 255, 255), -1 )
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 20, (255, 255, 255), -1 )
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 5, (0, 0, 255), -1 )
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 5, (0, 0, 255), -1 )
       # CEJAS
        img = cv.line(img, (x + int(w*0.2), y + int(h*0.20)), (x + int(w*0.4), y + int(h*0.20)), (0,0,0), 3) #izquierda
        img = cv.line(img, (x + int(w*0.6), y + int(h*0.20)), (x + int(w*0.8), y + int(h*0.20)), (0,0,0), 3) #derecha
        # NARIZ
        cv.ellipse(img, (x + int(w*0.5), y + int(h*0.55)), (12,18), 0, 0, 360, (0,0,255), -1)
        # BIGOTE 
        cv.ellipse(img, (x + int(w*0.45), y + int(h*0.70)), (20,8), 0, 0, 180, (0,0,0), 3)
        cv.ellipse(img, (x + int(w*0.55), y + int(h*0.70)), (20,8), 0, 0, 180, (0,0,0), 3)
        # OREJA IZQUIERDA
        cv.ellipse(img, (x - 15, y + int(h*0.5)), (25,40), 0, 0, 360, (150,180,255), -1)
        # OREJA DERECHA
        cv.ellipse(img, (x + w + 15, y + int(h*0.5)), (25,40), 0, 0, 360, (150,180,255), -1)
        
        img = cv.rectangle(img, (x+10,y+10), (x+w, y+h), (234,0 ,234), 5)
        
        
    img2=  img[y:y+h,x:x+w]
    cv.imshow('img2', img2)
    cv.imshow('img', img)
    if cv.waitKey(1)== ord('q'):
        break
cap.release()
cv.destroyAllWindows()

# DIBUJAR OJOS, BIGOTE, OREJAS Y CEJAS Y NARIZ