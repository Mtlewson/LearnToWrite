#Engineers: Sean Duback, Robert Geoffrion
#School: Weber State University
#Project: Motion Tracking
#Year: 2019 Academic Year

#Engineers: Michael Lewson
#School: Chapman University
#Project: Motion Tracking
#Year: 2021 Academic Year


import numpy as np
import cv2
import math
#import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw
import pandas as pd
############################################################ Global Variables ###############################################

excelFilePath = 'letter_images/Letter_M_Excel.xlsx' #grabs the decision windows from excel file

df = pd.read_excel(excelFilePath, index_col=0) #grabs excel file converts to data file
letter = df.to_numpy() #converts to numpy


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

#function to grab the letter image from excel (but not the decision windows)
def extractImageFromExcel(letter):
    #grabs a numpy array of excel
    #letter_array = np.array(letter, dtype=np.uint8)
    letter_array = letter
    height = letter_array.shape[0]
    width = letter_array.shape[1]
    #print(width,height)

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
    #new_image_temp = Image.fromarray(image_array_numpy)
    #new_image_temp.show()
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
    letter_image = extractImageFromExcel(letter)
    #extracts decision windows
    extractDecisionWindowsFromExcel()
    #colors the decision windows over the image
    colorDwin(letter_image)
    #shows the image
    letter_image = Image.fromarray(letter_image)
    letter_image.show() #shows the decision windows on the original image


############################################################# Main ########################################################
init()
