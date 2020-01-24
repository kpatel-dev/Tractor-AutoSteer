from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
from Adv_Settings import sliders_settings

import threading
import datetime
#import imutils
import os

#from imutils.video import VideoStream
import argparse
import time
import numpy as np
import math
import threshold


settings =  []

# saved slider function, stores settings

def advanced_settings():
    basicRoot=Tk()
    leftFrame = Frame(basicRoot, height = 500, width=400)
    leftFrame.pack(side=LEFT)
    rightFrame = Frame(basicRoot, height=500, width=200)
    rightFrame.pack(side=RIGHT, padx=50)







    show = True
#button functions
    #define a function that takes you to make new
    def make_new_file(event):
        from Adv_Settings import sliders_settings
        global show
        show=False
        print("new file")
        leftFrame.master.destroy()
        cv2.destroyAllWindows()
        sliders_settings()

    def change_basic(event):
        from Basic_Settings import basic_settings
        global show
        show = False
        print("change")
        leftFrame.master.destroy()
        cv2.destroyAllWindows()
        basic_settings()

    def go_home(event):
        from home import main_screen
        global show
        show = False
        print("change")
        cap.release()
        leftFrame.master.destroy()
        cv2.destroyAllWindows()
        from home import main_screen
        main_screen()

    titleLabel=Label(leftFrame, text="ADVANCED SETTINGS")
    titleLabel.pack(side=TOP)

    scrollFrame = Frame(rightFrame)
    scrollFrame.pack(pady=30, padx=10)
    #create the scroll bar for selection
    scrollbar = Scrollbar(scrollFrame)
    scrollbar.pack(side=RIGHT, fill=Y)

    def update_sliders(self):
       index=mylist.curselection()
       setting= settings[index[0]]
       threshold.currentThresh.setAll(setting.s2, setting.s1, setting.s4, setting.s3, setting.s6, setting.s5)


       #update sliders



    #settings=["Day","Evening","Short","Tall","other","other1","other3","other4","other5","other5","other6","other7", "other8"]
    mylist = Listbox(scrollFrame, yscrollcommand=scrollbar.set, selectmode=EXTENDED)
    mylist.bind("<Double-Button-1>",update_sliders)
    for line in settings:
        mylist.insert(END, line.name)

    mylist.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=mylist.yview)



    #the top will show the video
    imageFrame = Frame(leftFrame)
    imageFrame.pack(side=BOTTOM, padx=10, pady=10)

    def show_frame():

        if (show == True ):
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (590, 440))
            frame_orig=frame
            # *************detect line
            # threshold the image according to the values

          #  frame_mod = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # standard values that usually work:
            # lower_hsv = np.array([6, 88, 100])
            # higher_hsv= np.array([24, 207, 255])

            lower_hsv = np.array([threshold.currentThresh.getHMin(), threshold.currentThresh.getSMin(),
                                  threshold.currentThresh.getVMin()])
            higher_hsv = np.array([threshold.currentThresh.getHMax(), threshold.currentThresh.getSMax(),
                                   threshold.currentThresh.getVMax()])
            mask = cv2.inRange(hsv, lower_hsv, higher_hsv)

            # find the vertical histogram and draw a line
         #   histogram = np.sum(mask[math.floor(mask.shape[0] / 2):, :], axis=0)
            histogram = np.sum(mask[(mask.shape[0] / 2):, :], axis=0)
            val = np.amax(histogram)
            i = histogram.tolist().index(val)

            # draw a line at the column with the most white pixels
            # draw a line at the column with the most white pixels
        #    cv2.line(frame_orig, (i, 150), (i, 400), (255, 0, 0), 3)
        #    cv2.line(frame_orig, (295, 150), (295, 400), (0, 0, 255), 2)

            #frame = cv2.bitwise_and(frame_orig, frame_orig, mask=mask)

            # *********continue with showing
            cv2image = cv2.cvtColor(frame_orig, cv2.COLOR_BGR2RGBA)
            cv2.line(cv2image, (i, 150), (i, 400), (255, 0, 0), 3)
            cv2.line(cv2image, (295, 150), (295, 400), (0, 0, 255), 2)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_RGBA2RGB)
            # in the future, loop to another function to adjust image from here
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

            # *********continue with showing
            #frame = cv2.bitwise_and(frame, frame, mask=mask)
         #   cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            #cv2image = frame
            # in the future, loop to another function to adjust image from here
         #   img = Image.fromarray(cv2image)
         #   imgtk = ImageTk.PhotoImage(image=img)
         #   lmain.imgtk = imgtk
         #   lmain.configure(image=imgtk)
         #   lmain.after(10, show_frame)

    # Capture video frames
    lmain = Label(imageFrame)
    lmain.pack()
    cap = cv2.VideoCapture(0)

    mkbtn= Button(rightFrame, text="MAKE NEW")
    buttonsFrame = Frame(rightFrame)
    mkbtn.bind("<Button 1>", make_new_file)

    img = "icons/house_2.png"
    img2 = Image.open(img)
    img3 = ImageTk.PhotoImage(image=img2)
    home = Button(buttonsFrame, image=img3)
    home.bind("<Button 1>", go_home)

    imgbk = "icons/back.png"
    imgbk2 = Image.open(imgbk)
    imgbk3 = ImageTk.PhotoImage(image=imgbk2)
    back = Button(buttonsFrame, image=imgbk3)
    back.bind("<Button 1>", change_basic)


    mkbtn.pack(pady=10)
    buttonsFrame.pack()
    home.pack(side=LEFT, pady=10, padx=10)
    back.pack(pady=10, padx=10)

    show_frame()
    basicRoot.mainloop()
