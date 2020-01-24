from tkinter import *
from PIL import Image
from PIL import ImageTk
import threading
import datetime
import imutils
import cv2
import math
from imutils.video import VideoStream
import argparse
import time
import numpy as np
import math
import threshold

import serial as serial
from home import ard
#port = 'COM3' # note I'm using Mac OS-X
timeError = 0
totalError = 0
#ard = serial.Serial(port,9600,timeout=5)

frame_counter=0
def basic_settings():

    basicRoot=Tk()
    leftFrame = Frame(basicRoot, height = 500, width=400)
    leftFrame.pack(side=LEFT)
    rightFrame = Frame(basicRoot, height=500, width=200)
    rightFrame.pack(side=RIGHT, padx=60)

    titleLabel=Label(leftFrame, text="BASIC SETTINGS")
    titleLabel.pack(side=TOP)

    topbtns = Frame(rightFrame)
    topbtns.pack()
    rightbtns = Frame(topbtns)
    leftbtns = Frame(topbtns)
    leftbtns.pack(side=LEFT, pady=20)
    rightbtns.pack(pady=20)

    #Basic settings button functions
    def sun_set(self):
        threshold.currentThresh.setAll(24, 6, 207, 88, 255, 100)

    def cloudy_set(self):
        threshold.currentThresh.setAll(50, 80, 30, 50, 255, 100)
    def eve_set(self):
        threshold.currentThresh.setAll(24, 6, 207, 88, 255, 100)
    def rain_set(self):
        threshold.currentThresh.setAll(24, 6, 207, 88, 255, 100)



    imgsun = "icons/sun.png"
    imgsun2 = Image.open(imgsun)
    imgsun3 = ImageTk.PhotoImage(image=imgsun2)
    sunBtn=Button(leftbtns, image=imgsun3)
    sunBtn.bind("<Double-Button-1>", sun_set)

    imgcld = "icons/cloud.png"
    imgcld2 = Image.open(imgcld)
    imgcld3 = ImageTk.PhotoImage(image=imgcld2)
    cloudBtn = Button(rightbtns, image=imgcld3)
    cloudBtn.bind("<Double-Button-1>", cloudy_set)

    sunBtn.pack(side=TOP, pady=10, padx=10)
    cloudBtn.pack(side=TOP, pady=10, padx=0)


    imgevening = "icons/evening.png"
    imgevening2 = Image.open(imgevening)
    imgevening3 = ImageTk.PhotoImage(image=imgevening2)
    eveningBtn = Button(leftbtns, image=imgevening3, pady=10, padx=10)
    eveningBtn.bind("<Double-Button-1>", eve_set)

    imgraining = "icons/rain.png"
    imgraining2 = Image.open(imgraining)
    imgraining3 = ImageTk.PhotoImage(image=imgraining2)
    rainyBtn = Button(rightbtns, image=imgraining3, pady=10, padx=10)
    rainyBtn.bind("<Double-Button-1>", rain_set)
    eveningBtn.pack()
    rainyBtn.pack()

    #the top will show the video
    imageFrame = Frame(leftFrame)
    imageFrame.pack(side=BOTTOM, padx=10, pady=10)



    # Capture video frames
    lmain = Label(imageFrame)
    lmain.pack()
    cap = cv2.VideoCapture(0)

    show = True

    def change_advanced(event):
        from advanced_settings import advanced_settings
        global show
        show = False
        leftFrame.master.destroy()
        cap.release()
        cv2.destroyAllWindows()
        advanced_settings()

    def go_home(event):
        global show
        show = False
        cap.release()
        leftFrame.master.destroy()
        cv2.destroyAllWindows()
        from home import main_screen
        main_screen()

    advancedSettings= Button(rightFrame, text="ADVANCED SETTINGS")
    advancedSettings.bind("<Button 1>", change_advanced)

    buttonsFrame = Frame(rightFrame)

    img = "icons/house_2.png"
    img2 = Image.open(img)
    img3 = ImageTk.PhotoImage(image=img2)
    home = Button(buttonsFrame, image=img3)
    home.bind("<Button 1>", go_home)

    imgbk = "icons/back.png"
    imgbk2 = Image.open(imgbk)
    imgbk3 = ImageTk.PhotoImage(image=imgbk2)
    back = Button(buttonsFrame, image=imgbk3)
    back.bind("<Button 1>", go_home)

    advancedSettings.pack(pady=10)
    buttonsFrame.pack()

    home.pack(side=LEFT, pady=10, padx=10)
    back.pack(pady=10, padx=0)

    def show_frame():
        if (show == True):
            _, frame = cap.read()
            global frame_counter
            frame_counter += 1
            #frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (500, 400))
            frame_orig=frame
            #*************detect line
            # threshold the image according to the values

            frame_mod = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hsv = cv2.cvtColor(frame_mod, cv2.COLOR_BGR2HSV)
            # standard values that usually work:
            # lower_hsv = np.array([6, 88, 100])
            # higher_hsv= np.array([24, 207, 255])
            lower_hsv = np.array([threshold.currentThresh.getHMin(), threshold.currentThresh.getSMin(),threshold.currentThresh.getVMin()])
            higher_hsv = np.array([threshold.currentThresh.getHMax(), threshold.currentThresh.getSMax(), threshold.currentThresh.getVMax()])
            mask = cv2.inRange(hsv, lower_hsv, higher_hsv)

            # find the vertical histogram and draw a line
            histogram = np.sum(mask[math.floor(mask.shape[0] / 2):, :], axis=0)
            #histogram = np.sum(mask[(mask.shape[0] / 2):, :], axis=0)
            val = np.amax(histogram)
            i = histogram.tolist().index(val)


            thisError = i - 250
            ard.flush()
            errorStr = str(thisError)
            errorStr = 'e' + errorStr + '\n'
            ard.write(errorStr.encode())
            # *********continue with showing

            #*********continue with showing

            #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            # draw a line at the column with the most white pixels


            cv2image = cv2.cvtColor(frame_orig, cv2.COLOR_BGR2RGBA)
            cv2.line(cv2image, (i, 150), (i, 400), (255, 0, 0), 3)
            cv2.line(cv2image, (250, 150), (250, 400), (0, 0, 255), 2)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_RGBA2RGB)
            #in the future, loop to another function to adjust image from here
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

    show_frame()
    basicRoot.mainloop()
