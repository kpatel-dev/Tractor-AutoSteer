from tkinter import *
from tkinter import ttk
import cv2
from tkinter import PhotoImage
import tkinter as tk
import tkinter
from PIL import Image, ImageTk
import time
import numpy as np
import math
import threshold

import serial as serial

threshold.currentThresh

# port = '/dev/ttyACM0' # note I'm using Mac OS-X
port = '/dev/ttyS0'
timeError = 0
totalError = 0
ard = serial.Serial(port, 9600, timeout=5)

frame_counter = 0


def main_screen():
    # Capture video frames

    # left and right frames

    width, height = 500, 400
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    root = Tk()

    root.title("Home")
    root.geometry('1000x500')

    vidFrame = Frame(root)
    buttonFrame = Frame(root)
    vidFrame.pack(side=LEFT, padx=10, pady=10)
    buttonFrame.pack(side=RIGHT, padx=10, pady=10)
    title = Label(vidFrame, text="Home", justify=LEFT)

    title.grid(row=0, column=0, pady=10, padx=10)

    lmain = tk.Label(vidFrame, relief=SUNKEN)
    lmain.grid(row=1, column=0, rowspan=3, sticky=S)
    # cap=cv2.VidepCapture(0)
    # buttonsFrame = Frame (root)
    # buttonsFrame.pack(side=RIGHT)

    # images
    settimg = ImageTk.PhotoImage(Image.open("icons/set.png"))
    powerimg = ImageTk.PhotoImage(Image.open("icons/powerw.png"))
    goimg = ImageTk.PhotoImage(Image.open("icons/go.png"))

    show = True

    # define a function that shuts down the program
    def exitProgram(event):
        shut = "x"
        ard.flush()
        ard.write(shut.encode())
        exit(0)

    def change_basic(event):
        from Basic_Settings import basic_settings
        global show
        show = False
        vidFrame.master.destroy()
        cap.release()
        cv2.destroyAllWindows()
        basic_settings()

    def goButton(event):
        
        start = "s"
        ard.flush()
        ard.write(start.encode())

    # buttons
    settings = Button(buttonFrame, width=64, height=64, image=settimg, bg="gray")
    power = Button(buttonFrame, width=64, height=64, image=powerimg, bg="gray")
    go = Button(buttonFrame, width=64, height=64, image=goimg, bg="gray")
    power.bind("<Button 1>", exitProgram)  # connect button to shutdown
    settings.bind("<Button 1>", change_basic)
    go.bind("<Button 1>", goButton)

    power.grid(row=0, column=1, padx=(45, 45), pady=(10, 20))
    settings.grid(row=1, column=1, padx=(45, 45), pady=(0, 20))
    go.grid(row=2, column=1, padx=(45, 45), pady=(0, 10))

    def show_frame():
        if (show == True):
            _, frame = cap.read()
            global frame_counter
            frame_counter += 1
            # frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (500, 400))
            frame_orig = frame
            # *************detect line
            # threshold the image according to the values

            frame_mod = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hsv = cv2.cvtColor(frame_mod, cv2.COLOR_BGR2HSV)
            # standard values that usually work:
            # lower_hsv = np.array([6, 88, 100])
            # higher_hsv= np.array([24, 207, 255])
            lower_hsv = np.array([threshold.currentThresh.getHMin(), threshold.currentThresh.getSMin(),
                                  threshold.currentThresh.getVMin()])
            higher_hsv = np.array([threshold.currentThresh.getHMax(), threshold.currentThresh.getSMax(),
                                   threshold.currentThresh.getVMax()])
            mask = cv2.inRange(hsv, lower_hsv, higher_hsv)

            # find the vertical histogram and draw a line
            histogram = np.sum(mask[math.floor(mask.shape[0] / 2):, :], axis=0)
            # histogram = np.sum(mask[(mask.shape[0] / 2):, :], axis=0)
            val = np.amax(histogram)
            i = histogram.tolist().index(val)


            thisError = i - 250

            ard.flush()
            errorStr = str(thisError)
            errorStr = 'e' + errorStr + '\n'
            ard.write(errorStr.encode())
             
            # *********continue with showing

            # *********continue with showing

            # cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            # draw a line at the column with the most white pixels

            cv2image = cv2.cvtColor(frame_orig, cv2.COLOR_BGR2RGBA)
            cv2.line(cv2image, (i, 150), (i, 400), (255, 0, 0), 3)
            cv2.line(cv2image, (250, 150), (250, 400), (0, 0, 255), 2)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_RGBA2RGB)
            # in the future, loop to another function to adjust image from here
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

    show_frame()
    root.mainloop()

