import cv2 as cv
import numpy as np
import threading
import time
import random
import requests
from playsound import playsound





end=False
count=True
sendable=True
snaps=0
url='http://127.0.0.1:8000/api/capture-frame/'
is_alert_playing=False
def alert():
    print(f'DUDE {threading.current_thread().name}')
    global is_alert_playing
    is_alert_playing=True
    playsound("C:/Users/Dayod/Downloads/395400__wolfercz__siren.wav")
    is_alert_playing=False
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
            if(count%200==0):
                sendable=True

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
        if(not is_alert_playing):
            print('inside')
            alert_thread=threading.Thread(target=alert)
            alert_thread.start()
        (x,y,w,h)=cv.boundingRect(contour)
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        if(sendable):
            if(snaps<300):
                if(snaps%100==0):
                    capture_no=random.randint(0,5000)
                    capture_name=f'captured_{capture_no}.png'
                    cv.imwrite(capture_name,frame)
                    image=open(capture_name,'rb')
                    print(image)
                    file={'captured_frame':image}
                    # requests.post(url=url,files=file)

                snaps+=1
                print(snaps)
            else:
                sendable=False
                snaps=0
                

    cv.imshow('Frame',frame)

    key=cv.waitKey(5)
    if(key==ord('d')):
        end=True
        break

video_capture.release()
cv.destroyAllWindows()
