import cv2
import sys
import numpy as np

cap=cv2.VideoCapture(0)


count=0

while cap.isOpened():
    
    ret,frame=cap.read()

    if count!=20:
        cv2.imwrite("C:\\Users\\prath\\GUI_SIH\\images\\user\\q"+str(count)+".jpg",frame)
        #cv2.imwrite("/home/piyush/Gesture_detection/face_recognition/images/pratham/q"+str(count)+".jpg",frame)
        count=count+1
    else:
        break
    
    cv2.imshow('OpenCV Feed', frame)

    if cv2.waitKey(500) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()