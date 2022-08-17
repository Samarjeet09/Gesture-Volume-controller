import cv2
import time
import handTrackingModule as handTM
import os

cam = cv2.VideoCapture(0)
cam.set(3,720)
cam.set(4,720)

detector = handTM.handDetector(detectionConfi=0.8)
cTime, pTime = 0, 0

tipIds=[4,8,12,16,20]
while True:
    success,img = cam.read()
    img = detector.findHands(img)

    landmarkList = detector.findPosition(img,draw=False)
    if(len(landmarkList)!=0):
        fingers = []

        # for thumb
        if (landmarkList[4][1] < landmarkList[3][1]):
            fingers.append(1)
        else:
            fingers.append(0)
        #  4 fingers
        for id in range(1,5):
            if(landmarkList[tipIds[id]][2]<landmarkList[tipIds[id]-2][2]):
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers=fingers.count(1)
        print(totalFingers)
        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)
    cTime = time.time()
    fps = 1/ (cTime-pTime)
    pTime= cTime
    cv2.putText(img,f'FPS:{int(fps)}',(10,40),cv2.FONT_HERSHEY_PLAIN,2 ,(69,69,420),2)

    cv2.imshow("FINGER COUNTER",img)
    cv2.waitKey(1)