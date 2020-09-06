from camera import VideoCamera
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
t0_warning = 0
warning_wait_time = 3
t0_detect = 0
detect_wait_time = 1
first = False

def start_timer():
    global t0_detect
    t0_detect = time.time()

while True:
    ret, img = stream.read()
    cv_output_data, pose_candidates, phone_detected = myop.estimate(img)
    cv2.imshow("ATM", cv_output_data)

    if phone_detected:
        if not first:
            first = True
            t0_detect = time.time()
        elif time.time() - t0_detect > detect_wait_time:
            first = False
            # if time.time() - t0_warning > warning_wait_time:
            messagebox.showwarning("Warning", "Mind the phone scammers!")
            t0_warning = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
