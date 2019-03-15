import numpy as np
import cv2 as cv
import imutils
    
MOT_THRESHOLD =30 #чувств


vid = cv.VideoCapture('007.mp4') #выбор камеры

fps = vid.get(cv.CAP_PROP_FPS) #выбор fps
cont_Start = []     #init of list
cont_Start2 = []
extLeftOld = [0,0]
extRightOld = [0,0]
extTopOld = [0,0]
extBotOld = [0,0]
SpeedOld = 0.0

while(vid.isOpened()):  #while file is open
    ret, frame = vid.read()  #чтение первого кадра     
    pos_frame = vid.get(cv.CAP_PROP_POS_FRAMES) #положение кадра

    if frame is None:   #стоп, если видео кончилось
        break
    
    prev_frame=frame[:]     #сохран
    ret, frame = vid.read() #чтение второго карра

    
    if frame is None:   #стоп, если видео кончилось
        break
    
    #изменённый кадр
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(hsv,(3,3),-1)
    #предыдущий  
    hsvPr = cv.cvtColor(prev_frame, cv.COLOR_BGR2GRAY)
    

    diff = cv.absdiff( blur,hsvPr) #ищем разницу между этими двумя
     
    ret2, thres = cv.threshold( diff, MOT_THRESHOLD, 255, 0)  #ищём активность
    thres =  cv.morphologyEx(thres, cv.MORPH_OPEN, np.ones((5,5),np.uint8)) #сглаживание маленьких полигонов
    thres = cv.morphologyEx(thres, cv.MORPH_CLOSE, np.ones((5,5),np.uint8)) #больших

    #ищем контуры
    thres, contours, hierarchy = cv.findContours(thres,1, 2)
    
    
            
    cnts = cv.findContours(thres.copy(), cv.RETR_EXTERNAL,
	cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    
    if cnts:
        
        c = max(cnts, key=cv.contourArea)
        # определение экстремальных точкек вдоль контура
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])

        Speed = (((extLeft[0]-extLeftOld[0] + extRight[0]-extRightOld[0] +
              extTop[0] - extTopOld[0] + extBot[0]-extBotOld[0])/2) + SpeedOld)/2

        
        try:
            cv.putText(thres,  str(Speed), (20,50), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        except:
            print("NO TEXT")
        
        extLeftOld = extLeft
        extRightOld = extRight
        extTopOld = extTop
        extBotOld = extBot
        SpeedOld = Speed
        
        # is green, top-most is blue, and bottom-most is teal
       # cv.drawContours(frame, [c], -1, (0, 255, 255), 2)
        #cv.circle(thres, extLeft, 8, (0, 0, 255), -1)
        #cv.circle(thres, extRight, 8, (0, 255, 0), -1)
        #cv.circle(thres, extTop, 8, (255, 0, 0), -1)
        #cv.circle(thres, extBot, 8, (255, 255, 0), -1)

        
                
    #cv.drawContours(frame, cont_Start2 , -1, (255,0,255), 2) #draw first
    cv.drawContours(thres, contours , -1, (255,0,0), 2)  #draw second
    #cv.drawContours(frame, hull , -1, (0,0,0), 2)  #draw second
    cv.imshow('video',thres) #show video 

    
    if cv.waitKey(1) & 0xFF == ord('q'): 
          break    
    cv.waitKey(50)
    

vid.release()
cv.destroyAllWindows()

