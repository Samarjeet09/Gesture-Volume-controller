from operator import mod
import cv2
import time
import numpy as np
import handTrackingModule as handTM
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
##########################################
# space for parameters
wCam, hCam = 720, 480
cTime, pTime = 0, 0

##########################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = handTM.handDetector(detectionConfi=0.7, trackingConfi=0.6)
#################################################
# initalization of pycaw wali chiz
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#####################################################
# volume.GetMute()
# volume.GetMasterVolumeLevelScalar()
volumeRange = volume.GetVolumeRange()
minVol = volumeRange[0]
maxVol = volumeRange[1]
vol = 0
volPercentage = 0
volBar = 420
area = 0
# landmarkList=[]
colorVolume = (420, 420, 69)
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img,)
    # landmarkList, boundingBox = detector.findPosition(img, draw=True)
    if hands:
        hand1 = hands[0]
        landmarkList = hand1["lmList"]
        boundingBox = hand1['bbox']
        if(len(landmarkList) != 0):
            # print(landmarkList[4],landmarkList[8])
            #  filter based on size
            # area = abs( (boundingBox[2]-boundingBox[0]) * \
            #     (boundingBox[3]-boundingBox[1]) ) //100
            area = boundingBox[2] * boundingBox[3] // 100
            # print(area)
            if 100 < area < 1000:
                # print("yes")
                if 100 < area < 250:
                    maxLength = 100
                    minLenght = 10
                else:
                    maxLength = 200
                    minLenght = 40

                # Find distance  between index and thumb
                length, lineInfo, img = detector.findDistance(
                    landmarkList[4][0:2], landmarkList[8][0:2], img)
                print(area,length)
                # convert length to volume
                volBar = np.interp(length, [minLenght, maxLength], [420, 69])
                volPercentage = np.interp(length, [minLenght, maxLength], [0, 100])
                # reduce resolution to make it smoother
                smoothness = 5
                volPercentage = smoothness * round(volPercentage/smoothness)
                # doing this for smoother values thori steps mei aaygi issie
                # check which fingers are up
                fingers = detector.fingersUp(hand1)
                # if pinky is down set the volume
                if fingers[4]:
                    volume.SetMasterVolumeLevelScalar(volPercentage/100, None)
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),
                               6, (0, 255, 89), cv2.FILLED)  # indication ki vol set karidya
                    cv2.putText(img, f'setting mode', (100, 69),
                                cv2.FONT_HERSHEY_PLAIN, 2, (69, 420, 69), 2)
                    colorVolume = (420, 69, 420)
                else:
                    colorVolume = (420, 420, 69)

                # print(length)
                # our hand range was btw 50 and 300
                # --> convert it to vol range -65 to 0
                # we use numpy ka function

                if length < 50:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),
                               6, (420, 69, 69), cv2.FILLED)

     # drawings
    cv2.rectangle(img, (50, 69), (75, 420), (69, 69, 69), 3)
    cv2.rectangle(img, (50, int(volBar)), (75, 420),
                  (69, 420, 420), cv2.FILLED)
    currentVol = int(volume.GetMasterVolumeLevelScalar()*100)
    cv2.putText(img, f'Set Volume:{int(currentVol)}%', (400, 69),
                cv2.FONT_HERSHEY_PLAIN, 2, colorVolume, 2)
    cv2.putText(img, f'{int(volPercentage)}%', (30, 450),
                cv2.FONT_HERSHEY_PLAIN, 2, (69, 420, 69), 2)

    # frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 50),
                cv2.FONT_HERSHEY_PLAIN, 2, (69, 420, 69), 2)

    cv2.imshow("Controlllllllll", img)
    cv2.waitKey(1)
