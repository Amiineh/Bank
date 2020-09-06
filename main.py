from op import OP
import cv2
import tkinter
import time
from tkinter import messagebox

# This code is to hide the main tkinter window
root = tkinter.Tk()
root.withdraw()

myop = OP()
stream = cv2.VideoCapture(0)
t0_detect = 0
detect_wait_time = 2
first = False

# warning text:
font = cv2.FONT_HERSHEY_SIMPLEX
org = (100, 200)
fontScale = 1
color = (0, 0, 255)
thickness = 2

while True:
    ret, img = stream.read()
    cv_output_data, phone_detected, num_people = myop.estimate(img)


    if phone_detected:
        if not first:
            first = True
            t0_detect = time.time()
        elif time.time() - t0_detect > detect_wait_time:
            first = False
            cv2.putText(img, "Mind the phone scammers!", org, font,
                   fontScale, color, thickness, cv2.LINE_AA)
            # messagebox.showwarning("Warning", "Mind the phone scammers!")
            t0_warning = time.time()
            cv2.imshow("ATM", img)
            cv2.waitKey(0)
    # else:
    cv2.putText(img, "People: " + str(num_people), (20, 20), cv2.FONT_HERSHEY_PLAIN,
                fontScale, (0, 255, 0), thickness, cv2.LINE_AA)
    if num_people >= 2:
        cv2.putText(img, "Someone behind you!", org, font,
                    fontScale, (255, 0, 255), thickness, cv2.LINE_AA)
    cv2.imshow("ATM", img)
    # if num_people > 1:
    #     messagebox.showwarning("Warning", "Someone behind you!")
    # cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
