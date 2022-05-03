#imports the pygame library module
import pygame
import pygame.camera
from pygame.locals import (
RLEACCEL
)
import os

from os.path import exists
import threading
import signal
import time
from random import random
from datetime import date


# initilize the pygame module
pygame.init()

# Setting your screen size with a tuple of the screen width and screen height
screen = pygame.display.set_mode((800,480))

# Setting a random caption title for your pygame graphical window.
pygame.display.set_caption("SPEED TRACKER")

# Speed limit signs and their image representations
signs = {
    'unknown': '/home/pi/Documents/FYS-PROJECT/images/signs/unknown.png',
    '5': '/home/pi/Documents/FYS-PROJECT/images/signs/5.png',
    '10': '/home/pi/Documents/FYS-PROJECT/images/signs/10.png',
    '15': '/home/pi/Documents/FYS-PROJECT/images/signs/15.png',
    '20': '/home/pi/Documents/FYS-PROJECT/images/signs/20.png',
    '25': '/home/pi/Documents/FYS-PROJECT/images/signs/25.png',
    '30': '/home/pi/Documents/FYS-PROJECT/images/signs/30.png',
    '35': '/home/pi/Documents/FYS-PROJECT/images/signs/35.png',
    '40': '/home/pi/Documents/FYS-PROJECT/images/signs/40.png',
    '45': '/home/pi/Documents/FYS-PROJECT/images/signs/45.png',
    '50': '/home/pi/Documents/FYS-PROJECT/images/signs/50.png',
    '55': '/home/pi/Documents/FYS-PROJECT/images/signs/55.png',
    '60': '/home/pi/Documents/FYS-PROJECT/images/signs/60.png',
    '65': '/home/pi/Documents/FYS-PROJECT/images/signs/65.png',
    '70': '/home/pi/Documents/FYS-PROJECT/images/signs/70.png',
    '75': '/home/pi/Documents/FYS-PROJECT/images/signs/75.png'
}
os.system("rm /home/pi/Documents/FYS-PROJECT/models-master/research/object_detection/SpeedLimitDetection-master/flagger.txt")

def initGPS():
    os.system("/home/pi/Documents/FYS-PROJECT/./gpsd-example")

def initDetection():
    os.system("python3 /home/pi/Documents/FYS-PROJECT/models-master/research/object_detection/SpeedLimitDetection-master/speed_limit_search.py")
    
#so the save function knows in which order to stitch videos in
firstFlag = True
exitFlag = False
#record two 1 minute videos back to back for stitching
def handleRecord():
    while True:
        
        firstFlag = True
        os.system("/home/pi/Documents/FYS-PROJECT/./libcamera-vid -n -t 6000 -o /media/pi/videos/unsaved/primary.h264 -s")
        if exitFlag:
            break
        
        firstFlag = False
        os.system("/home/pi/Documents/FYS-PROJECT/./libcamera-vid -n -t 6000 -o /media/pi/videos/unsaved/secondary.h264 -s")
        if exitFlag:
            break
        
content = ''
toggled = False
def toggleVideo():
    #obtain process ID from file genreated from libcamera
    global toggled
    with open("/home/pi/Documents/FYS-PROJECT/test.txt") as f:
        content = f.read()
        #send a signal to the recording program to pause or resume recording
        os.kill(int(content), signal.SIGUSR1)
    if(not toggled):
        if(not exists("/home/pi/Documents/FYS-PROJECT/models-master/research/object_detection/SpeedLimitDetection-master/flagger.txt")):
            outputFile = open("/home/pi/Documents/FYS-PROJECT/models-master/research/object_detection/SpeedLimitDetection-master/flagger.txt", "x")
            outputFile.write("f");
            outputFile.close()
            toggled = True
    else:
        os.system("rm /home/pi/Documents/FYS-PROJECT/models-master/research/object_detection/SpeedLimitDetection-master/flagger.txt")
        toggled = False
    
    #os.system("rm /media/pi/videos/unsaved/primary.h264")
    #os.system("rm /media/pi/videos/unsaved/secondary.h264")
    
def saveVideo():
    #to help generate random file name so no video file gets overwritten
    fileName = str(random())
    #check if we need to merge the second video
    if exists("/media/pi/videos/unsaved/secondary.h264"):
        if firstFlag:
            finalActionMergePrim = "mkvmerge -o {}.mkv /media/pi/videos/unsaved/primary.h264 +/media/pi/videos/unsaved/secondary.h264"
            os.system(finalActionMergePrim.format(fileName))
           
        else:
            finalActionMergeSec = "mkvmerge -o {}.mkv /media/pi/videos/unsaved/secondary.h264 +/media/pi/videos/unsaved/primary.h264"
            os.system(finalActionMergeSec.format(fileName))
            
        finalActionMove = "mv {}.mkv /media/pi/videos/videos"
        os.system(finalActionMove.format(fileName))
        
    else:
        finalActionMerge = "mkvmerge -o {}.mkv /media/pi/videos/unsaved/primary.h264"
        os.system(finalActionMerge.format(fileName))
        finalActionMove = "mv {}.mkv /media/pi/videos/videos"
        os.system(finalActionMove.format(fileName))
        
#init a thread for handling recording
recordingThread = threading.Thread(target=handleRecord)
recordingThread.start()

#init a thread for gps
gpsThread = threading.Thread(target=initGPS)
gpsThread.start()

#init a thread for detection
detectionThread = threading.Thread(target=initDetection)
detectionThread.start()

def Shutdown():
    with open("/home/pi/Documents/FYS-PROJECT/test.txt") as f:
        content = f.read()
        #flag the recording thread to exit
        global exitFlag
        exitFlag = True
        print(int(content))
        os.kill(int(content), signal.SIGUSR2)
    
    
    
    os.system("rm /media/pi/videos/unsaved/primary.h264")
    os.system("rm /media/pi/videos/unsaved/secondary.h264")
    
    
    
    with open("/home/pi/Documents/FYS-PROJECT/gpstest.txt") as file:
        GPScontent = file.read()
    #send a signal to the gps program to halt execution
    os.kill(int(GPScontent), signal.SIGUSR1)
    
    os.system('echo "1" > /sys/class/backlight/rpi_backlight/bl_power')
    if(not exists("/home/pi/Documents/FYS-PROJECT/models-master/research/object_detection/SpeedLimitDetection-master/flagger.txt")):
        outputFile = open("/home/pi/Documents/FYS-PROJECT/models-master/research/object_detection/SpeedLimitDetection-master/flagger.txt", "x")
        outputFile.write("f");
        outputFile.close()


def StartupOnTouch():
    global exitFlag
    exitFlag = False
    print("ON")
    
    os.system("rm /home/pi/Documents/FYS-PROJECT/models-master/research/object_detection/SpeedLimitDetection-master/flagger.txt")
    #restart recording thread after pid kill
    #init a thread for handling recording
    recordingThreadSecondary = threading.Thread(target=handleRecord)
    recordingThreadSecondary.start()
    
    with open("/home/pi/Documents/FYS-PROJECT/gpstest.txt") as file:
        GPScontent = file.read()
    #send a signal to the gps program to unpause execution
    os.kill(int(GPScontent), signal.SIGUSR1)
    
    #enable backlight again
    os.system('echo "0" > /sys/class/backlight/rpi_backlight/bl_power')
    

class Button(pygame.sprite.Sprite):
    def __init__(self, buttonType, unpressedSrc, pressedSrc,x,y):
        super(Button,self).__init__()
        self.unpressedSrc = unpressedSrc
        self.pressedSrc = pressedSrc
        self.x = x
        self.y = y
        self.buttonType = buttonType

        self.surf = pygame.image.load(self.unpressedSrc).convert()
        self.rect = self.surf.get_rect().move(self.x,self.y)

        self.isDrawn = True
    
    def pressDown(self):
        # Change image to pressedSrc
        self.surf = pygame.image.load(self.pressedSrc).convert()
        self.rect = self.surf.get_rect().move(self.x,self.y)

        # Call type specific function
        if(self.buttonType == 'recordButton' and not exitFlag):
            saveVideo()
        elif(self.buttonType == 'viewButton' and not exitFlag):
            self.toggleScreens(speedList)
        elif(self.buttonType == 'shutdownButton'):
            if (not exitFlag and self.isDrawn):
                self.isDrawn = False
                Shutdown()
        elif(self.buttonType == 'toggleButton' and shutdownButton.isDrawn):
            #we do this to toggle the button instead of press it.
            tempMemory = self.unpressedSrc
            self.unpressedSrc = self.pressedSrc
            self.pressedSrc = tempMemory
            toggleVideo()
            print("TOGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
            
    
    def pressUp(self):
        # Change image to unpressedSrc
        self.surf = pygame.image.load(self.unpressedSrc).convert()
        self.rect = self.surf.get_rect().move(self.x,self.y)

    def toggleScreens(self,speedObjects): # <--- This is where the camera and speed screens can be switched
        # Set the drawing of the speed objects to False/True
        # Show/Hide camera
        print("Screen Toggle")
        pass


class Entity(pygame.sprite.Sprite):
    def __init__(self,src,x,y,greenOut=False):
        super(Entity,self).__init__()
        self.surf = pygame.image.load(src).convert()

        self.x = x
        self.y = y

        if(greenOut):
            self.surf.set_colorkey((0,255,0), RLEACCEL)

        self.rect = self.surf.get_rect().move(self.x,self.y)

        self.isDrawn = True
    
    def changeSign(self,sign):
        self.surf = pygame.image.load(signs[sign]).convert()

class Text():
    def __init__(self,x,y,text,font,size,textColor,aa=True):
        self.x = x
        self.y = y
        self.stringText = text
        self.font = font
        self.size = size
        self.textColor = textColor
        self.aa = aa

        self.fontObject = pygame.font.Font(self.font,self.size)
        self.text = self.fontObject.render(self.stringText,self.aa,self.textColor)

        self.rect = self.text.get_rect()
        self.rect.center = (self.x,self.y)

        self.isDrawn = True

    def changeText(self,text):
        self.stringText = text
        self.fontObject = pygame.font.Font(self.font,self.size)
        self.text = self.fontObject.render(self.stringText,self.aa,self.textColor)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x,self.y)


# List of Objects
buttonList = pygame.sprite.Group()
spriteList = pygame.sprite.Group()
speedList = []
textList = []

#Objects
recordButton = Button("recordButton",'/home/pi/Documents/FYS-PROJECT/images/recordUnpressed.png','/home/pi/Documents/FYS-PROJECT/images/recordPressed.png',50,75)
viewButton = Button("viewButton",'/home/pi/Documents/FYS-PROJECT/images/viewUnpressed.png','/home/pi/Documents/FYS-PROJECT/images/viewPressed.png',50,150)
toggleButton = Button("toggleButton", '/home/pi/Documents/FYS-PROJECT/images/pauseUnpressed.png','/home/pi/Documents/FYS-PROJECT/images/resumeUnpressed.png',50,225)
shutdownButton = Button("shutdownButton", '/home/pi/Documents/FYS-PROJECT/images/shutdownUnpressed.png','/home/pi/Documents/FYS-PROJECT/images/shutdownPressed.png',50,300)

spriteList.add(recordButton)
spriteList.add(viewButton)
spriteList.add(toggleButton)
spriteList.add(shutdownButton)


buttonList.add(recordButton)
buttonList.add(viewButton)
buttonList.add(toggleButton)
buttonList.add(shutdownButton)


speedBackground = Entity('/home/pi/Documents/FYS-PROJECT/images/speedBackground.png',320,70)
spriteList.add(speedBackground)

speedSign = Entity(signs['unknown'],530,110,True)
spriteList.add(speedSign)
speedList.append(speedSign)

yourSpeedText1 = Text(425,160,'Your','freesansbold.ttf',44,(255,255,255))
yourSpeedText2 = Text(425,210,'Speed','freesansbold.ttf',44,(255,255,255))
currentSpeedText = Text(425,300,'--','freesansbold.ttf',68,(255,255,255))
textList.append(yourSpeedText1)
textList.append(yourSpeedText2)
textList.append(currentSpeedText)
speedList.append(yourSpeedText1)
speedList.append(yourSpeedText2)
speedList.append(currentSpeedText)
def draw():
    # Draw all objects in spriteList
    for i in spriteList:
        if(i.isDrawn):
            screen.blit(i.surf, (i.rect.x,i.rect.y))

    # Draw text fields
    for i in textList:
        if(i.isDrawn):
            screen.blit(i.text,i.rect)


# Logic Loop
running = True
while running:
    if(exitFlag == False):
        shutdownButton.isDrawn = True
    if firstFlag:
        f = open("/home/pi/Documents/FYS-PROJECT/Y.txt", "w")
        f.write("TESTDATA")
        f.close()
    else:
        os.system("rm /home/pi/Documents/FYS-PROJECT/Y.txt")
        # Event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("mouse down")
            if(exitFlag == True):
                StartupOnTouch();
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for b in buttonList:
                    if b.rect.collidepoint(pygame.mouse.get_pos()):
                        b.pressDown()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for b in buttonList:
                    b.pressUp()

    # Fill the background
    screen.fill((31, 0, 76))

    # Draw all elements
    draw()

    # Flip the display
    pygame.display.flip()
    
    if exists("/home/pi/Documents/FYS-PROJECT/flag.txt"):
        gpsFile = open("/home/pi/Documents/FYS-PROJECT/flag.txt", "r")
        if os.path.getsize("/home/pi/Documents/FYS-PROJECT/flag.txt") < 3:
            currentSpeedText.changeText(gpsFile.readline(1))
            print(gpsFile.readline(1))
        else:
            currentSpeedText.changeText(gpsFile.readline(2))
            print(gpsFile.readline(2))
        gpsFile.close()
        os.remove("/home/pi/Documents/FYS-PROJECT/flag.txt")
        
    if exists("/home/pi/Documents/FYS-PROJECT/speed.txt"):
        speedFile = open("/home/pi/Documents/FYS-PROJECT/speed.txt", "r")
        if os.path.getsize("/home/pi/Documents/FYS-PROJECT/speed.txt") < 2:
            #print(speedFile.readline(1))
            speedSign.changeSign(speedFile.readline(1))
            
        else:
            #print(speedFile.readline(2))
            speedSign.changeSign(speedFile.readline(2))
            
        speedFile.close()
        #os.remove("/home/pi/Documents/FYS-PROJECT/speed.txt")

# Done! Time to quit.
pygame.quit()

# End the program
quit()
