#Engineers: Sean Duback, Robert Geoffrion
#School: Weber State University
#Project: Motion Tracking
#Year: 2019 Academic Year

#Engineers: Michael Lewson
#School: Chapman University
#Project: Motion Tracking
#Year: 2021 Academic Year


import numpy as np
# import cv2
import math
#import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw
import pandas as pd

import asyncio
import random
#import logging
import msvcrt
from bleak import BleakClient
############################################################ Global Variables ###############################################

excelFilePath = 'letter_images/Letter_L_Excelv2.xls' #grabs the decision windows from excel file

df = pd.read_excel(excelFilePath, index_col=0) #grabs excel file converts to data file
letter = df.to_numpy() #converts to numpy
#letter = np.resize(letter, (512, 512))

address = "7c:9e:bd:ee:7a:82"#'7c:9e:bd:ee:7a:80'#"3C:71:BF:FF:5E:5A" # Change the MAC address for your specific ESP32 here
UUID_NORDIC_TX = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
UUID_NORDIC_RX = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"


#y: 0 is B2
#y -1 is the bottommost y point
#letter[y][x]
#x 0 is B
#x -1 is the furthest x point point

white = [255,255,255]
black = [0,0,0]
nearBlack = [5,5,5]
dWinList = []


pixDistance = 0
pixDistFirst = []
pixDirFirst = {}
pixDistSecond = []
pixDirSecond = {}
pixDistStart = 100
minPixDist = {}
# grab the reference to the webcam
# camera = cv2.VideoCapture(0)
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

def showDwin():
    letter_image = extractImageFromExcel(letter)
    #extracts decision windows
    extractDecisionWindowsFromExcel()
    #colors the decision windows over the image
    colorDwin(letter_image)
    #shows the image
    letter_image = Image.fromarray(letter_image)
    letter_image.show()

def totalDistance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)


def start (img, inputX, inputY):

    for x in range(dWinList[0].xmin, dWinList[0].xmax):
        for y in range(dWinList[0].ymin, dWinList[0].ymax, -1):
            if np.array_equal(img[y, x], black):
                pixDistStart = int(totalDistance(x, y, inputX, inputY))
                if pixDistStart <= 5:
                    return True
    return False

def getdirection(inputX, inputY, x, y):
    yDistance = y - inputY
    xDistance = x - inputX
    if abs(yDistance) >= abs(xDistance):
        if y >inputY: return 3
        else: return 1
    else:
        if x > inputX: return 4
        else: return 2


def getMinDistance (img, dWinNum, inputX, inputY, score):
    FirstKey = 0 #used as flags for distance to not update min distince if no new values
    SecondKey = 0 #used as flags for distance to not update min distince if no new values
    direction = 0
    #print("DwinNum = %s"%(dWinNum))  #used for debugging
    if dWinNum == 36: #if the game is over return end game true, no currect dWin 36 in logic, game will never end
        return 36, 0, True
    else:
        for x in range(dWinList[dWinNum].xmin, dWinList[dWinNum].xmax):
            for y in range(dWinList[dWinNum].ymin, dWinList[dWinNum].ymax, -1):
                if np.array_equal(img[y, x], black):
                    yDistance = y - inputY
                    xDistance = x - inputX
                     #numpy.allclose(a, b, rtol=0, atol=3, equal_nan=False)
                    if yDistance <= 2 and xDistance <= 2: # a two pixel tolerance is added to the first window as a handicap for the user
                        score = score +1
                        pixDistFirst.clear()
                        pixDistSecond.clear()
                        pixDirFirst.clear()
                        pixDirSecond.clear()
                        return dWinNum, 0, False, score, direction
                    else:
                        FirstKey += 1 #Counts up as the loop goes on so every value has a unquie key in the dict
                        totalDisOne = int(totalDistance(x, y, inputX, inputY)) #the distance of the user input from the black pixel is calculated
                        pixDistFirst.insert(FirstKey, totalDisOne) #the distance is stored in a dict with the "FirstKey" acting as the key
                        pixDirFirst[totalDisOne] =  getdirection(inputX, inputY, x, y) #A direction is stored with using the distance as its location in a list


        for x in range(dWinList[dWinNum+1].xmin, dWinList[dWinNum+1].xmax):
            for y in range(dWinList[dWinNum+1].ymin, dWinList[dWinNum+1].ymax, -1):
                if  np.array_equal(img[y, x],black):
                    if np.array_equal(img[y,x], [inputY, inputX]): #if the input is on a letter pixel add one to score and return
                        score = score +1
                        pixDistFirst.clear()
                        pixDistSecond.clear()
                        pixDirFirst.clear()
                        pixDirSecond.clear()
                        return dWinNum+1, 0, False, score, direction
                    else:
                        SecondKey += 1 #Counts up as the loop goes on so every value has a unquie key in the dict
                        totalDisTwo = int(totalDistance(x, y, inputX, inputY))
                        pixDistSecond.insert(SecondKey, totalDisTwo)
                        pixDirSecond[totalDisTwo] =  getdirection(inputX, inputY, x, y)

        if FirstKey != 0:
            minPixDist.update({dWinNum: min(pixDistFirst)}) #the minimum distance from the first Dwin is taken
        else: minPixDist[dWinNum] = 1000 #used to asign a value to minPixDist if none was found
        if SecondKey != 0:
            minPixDist.update({dWinNum+1: min(pixDistSecond)})  #the minimum distance from the second Dwin is taken
        else: minPixDist[dWinNum+1] = 1000  #used to asign a value to minPixDist if none was found
        if (minPixDist[dWinNum+1] + 1) < minPixDist[dWinNum]: #compares the two min distances
            direction = pixDirSecond[minPixDist[dWinNum+1]] #grabs the direction associated with the minimum distance
            #print ("Window#= %s, Distance = %s, direction = %s"% (dWinNum+1, minPixDist[dWinNum+1], direction))  #used for debugging
            pixDistFirst.clear()
            pixDistSecond.clear()
            pixDirFirst.clear()
            pixDirSecond.clear()
            return dWinNum+1, minPixDist[dWinNum+1], False, score, direction
            #returns the new dWinNum, min distance, flag signaling the game is to continue, the current score, and direction
        #end the gmae here elif dwin 36 ... need to make it go to dwin 36 no current logic for a 36th decision window
# =============================================================================
#         else:
#             return dWinNum, 0, True, score, direction
# =============================================================================
        else:
            direction = pixDirFirst[minPixDist[dWinNum]]
            #print ("Window#= %s, Distance = %s, direction = %s"% (dWinNum, minPixDist[dWinNum], direction)) #used for debugging
            pixDistFirst.clear()
            pixDistSecond.clear()
            pixDirFirst.clear()
            pixDirSecond.clear()
            return dWinNum, minPixDist[dWinNum], False, score, direction



def extractEntireImage(address):
    print()

#function to grab the letter image from excel (but not the decision windows)
def extractImageFromExcel(letter):
    #grabs a numpy array of excel
    #letter_array = np.array(letter, dtype=np.uint8)
    letter_array = letter
    height = letter_array.shape[0]
    width = letter_array.shape[1]
    # height = 256
    # width = 256
    print("width, height", width,height)

    #creates a new array for the image (because can't change the type of numpy array to be proper pixels)
    rows, cols = (height, width)
    image_arr=[]
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append((255,255,255))
        image_arr.append(col)

    for yRow in range(0, height):
      for xColumn in range(0, width):
          if (not math.isnan (letter_array[yRow][xColumn])) and (letter_array[yRow][xColumn] == 0): #black pixels
              image_arr[yRow][xColumn] = (0, 0, 0)
          #else:
            #  image_arr[yRow][xColumn] = (0, 0, 0)

    image_array_numpy = np.array(image_arr, dtype=np.uint8)
    print("raw first image")
    new_image_temp = Image.fromarray(image_array_numpy)
    new_image_temp.show()
    print("I am here")
    return image_array_numpy



#function to grab the decision windows from excel
def extractDecisionWindowsFromExcel():
    dwDict = {}

    height = letter.shape[0]
    width = letter.shape[1]
    #extracts the coordinates of the decision windows by reading through excel file
    for yRow in range(0, height):
      for xColumn in range(0, width):
          #if letter[yRow][xColumn]!= 'nan':
          if not (math.isnan (letter[yRow][xColumn])):
              DW_Number = letter[yRow][xColumn]
              if DW_Number in dwDict:
                  #to be replaced with coordinates
                  dwDict[DW_Number] += [xColumn, yRow]
              else:
                  #first value of it found, creates the section
                  dwDict[DW_Number] = [xColumn, yRow]

    print("number of decision windows", len(dwDict))
    #print(dwDict)
     #dw format: Ymin, YMax, XMin, XMax
    for key in dwDict:
        if len(dwDict[key]) == 4:
            #print(dwDict[key])
            x1 = dwDict[key][0]
            x2 = dwDict[key][2]
            y1 = dwDict[key][1]
            y2 = dwDict[key][3]
            #print(dwDict[key][1], dwDict[key][3])
            #print(y1,y2,x1,x2)

            #determine Ymin, YMax, XMin, XMax
            #ymin is bigger
            #xmax is bigger
            if y1 > y2:
                yMin = y1
                yMax = y2
            else:
                yMin = y2
                yMax = y1
            if x1 > x2:
                xMax = x1
                xMin = x2
            else:
                xMax = x2
                xMin = x1
            #Ymin, YMax, XMin, XMax

            dWinList.append(Dwin(key, yMin, yMax, xMin, xMax))


        #else:
        #    print("Please ensure there are 2 points per decision window")
            #print(dwDict[key])
        dWinList.sort(key=lambda x: x.idnum, reverse=False)
        #ut.sort(key=lambda x: x.count, reverse=True)

def init():

    #so we have an excel file of the image with numbers marked for each coord
    #find the coord of each number then make the decision window from there

    height = letter.shape[0]
    width = letter.shape[1]
    #grabs the image
    # letter_image = extractImageFromExcel(letter)
    # #extracts decision windows
    extractDecisionWindowsFromExcel()




############################################################# Main ########################################################
#init()
showDwin()
# letter = extractImageFromExcel(letter)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main(address, loop, letter))
# camera.release()
# cv2.destroyAllWindows()



###################################################################### ARCHIVE ###################################################################
