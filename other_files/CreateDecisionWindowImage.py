#Engineers: Sean Duback, Robert Geoffrion
#School: Weber State University
#Project: Motion Tracking
#Year: 2019 Academic Year

#creates decision window image of original

import numpy as np
import cv2
import math
import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw
############################################################ Global Variables ###############################################
white = [255,255,255]
black = [0,0,0]
nearBlack = [5,5,5]
dWinList = []
letter = cv2.imread('bw_image.png', 1)
pixDistance = 0
pixDistFirst = []
pixDirFirst = {}
pixDistSecond = []
pixDirSecond = {}
pixDistStart = 100
minPixDist = {}
# grab the reference to the webcam
#camera = cv2.VideoCapture(0)
# define the lower and upper boundaries of the "orange"
colorLower = (0, 120, 70)
colorUpper = (50, 255, 180)
winNum = 0

startFlag = False
oldStartFlag = False
endFlag = False
score = 0

############################################################# Class Definitions #################################################

class Dwin(object):
    def __init__(self, idnum=0, ymin=0, ymax=0, xmin=0, xmax=0):
        self.idnum = idnum
        self.ymin = ymin
        self.ymax = ymax
        self.xmin = xmin
        self.xmax = xmax


############################################################# Functions ###########################################

def colorDwin (img, class_type="Dwin"):
    #func used for debugging colors in the dWins black and makes the letter white
    for Dwin in dWinList:
        print ("Window#= %s, xmin=%s, xmax= %s, ymin= %s ymax= %s"% (Dwin.idnum, Dwin.xmin, Dwin.xmax, Dwin.ymin, Dwin.ymax))
        for x in range(Dwin.xmin, Dwin.xmax):
            for y in range(Dwin.ymin, Dwin.ymax, -1):
                if np.array_equal(img[y, x], black):
                    #print ("x=%s y=%s"%(x, y))
                    img[y, x] = white
                else:
                     img[y, x] = 0
        #letter_image = Image.fromarray(letter)
        #letter_image.show()


def init ():
    #rectangles for the image
    #decision windows,   #, Ymin, YMax, XMin, XMax
    #make Distance windows starting at the lower left corner and moving towards the upper right
    dWinList.append(Dwin(0, 421, 404, 366, 374))
    dWinList.append(Dwin(1, 404, 402, 372, 376))
    dWinList.append(Dwin(2, 402, 396, 374, 378))
    dWinList.append(Dwin(3, 396, 394, 376, 383))
    dWinList.append(Dwin(4, 394, 390, 379, 384))
    dWinList.append(Dwin(5, 390, 386, 380, 385))
    dWinList.append(Dwin(6, 386, 365, 382, 400))
    dWinList.append(Dwin(7, 365, 345, 390, 410))
    dWinList.append(Dwin(8, 345, 325, 395, 415))
    dWinList.append(Dwin(9, 325, 305, 400, 420))
    dWinList.append(Dwin(10, 305, 285, 405, 425))
    dWinList.append(Dwin(11, 285, 265, 410, 430))
    dWinList.append(Dwin(12, 265, 245, 420, 440))
    dWinList.append(Dwin(13, 245, 225, 420, 440))
    dWinList.append(Dwin(14, 225, 205, 420, 440))
    dWinList.append(Dwin(15, 205, 185, 420, 440))
    #Dwin 16 begins left movement
    dWinList.append(Dwin(16, 205, 185, 400, 420))
    #Dwin 17 begins down movement
    dWinList.append(Dwin(17, 225, 205, 390, 410))
    dWinList.append(Dwin(18, 245, 225, 385, 405))
    dWinList.append(Dwin(19, 265, 245, 380, 400))
    dWinList.append(Dwin(20, 285, 265, 380, 400))
    dWinList.append(Dwin(21, 305, 285, 375, 395))
    dWinList.append(Dwin(22, 325, 305, 375, 390))
    dWinList.append(Dwin(23, 345, 325, 375, 385))
    dWinList.append(Dwin(24, 365, 345, 375, 385))
    dWinList.append(Dwin(25, 385, 365, 370, 380))
    dWinList.append(Dwin(26, 405, 385, 370, 380))
    dWinList.append(Dwin(27, 425, 405, 370, 380))
    dWinList.append(Dwin(28, 445, 425, 370, 380))
    dWinList.append(Dwin(29, 465, 445, 370, 380))
    dWinList.append(Dwin(30, 490, 465, 370, 380))
    #Dwin 28 begins right movement
    dWinList.append(Dwin(31, 495, 475, 380, 400))
    dWinList.append(Dwin(32, 495, 475, 400, 420))
    #Dwin 30 begins up movement
    dWinList.append(Dwin(33, 475, 455, 410, 430))
    dWinList.append(Dwin(34, 455, 435, 420, 440))
    dWinList.append(Dwin(35, 435, 405, 430, 450))
    dWinList.append(Dwin(36, 0, 0, 0, 0)) #dummy window for dWin +1 loop when dWin loop is on dwin=35

############################################################# Main ########################################################
init()
#width = 800
#pixels2 = [(0,0,0)]*600
#blankImage = Image.new('RGB', (800, 600), color = (255, 255, 255))
#img.save("test1.png")
#ImageArray = cv2.imread("test1.png", 1)

# Using above first method to create a
# 2D array
# Using above second method to create a
# 2D array
#y, x
# rows, cols = (600, 800)
# arr=[]
# for i in range(rows):
#     col = []
#     for j in range(cols):
#         col.append((255,255,255))
#     arr.append(col)
# #arr[3][3] = (0,0,0)
# array = np.array(arr, dtype=np.uint8)
# #print(arr)
# new_image = Image.fromarray(array)
# new_image.save('DWTest1.png')


colorDwin(letter, dWinList) #used to color in the dWin black for debugging
letter_image = Image.fromarray(letter)
letter_image.save('VisibleDecisionWindows.png')
# broker = "192.168.43.175"
# client = mqtt.Client("computer2")
# client.connect(broker)
# while True:
#     cv2.imshow("Learn to Write!", letter)
#     key = cv2.waitKey(1) & 0xFF
#
#     # grab the current frame
#     (grabbed, frame) = camera.read()
#     frame = cv2.flip(frame, 1)
#
#     # resize the frame, blur it, and convert it to the HSV color space
#     blurred = cv2.GaussianBlur(frame, (11, 11), 0)
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#
#     # construct a mask for the color then perform a series of dilations and erosions to remove any small blobs left in the mask
#     mask = cv2.inRange(hsv, colorLower, colorUpper)
#     mask = cv2.erode(mask, None, iterations=2)
#     mask = cv2.dilate(mask, None, iterations=2)
#
#     # find contours in the mask and initialize the current (x, y) center of the ball
#     cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
#     #center = None #why is center none?
#
#     # only proceed if at least one contour was found
#     if len(cnts) > 0:
#         # find the largest contour in the mask, then use centroid
#         c = max(cnts, key=cv2.contourArea)
#         ((x, y), radius) = cv2.minEnclosingCircle(c)
#         M = cv2.moments(c)
#         centerX = (int(M["m10"] / M["m00"])+50)
#         centerY = (int(M["m01"] / M["m00"])+50)
#         #print("X is %s, Y is %s"%(int(centerX),int(centerY))) #used for debugging
#         #if centerX < 800 and centerY < 600:
#         if startFlag == False: #Wait until input is near Dwin 0 to start game
#             cv2.circle(letter, (centerX, centerY), 1, (0, 0, 255), -1)
#             startFlag = start(letter, centerX,centerY)
#         else:
#             if oldStartFlag == False: #Clean the img on game start
#                 oldStartFlag = True
#                 letter = cv2.imread('bw_image.png', 1)
#                 winNum, pixDistance, endFlag, score, direction = getMinDistance(letter, winNum, centerX, centerY, score)
#                 cv2.circle(letter, (centerX, centerY), 1, (0, 0, 255), -1)
#             else: #Play the game
#                 winNum, pixDistance, endFlag, score, direction = getMinDistance(letter, winNum, centerX, centerY, score)
#                 cv2.circle(letter, (centerX, centerY), 1, (0, 0, 255), -1)
#                 print ("Distance = %s, direction = %s, Win# %s"% (pixDistance, direction, winNum))
#                 msg = ("{0},{1}".format(direction, pixDistance))
#                 #send distance to arduino here!
#                 client.publish("motors",msg)
#
#
#
#     cv2.imshow("Learn to Write!", letter)
#     key = cv2.waitKey(1) & 0xFF
#
#     # if the q key is pressed, stop the loop
#     if key == ord("q") or endFlag == True:
#         msg = ("{0},{1}".format(0, 0 ))
#         client.publish("motors",msg)
#         print("Your Score is %s letter pixels hit out of 611 letter pixels"%(score))
#         break
#
# camera.release()
# cv2.destroyAllWindows()


###################################################################### ARCHIVE ###################################################################
#Below is a failed attempt at automating the creation of Decision Windows

# def isPixUp(img, y, x, wId):
#     y = y-3
#     for xw in range(x, x+2):
#         for yw in range(y-2, y):
#             if xw >= 1920: break
#             elif img[yw, xw] == 0:
#                 wId += 1
#                 dWinList.append(Dwin(wId, y, y-3, x, x+3, 'u'))
#                 return y, x, wId
#     return y, x, wId

# def isPixUpperRight(img, y, x, wId):
#     y = y-3
#     x = x+3
#     for xw in range(x, x+2):
#         for yw in range(y-2, y):
#             if xw >= 1920: break
#             elif img[yw, xw] == 0:
#                 wId += 1
#                 dWinList.append(Dwin(wId, y, y-3, x, x+3, 'ur'))
#                 return y, x, wId
#     return 0

# def isPixRight(img, y, x, wId):
#     x = x+5
#     for xw in range(x, x+4):
#         for yw in range(y-4, y+1):
#             if img[yw, xw] == 0:
#                 wId += 1
#                 dWinList.append(Dwin(wId, y, y-5, x, x+5, 'r'))
#                 return y, x, wId
#     return 0

# def isPixLeft(img, y, x, wId):
#     x = x - 10
#     for xw in range(x, x+4):
#         for yw in range(y-4, y):
#             if img[yw, xw] == 0:
#                 wId += 1
#                 dWinList.append(Dwin(wId, y, y-5, x, x+5, 'l'))
#                 return y, x, wId
#     return 0

# def isPixUpperLeft(img, y, x, wId):
#     y = y-5
#     x = x-5
#     for xw in range(x, x+4):
#         for yw in range(y-4, y):
#             if xw >= 1920: break
#             elif img[yw, xw] == 0:
#                 wId += 1
#                 dWinList.append(Dwin(wId, y, y-5, x, x+5, 'ul'))
#                 return y, x, wId
#     return 0

# def isPixDown(img, y, x, wId):
#     y = y+5
#     for xw in range(x, x+4):
#         for yw in range(y-4, y):
#             if xw >= 1920: break
#             elif img[yw, xw] == 0:
#                 wId += 1
#                 dWinList.append(Dwin(wId, y, y-5, x, x+5, 'd'))
#                 return y, x, wId
#     return

# def isPixDownLeft(img, y, x, wId):
#     y = y+5
#     x = x-5
#     for xw in range(x, x+9):
#         for yw in range(y-9, y):
#             if xw >= 1920: break
#             elif img[yw, xw] == 0:
#                 wId += 1
#                 dWinList.append(Dwin(wId, y, y-5, x, x+5, 'dl'))
#                 return y, x, wId
#     return 0

# def isPixDownRight(img, y, x, wId):
#     y = y+5
#     x = x+5
#     for xw in range(x, x+9):
#         for yw in range(y-9, y):
#             if xw >= 1920: break
#             elif img[yw, xw] == 0:
#                 wId += 1
#                 dWinList.append(Dwin(wId, y, y-5, x, x+5, 'dr'))
#                 return y, x, wId
#     return 0

# def createFirstDWindow(img, y, x, wId):
#     dWinList.append(Dwin(wId, y, y-5, x, x+5, 'fr')) #create first window at the most lower left pixel
#     return y, x, wId

# def initLetter(img, class_type = "Dwin"):
#     """Convert img to BW and Create Decision windows"""
#     #change the image to black and white
#     changeToBW(img)
#     # find the height, width, of the image
#     ys = img.shape[0]
#     xs = img.shape[1]
#     oneTimeFlag = 1
#     wId = 1
#     #iterate over image starting at bottom left to find most lower left pixel
#     x = 0
#     y = ys-1
#     while x < xs-1:
#         y = ys-1
#         while  y > 0:
#             if img[y, x] == 0:
#                 if oneTimeFlag:
#                     oneTimeFlag = 0
#                     y, x, wId = createFirstDWindow(img, y, x, wId)
#                     y, x, wId = isPixUp(img, y, x, wId)
#                     y, x, wId = isPixUpperRight(img, y, x, wId)
#                     y, x, wId = isPixUp(img, y, x, wId)
#                     y, x, wId = isPixUpperRight(img, y, x, wId)


#                     return
#             else:
#                 y -= 1
#         x += 1
