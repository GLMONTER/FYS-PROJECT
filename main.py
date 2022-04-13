from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle

import os
from os.path import exists
import threading
import signal
import time
from random import random
from datetime import date


#so the save function knows in which order to stitch videos in
firstFlag = True

#record two 10 minute videos back to back for stitching
def handleRecord():
    while True:
        
        firstFlag = True
        os.system("./libcamera-vid  -t 600000 -o /media/pi/videos/unsaved/primary.h264 -s")
        if exitFlag:
            break
        
        firstFlag = False
        os.system("./libcamera-vid -t 600000 -o /media/pi/videos/unsaved/secondary.h264 -s")
        if exitFlag:
            break
        
content = ''   
def stopVideo():
    #obtain process ID from file genreated from libcamera
    
    with open("test.txt") as f:
        content = f.read()
        #send a signal to the recording program to pause recording
    os.kill(int(content), signal.SIGUSR1)
  #  os.system("rm /media/pi/videos/unsaved/primary.h264")
   # os.system("rm /media/pi/videos/unsaved/secondary.h264")
    
def saveVideo():
    #to help generate random file name so no video file gets overwritten
    fileName = str(random())
    #check if we need to merge the second video
    if exists("secondary.h264"):
        if firstFlag:
            finalActionMergePrim = "mkvmerge -o {}.mkv /media/pi/videos/unsaved/primary.h264 +/media/pi/videos/unsaved/secondary.h264"
            os.system(finalActionMergePrim.format(fileName))
           
        else:
            finalActionMergeSec = "mkvmerge -o {}.mkv /media/pi/videos/unsaved/secondary.h264 +/media/pi/videos/unsaved/primary.h264"
            os.system(finalActionMergeSec.format(fileName))           
    #merge video(s) and move final export to external media
    else:
        
        finalActionMerge = "mkvmerge -o {}.mkv /media/pi/videos/unsaved/primary.h264"
        os.system(finalActionMerge.format(fileName))
        print(fileName)
        finalActionMove = "mv {}.mkv /media/pi/videos/videos"
        os.system(finalActionMove.format(fileName))

#init a thread for handling recording
thread1 = threading.Thread(target=handleRecord)
thread1.start()

window = Tk()
window.geometry("800x480")
style = ThemedStyle(window)
style.set_theme("equilux")

def Shutdown():
    with open("test.txt") as f:
        content = f.read()
    #flag the recording thread to exit
    global exitFlag
    exitFlag = True
    os.kill(int(content), signal.SIGUSR2)
   # thread1.join()
    os.system("rm /media/pi/videos/unsaved/primary.h264")
    os.system("rm /media/pi/videos/unsaved/secondary.h264")
    window.destroy()

# setting attribute
#window.attributes('-fullscreen', True)
leftFrame = ttk.Frame(window, padding=0)
leftFrame.pack(side=LEFT, expand=True, fill='both')
rightFrame = ttk.Frame(window, padding=0)
rightFrame.pack(side=RIGHT, expand=True, fill='both')

ttk.Button(leftFrame, text="Shutdown", command=Shutdown).grid(column=0, row=4)
ttk.Button(leftFrame, text="Stop Recording", command=stopVideo).grid(column=0, row=3)
ttk.Button(leftFrame, text="Resume Recording", command=stopVideo).grid(column=0, row=2)
ttk.Button(leftFrame, text="Save Recording", command=saveVideo).grid(column=0, row=0)
ttk.Button(leftFrame, text="Preview Camera").grid(column=0, row=1)
currentSpeed = Label(rightFrame, height=1, width=3, bg="black", fg="gray", text="55", font=("Arial, 150"))
currentSpeed.grid(column=3, row=0)
readSpeed = Label(rightFrame, height=1, width=3, bg="black", fg="gray", text="50", font=("Arial, 150"))
readSpeed.grid(column=3, row=1)


window.mainloop()


  

