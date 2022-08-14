import cv2
import mediapipe as mp
import time

# to get a video capture object for the camera.
cap = cv2.VideoCapture(0)

# this is a formality to use mediapipe kei Hands wala obj
mpHands = mp.solutions.hands
hands = mpHands.Hands()
# we have a method to draw the landmarks
mpDraw = mp.solutions.drawing_utils
# set up an infinite while loop and use the read()
# method to read the frames using the above created object.
cTime =0
pTime=0
while True:
    success, img = cap.read()  # this will give us our frame
    # humara hands wala obj takes rgb
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)  # hands mei ek function jo process kargea isko bas aab info extract karni hai lol
    # print(result.multi_hand_landmarks)
    if result.multi_hand_landmarks:
          for handLms in result.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                # print(id,lm)
                h,w,c = img.shape # as we get in decimals usko pixel convert kiya
                cx,cy = int(lm.x * w), int(lm.y * h) #  yahan pei we got the codinates in pixels
                print(id,cx,cy)
                if id == 4: #  specific pei circle ya mark karnei kei liye
                    cv2.circle(img,(cx,cy),15,(230,0,230),cv2.FILLED)
            # img hai jispei draw kiya
            # and handlms is list of landmarks dono hands kei
                mpDraw.draw_landmarks(img, handLms,mpHands.HAND_CONNECTIONS)  # draw on original img

    # doing this to show fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)

    cv2.imshow("image", img)  # to show the frames in the video.
    # cv2.imshow("img",imgRGB)
    cv2.waitKey(1)  # waitKey is to display the given window for certain mili sec
