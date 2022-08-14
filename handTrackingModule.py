import cv2
import time
import mediapipe as mp

# made this to use it as a module
class handDetector():
    def __init__(self, mode = False, maxHands=2, modelComplexity = 1 , detectionConfi=0.5, trackingConfi = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionConfi = detectionConfi
        self.trackingConfi = trackingConfi

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionConfi, self.trackingConfi)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw = True):
        landmarkList = []
        if(self.results.multi_hand_landmarks):
            reqHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(reqHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarkList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (230, 0, 230), cv2.FILLED)

        return landmarkList





def main():
    cam = cv2.VideoCapture(0)
    currentTime, prevTime = 0, 0

    img = detector = handDetector()

    while True:
        success, img = cam.read()
        detector.findHands(img)
        landmarkList = detector.findPosition(img)
        if(len(landmarkList)!= 0 ):
            print(landmarkList[2])

        currentTime = time.time()
        fps = 1 / (currentTime - prevTime)
        prevTime = currentTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

        cv2.imshow("image", img)
        cv2.waitKey(1)

if __name__ =="__main__":
    main()
