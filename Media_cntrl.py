import cv2
import mediapipe as mp
import pyautogui


mphands=mp.solutions.hands
draw=mp.solutions.drawing_utils
hands=mphands.Hands()


cap=cv2.VideoCapture(0)
while True:
    suc,image=cap.read()
    image=cv2.flip(image,1)
    imgrgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    res=hands.process(imgrgb)
    # print(res)
    
    lmlist=[]
    tipids=[4,8,12,16,20]

    if res.multi_hand_landmarks:
        for handlms in res.multi_hand_landmarks:
            draw.draw_landmarks(image,handlms,mphands.HAND_CONNECTIONS)
            for id,lm in enumerate(handlms.landmark):
              cx=lm.x
              cy=lm.y
              lmlist.append([id,cx,cy])

    fingerlist=[]
    if len(lmlist)!=0 and len(lmlist)==21:
      if lmlist[12][1]<lmlist[20][1]:
         if lmlist[tipids[0]][1]>lmlist[tipids[0]-1][1]:
            fingerlist.append(0)
         else:
            fingerlist.append(1)
      else:
         if lmlist[tipids[0]][1]<lmlist[tipids[0]-1][1]:
            fingerlist.append(0)
         else:
            fingerlist.append(1)
      for id in range(1,5):
        if lmlist[tipids[id]][2]>lmlist[tipids[id]-2][2]:
            fingerlist.append(0)
        else:
            fingerlist.append(1)
    # print(fingerlist)
      if len(fingerlist)!=0:
        fingercount=fingerlist.count(1)
        print(fingercount)
        if (fingercount==1):
               pyautogui.press('right')
               cv2.putText(image, "Forward", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
        elif (fingercount==2):
                pyautogui.press('left')
                cv2.putText(image, "Backward", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
        elif (fingercount==3):
                pyautogui.press('up')
                cv2.putText(image, "Volume up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
        elif (fingercount==4):
                pyautogui.press('down')
                cv2.putText(image, "Volume down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
        elif (fingercount==5):
                pyautogui.press('space')
                cv2.putText(image, "Play/Pause", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)

    cv2.imshow('hand_gesture_counting',image)
    if cv2.waitKey(1) & 0XFF==ord('q'):
       break
cap.release()
cv2.destroyAllWindows()                         