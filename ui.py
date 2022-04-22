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


#so the save function knows in which order to stitch videos in
firstFlag = True
exitFlag = False
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

def toggleVideo():
    #obtain process ID from file genreated from libcamera
   
    with open("test.txt") as f:
        content = f.read()
    #send a signal to the recording program to pause or resume recording
    os.kill(int(content), signal.SIGUSR1)
    #os.system("rm /media/pi/videos/unsaved/primary.h264")
    #os.system("rm /media/pi/videos/unsaved/secondary.h264")
    
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
            
        finalActionMove = "mv {}.mkv /media/pi/videos/videos"
        os.system(finalActionMove.format(fileName))
        
    else:
        
        finalActionMerge = "mkvmerge -o {}.mkv /media/pi/videos/unsaved/primary.h264"
        os.system(finalActionMerge.format(fileName))
        finalActionMove = "mv {}.mkv /media/pi/videos/videos"
        os.system(finalActionMove.format(fileName))
        
    #init a thread for handling recording
thread1 = threading.Thread(target=handleRecord)
thread1.start()


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
    os.system('echo "1" > /sys/class/backlight/rpi_backlight/bl_power')




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
        if(self.buttonType == 'recordButton'):
            saveVideo()
        elif(self.buttonType == 'viewButton'):
            self.toggleScreens(speedList)
        elif(self.buttonType == 'toggleButton'):
            #we do this to toggle the button instead of press it.
            tempMemory = self.unpressedSrc
            self.unpressedSrc = self.pressedSrc
            self.pressedSrc = tempMemory
            toggleVideo()
            
    
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
toggleButton = Button("toggleButton", '/home/pi/Documents/FYS-PROJECT/images/toggle.png','/home/pi/Documents/FYS-PROJECT/images/untoggle.png',50,225)

spriteList.add(recordButton)
spriteList.add(viewButton)
spriteList.add(toggleButton)

buttonList.add(recordButton)
buttonList.add(viewButton)
buttonList.add(toggleButton)

speedBackground = Entity('/home/pi/Documents/FYS-PROJECT/images/speedBackground.png',320,70)
spriteList.add(speedBackground)

speedSign = Entity(signs['unknown'],530,110,True)
spriteList.add(speedSign)
speedList.append(speedSign)

yourSpeedText1 = Text(425,160,'Your','freesansbold.ttf',44,(255,255,255))
yourSpeedText2 = Text(425,210,'Speed','freesansbold.ttf',44,(255,255,255))
currentSpeedText = Text(425,300,'00','freesansbold.ttf',68,(255,255,255))
textList.append(yourSpeedText1)
textList.append(yourSpeedText2)
textList.append(currentSpeedText)
speedList.append(yourSpeedText1)
speedList.append(yourSpeedText2)
speedList.append(currentSpeedText)

def getSpeed():
    # Implement function to get the speed from the GPS. Return it in string form.
    speed = 0
    return(str(speed))

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
    # Event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

# Done! Time to quit.
pygame.quit()

# End the program
quit()
