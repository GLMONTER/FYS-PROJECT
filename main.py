from tkinter import *
from tkinter import ttk

import os
from os.path import exists
import threading
import signal
import time

#so the save function knows in which order to stitch videos in
firstFlag = True



#record two 10 minute videos back to back for stitching
def handleRecord():
    while True:
        
        firstFlag = True
        os.system("./libcamera-vid -t 600000 -o /media/pi/videos/unsaved/primary.h264 -s")
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
    #check if we need to merge the second video
    if exists("secondary.h264"):
        if firstFlag:
            os.system("mkvmerge -o video.mkv /media/pi/videos/unsaved/primary.h264 +/media/pi/videos/unsaved/secondary.h264")
            os.system("rm /media/pi/videos/unsaved/primary.h264")
            os.system("rm /media/pi/videos/unsaved/secondary.h264")
        else:
            os.system("mkvmerge -o video.mkv /media/pi/videos/unsaved/secondary.h264 +/media/pi/videos/unsaved/secondary.h264")
            os.system("rm /media/pi/videos/unsaved/primary.h264")
            os.system("rm /media/pi/videos/unsaved/secondary.h264")
    #merge video(s) and move final export to external media
    else:
        os.system("mkvmerge -o video.mkv /media/pi/videos/unsaved/primary.h264")
        os.system("mv video.mkv /media/pi/videos/videos")
        os.system("rm /media/pi/videos/unsaved/primary.h264")

#init a thread for handling recording
thread1 = threading.Thread(target=handleRecord)
thread1.start()

window = Tk()

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
window.attributes('-fullscreen', True)
frm = ttk.Frame(window, padding=10)
frm.grid()

ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Shutdown", command=Shutdown).grid(column=1, row=0)
ttk.Button(frm, text="Stop Recording", command=stopVideo).grid(column=2, row=0)
ttk.Button(frm, text="Save Recording", command=saveVideo).grid(column=3, row=0)

window.mainloop()


  

