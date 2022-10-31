import cv2 as cv
import numpy as np
import threading
import time

end=False
count=True
class CountDownThread(threading.Thread):
    
    def __init__(self) -> None:
        threading.Thread.__init__(self)


    def run(self):
        global count
        print(end)
        while True and end==False:
            print(f"Starting countdown")
            time.sleep(1)
            print(count)
            count+=1
        print('Thread exit')

video_capture=cv.VideoCapture(0)

first_frame=None
count_down_thread=CountDownThread()
count_down_thread.start()

while (True):
    isTrue,frame=video_capture.read()
    
    gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    gray=cv.GaussianBlur(gray,(21,21),0)
    if(first_frame is None):
        first_frame=gray
        continue
    delta_frame=cv.absdiff(first_frame,gray)

    threshold_frame=cv.threshold(delta_frame,50,255,cv.THRESH_BINARY)[1]
    threshold_frame=cv.dilate(threshold_frame,None,iterations=2)
    if(count%5==0):
        count+=1
        print("Reframed")
        first_frame=gray
    (contours,_)=cv.findContours(threshold_frame.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if(cv.contourArea(contour)<1000):
            continue
        (x,y,w,h)=cv.boundingRect(contour)
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)

    cv.imshow('Frame',frame)

    key=cv.waitKey(20)
    if(key==ord('d')):
        end=True
        break

video_capture.release()
cv.destroyAllWindows()
