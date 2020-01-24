from tkinter import *
from tkinter import ttk
import cv2
from tkinter import PhotoImage
import tkinter as tk
import tkinter
from PIL import Image, ImageTk

import numpy as np
import math
import threshold

frame_counter = 0


# Capture video frames

# left and right frames

# Variables to keep track of slider position


class SliderSet:
    def __init__(self, name, hHigh, hLow, sHigh, sLow, vHigh, vLow):
        self.name = name
        self.s1 = hLow
        self.s2 = hHigh
        self.s3 = sLow
        self.s4 = sHigh
        self.s5 = vLow
        self.s6 = vHigh

    def print_sets(self):
        print(self.s1, self.s2, self.s3, self.s4, self.s5, self.s6)


def sliders_settings():
    cap = cv2.VideoCapture(0)
    root = Tk()

    # title
    root.title("Advanced Settings")
    root.geometry('1000x700')

    # video frame
    vidFrame = Frame(root)
    vidFrame.pack(side=LEFT, pady=10)
    title = Label(vidFrame, text="Advanced Settings", justify=LEFT)
    title.grid(row=0, column=0, pady=(0, 10), padx=10, sticky=W)
    lmain = tk.Label(vidFrame, relief=SUNKEN)
    lmain.grid(row=3, column=0, pady=(0, 0), padx=(10, 0), sticky=S + E + W)
    show = True
    # slider frame
    slideFrame = Frame(root)
    slideFrame.pack(side=RIGHT, pady=10)

    # entry
    file_name = StringVar()
    name = StringVar()
    name_label = Label(vidFrame, text="Name")
    name_entry = Entry(vidFrame, textvariable=file_name)
    name_label.grid(row=1, column=0, sticky=W, padx=(10, 0), pady=(20, 0))
    name_entry.grid(row=2, column=0, sticky=W + E, padx=(10, 200), pady=(0, 0), columnspan=2)

    # images
    saveimg = ImageTk.PhotoImage(Image.open("icons/save2.png"))
    homeimg = ImageTk.PhotoImage(Image.open("icons/home.png"))
    backimg = ImageTk.PhotoImage(Image.open("icons/back_n.png"))

    # button functions

    # save button function
    def save_as(self):
        from advanced_settings import settings
        name = file_name.get()
        item = SliderSet(name, slide2.get(), slide1.get(), slide4.get(), slide3.get(), slide6.get(), slide5.get())
        settings.append(item)
        return

    def go_home(event):
        global show
        show = False
        print("change")
        vidFrame.master.destroy()
        cap.release()
        cv2.destroyAllWindows()
        from home import main_screen
        main_screen()

    def change_advanced(event):
        from advanced_settings import advanced_settings
        global show
        show = False
        print("change")
        vidFrame.master.destroy()
        cap.release()
        cv2.destroyAllWindows()
        advanced_settings()

    # buttons

    save = Button(vidFrame, width=32, height=32, image=saveimg, bg="gray")
    save.grid(row=2, column=0, padx=(225, 0), pady=(0, 20), sticky=W)
    save.bind("<Button 1>", save_as)

    home = Button(slideFrame, width=45, height=45, image=homeimg, bg="gray")
    home.grid(row=6, column=0, padx=(0, 150), pady=(10, 0), sticky=E)
    home.bind("<Button 1>", go_home)

    back = Button(slideFrame, width=45, height=45, image=backimg, bg="gray")
    back.grid(row=6, column=0, padx=(150, 70), pady=(10, 0), sticky=E)
    back.bind("<Button 1>", change_advanced)

    # sliders
    slide1 = Scale(slideFrame, from_=0, to=255, orient=HORIZONTAL, label="Hue Min", length=200)
    slide1.grid(row=0, column=0, sticky=N + E, padx=(0, 30), pady=0)

    slide2 = Scale(slideFrame, from_=0, to=255, orient=HORIZONTAL, label="Hue Max", length=200)
    slide2.set(255)
    slide2.grid(row=1, column=0, sticky=N + E, padx=(0, 30), pady=0)

    slide3 = Scale(slideFrame, from_=0, to=255, orient=HORIZONTAL, label="Saturation Min", length=200)
    slide3.grid(row=2, column=0, sticky=N + E, padx=(0, 30), pady=0)

    slide4 = Scale(slideFrame, from_=0, to=255, orient=HORIZONTAL, label="Saturation Max", length=200)
    slide4.set(255)
    slide4.grid(row=3, column=0, sticky=N + E, padx=(0, 30), pady=0)

    slide5 = Scale(slideFrame, from_=0, to=255, orient=HORIZONTAL, label="Value Min", length=200)
    slide5.grid(row=4, column=0, sticky=N + E, padx=(0, 30), pady=0)

    slide6 = Scale(slideFrame, from_=0, to=255, orient=HORIZONTAL, label="Value Max", length=200)
    slide6.set(255)
    slide6.grid(row=5, column=0, sticky=N + E, padx=(0, 30), pady=0)

    def show_frame():
        if (show == True):
            _, frame = cap.read()
            # frame = cv2.flip(frame, 1)
            frame_orig = cv2.resize(frame, (400, 300))
            # *************detect line
            # threshold the image according to the values

            # get trackbar positions

            ilowH = slide1.get()
            ihighH = slide2.get()
            ilowS = slide3.get()
            ihighS = slide4.get()
            ilowV = slide5.get()
            ihighV = slide6.get()

            hsv = cv2.cvtColor(frame_orig, cv2.COLOR_BGR2HSV)
            lower_hsv = np.array([ilowH, ilowS, ilowV])
            higher_hsv = np.array([ihighH, ihighS, ihighV])
            mask = cv2.inRange(hsv, lower_hsv, higher_hsv)

            frame = cv2.bitwise_and(frame_orig, frame_orig, mask=mask)

            # *********continue with showing
            cv2image = frame

            # in the future, loop to another function to adjust image from here
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)



    show_frame()
    root.mainloop()

