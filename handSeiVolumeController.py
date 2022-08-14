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
wCam, hCam= 480,480
cTime , pTime = 0,0
##########################################

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector = handTM.handDetector(detectionConfi= 0.7,trackingConfi=0.6)
#################################################
# initalization of pycaw wali chiz
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#####################################################
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()
minVol = volumeRange[0]
maxVol = volumeRange[1]
vol =0
volPercentage = 0
volBar = 400
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    landmarkList = detector.findPosition(img,draw = False)
    if(len(landmarkList)!=0):
        # print(landmarkList[4],landmarkList[8])

        x1,y1 = landmarkList[4][1], landmarkList[4][2]
        x2, y2 = landmarkList[8][1], landmarkList[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),10,(420,69,420),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (420, 69, 420), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2), (420, 69, 420), 3)
        cv2.circle(img, (cx, cy), 6, (420, 69, 420), cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1) #inkei bich ka dist kei liye
        # print(length)
        # our hand range was btw 50 and 300
        # --> convert it to vol range -65 to 0
        # we use numpy ka function
        vol = np.interp(length,[25,155],[minVol,maxVol])
        volBar = np.interp(length,[25,155],[420,69])
        volPercentage = np.interp(length, [25, 155], [0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length <50:
            cv2.circle(img, (cx, cy), 6, (0,255,89), cv2.FILLED)

    cv2.rectangle(img,(50,69),(75,420),(69,69,69),3)
    cv2.rectangle(img, (50, int(volBar)), (75, 420), (69, 420, 69), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (69, 420, 69), 2)


    cv2.imshow("Controlllllllll",img)
    cv2.waitKey(1)