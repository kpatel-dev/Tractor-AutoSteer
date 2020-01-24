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

threshold.currentThresh

def main_screen():
    # Capture video frames

    #left and right frames


    width, height=500,400
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)



    root= Tk()

    root.title("Home")
    root.geometry('700x500')

    vidFrame = Frame(root)
    vidFrame.pack(side=LEFT)
    title= Label(vidFrame, text="Home",justify=LEFT)

    title.grid(row=0, column=0, pady=10, padx=10)



    lmain=tk.Label(vidFrame, relief=SUNKEN)
    lmain.grid(row=1, column=0, pady=0, padx=(10,0), rowspan=2, sticky=S)
    #cap=cv2.VidepCapture(0)
    #buttonsFrame = Frame (root)
    #buttonsFrame.pack(side=RIGHT)



    #images
    settimg=ImageTk.PhotoImage(Image.open("icons/set.png"))
    powerimg=ImageTk.PhotoImage(Image.open("icons/powerw.png"))

    show = True

    #define a function that shuts down the program
    def exitProgram(event):
        print("Exiting")
        exit(1)

    def change_basic(event):
        from Basic_Settings import basic_settings
        global show
        show = False
        print("change")
        vidFrame.master.destroy()
        cv2.destroyAllWindows()
        basic_settings()

    #buttons
    settings =Button(vidFrame, width=64, height=64, image=settimg,bg= "gray")
    power =Button(vidFrame, width=64, height=64, image=powerimg,bg="gray")
    power.bind("<Button 1>", exitProgram) #connect button to shutdown
    settings.bind("<Button 1>", change_basic)


    power.grid(row=1, column=1, padx=(10,45),pady=(30,50))
    settings.grid(row=1, column=1,padx=(10,45),pady=(150,0))



    def show_frame():
        if (show == True):
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (590, 440))
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
            #histogram = np.sum(mask[math.floor(mask.shape[0] / 2):, :], axis=0)
            histogram = np.sum(mask[(mask.shape[0] / 2):, :], axis=0)
            val = np.amax(histogram)
            i = histogram.tolist().index(val)

            #*********continue with showing

            #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            # draw a line at the column with the most white pixels


            cv2image = cv2.cvtColor(frame_orig, cv2.COLOR_BGR2RGBA)
            cv2.line(cv2image, (i, 150), (i, 400), (255, 0, 0), 3)
            cv2.line(cv2image, (295, 150), (295, 400), (0, 0, 255), 2)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_RGBA2RGB)
            #in the future, loop to another function to adjust image from here
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

    show_frame()
    root.mainloop()


