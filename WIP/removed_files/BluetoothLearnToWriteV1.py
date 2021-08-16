


# Haptic Sleeve Testing Program
# By Grant Stankaitis
#
# Summary:
# This program is used to test the Haptic Sleeve.
# Commands are sent programmatically to test various scenarios.
# Everything is logged, so check the log file for analysis.
# When test cases are running, select ONLY numerical or alphabetical keys (NO arrow keys, enter, etc.).
# This is due to msvcrt.getche()- Reads a keypress, returns the resulting character; does not wait for Enter press.
#
# The 3 testing scenarios are:
# Accuracy, being able to correctly decipher the correct direction
# Speed, how quick the user can react to haptic feedback
# Intensity, can the user distinguish between different vibrational intensities?
#
# Directions:
# Accuracy: Press W-A-S-D keys for directions, NOT arrow keys
# W- Forward, A- Left, S- Back, D- Right
# Speed: User can pick any key to press, select ONLY numerical or alphabetical keys
# Intensity: User can select 1, 2, 3 to pick intensity level

#learn to write


import numpy as np
import cv2
import math
#import paho.mqtt.client as mqtt



import time
import asyncio
import random
import logging
import msvcrt
from bleak import BleakClient
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
camera = cv2.VideoCapture(0)
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
                    print ("x=%s y=%s"%(x, y))
                    img[y, x] = white
                else:
                     img[y, x] = 0

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


############################################################# Main ########################################################
# def startLearnToWrite():
#     init()
#     #colorDwin(letter, dWinList) #used to color in the dWin black for debugging
#
#     #CHANGE HERE!!!!!
#     # broker = "192.168.43.175"
#     # client = mqtt.Client("computer2")
#     # client.connect(broker)
#
#     #CHANGE HERE!
#
#     while True:
#         cv2.imshow("Learn to Write!", letter)
#         key = cv2.waitKey(1) & 0xFF
#
#         # grab the current frame
#         (grabbed, frame) = camera.read()
#         frame = cv2.flip(frame, 1)
#
#         # resize the frame, blur it, and convert it to the HSV color space
#         blurred = cv2.GaussianBlur(frame, (11, 11), 0)
#         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#
#         # construct a mask for the color then perform a series of dilations and erosions to remove any small blobs left in the mask
#         mask = cv2.inRange(hsv, colorLower, colorUpper)
#         mask = cv2.erode(mask, None, iterations=2)
#         mask = cv2.dilate(mask, None, iterations=2)
#
#         # find contours in the mask and initialize the current (x, y) center of the ball
#         cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
#         #center = None #why is center none?
#
#         # only proceed if at least one contour was found
#         if len(cnts) > 0:
#             # find the largest contour in the mask, then use centroid
#             c = max(cnts, key=cv2.contourArea)
#             ((x, y), radius) = cv2.minEnclosingCircle(c)
#             M = cv2.moments(c)
#             centerX = (int(M["m10"] / M["m00"])+50)
#             centerY = (int(M["m01"] / M["m00"])+50)
#             #print("X is %s, Y is %s"%(int(centerX),int(centerY))) #used for debugging
#             #if centerX < 800 and centerY < 600:
#             if startFlag == False: #Wait until input is near Dwin 0 to start game
#                 cv2.circle(letter, (centerX, centerY), 1, (0, 0, 255), -1)
#                 startFlag = start(letter, centerX,centerY)
#             else:
#                 if oldStartFlag == False: #Clean the img on game start
#                     oldStartFlag = True
#                     letter = cv2.imread('bw_image.png', 1)
#                     winNum, pixDistance, endFlag, score, direction = getMinDistance(letter, winNum, centerX, centerY, score)
#                     cv2.circle(letter, (centerX, centerY), 1, (0, 0, 255), -1)
#                 else: #Play the game
#                     winNum, pixDistance, endFlag, score, direction = getMinDistance(letter, winNum, centerX, centerY, score)
#                     cv2.circle(letter, (centerX, centerY), 1, (0, 0, 255), -1)
#                     print ("Distance = %s, direction = %s, Win# %s"% (pixDistance, direction, winNum))
#                     msg = ("{0},{1}".format(direction, pixDistance))
#                     #send distance to arduino here!
#                     client.publish("motors",msg)
#
#
#
#         cv2.imshow("Learn to Write!", letter)
#         key = cv2.waitKey(1) & 0xFF
#
#         # if the q key is pressed, stop the loop
#         if key == ord("q") or endFlag == True:
#             msg = ("{0},{1}".format(0, 0 ))
#             # client.publish("motors",msg)
#             print("Your Score is %s letter pixels hit out of 611 letter pixels"%(score))
#             break
#
#     camera.release()
#     cv2.destroyAllWindows()











# def StartLearnToWrite():
#         height = letter.shape[0]
#         width = letter.shape[1]
#         #grabs the image
#         letter_image = extractImageFromExcel(letter)
#         #extracts decision windows
#         extractDecisionWindowsFromExcel()
#         #colors the decision windows over the image
#         colorDwin(letter_image)
#         #shows the image
#         letter_image = Image.fromarray(letter_image)
#         letter_image.show() #shows the decision windows on the original image
#



#testing modules


# Define UUIDs for Nordic UART Service
address = "7c:9e:bd:ee:7a:82"#'7c:9e:bd:ee:7a:80'#"3C:71:BF:FF:5E:5A" # Change the MAC address for your specific ESP32 here
UUID_NORDIC_TX = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
UUID_NORDIC_RX = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

# Lists that contain commands to activate motors
# Command b"4,2" is interpreted as direction: 4, intensity: 2
# 4 possible directions, 3 possible intensity levels
# 1 is forward, 2 left, 3 back, 4 right
# 0,0 is all motors off
command_list = [b"1,2", b"2,2", b"3,2", b"4,2"]
command_list_intensity1 = [b"1,1", b"1,2", b"1,3"]
command_list_intensity2 = [b"2,1", b"2,2", b"2,3"]
command_list_intensity3 = [b"3,1", b"3,2", b"3,3"]
command_list_intensity4 = [b"4,1", b"4,2", b"4,3"]
command = b"0,0"

# Configure logging parameters
log_date = time.strftime("%Y%m%d_%H%M%S", time.localtime())
log_name = "results_" + log_date + ".log"
logging.basicConfig(filename=log_name, filemode="a", format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                    level=logging.DEBUG)
logging.info("\n\n")
logging.info("PROGRAM BEGINS")


# Coroutine to run tests, based on which command list is picked to send from
# 50 loop iterations for accuracy, 30 for speed test 1, 50 for speed test 2, 30 for intensity
async def run_test(client, loop, command_list, loop_iterations):
    command_len = len(command_list)
    print("\nTest starting in: \n3")
    await asyncio.sleep(1.0, loop=loop)
    print("2")
    await asyncio.sleep(1.0, loop=loop)
    print("1")
    await asyncio.sleep(1.0, loop=loop)
    print("Start!")

    # All commands and keystrokes recorded
    previous_command = b""
    for i in range(loop_iterations):
        j = 0
        # Create temporary list to modify while iterating
        temp_command_list = command_list[:]
        while(j < command_len):
            # Choose/store a random command, make sure it isn't the same command randomly selected from previous loop
            # Remove command from list, then send command
            # Log command sent and log single keystroke from user
            motor_command = random.choice(temp_command_list)
            if motor_command != previous_command:
                temp_command_list.remove(motor_command)
                await client.write_gatt_char(UUID_NORDIC_TX, bytearray(motor_command[0:20]), True)
                logging.debug("Direction sent: " + str(motor_command))
                user_direction = msvcrt.getche()
                logging.debug("Key pressed: " + str(user_direction))
                previous_command = motor_command
                j += 1
    # Turn all motors off
    motor_command = command
    await client.write_gatt_char(UUID_NORDIC_TX, bytearray(motor_command[0:20]), True)
    logging.debug("ALL OFF, Direction sent: " + str(motor_command))
    logging.debug("Key pressed: b'0'")
    print("\nDone!")


async def run_training(client):
    print("\nUser training started.")
    print("Select a vibrational intensity using 1, 2, or 3.")
    intensity = msvcrt.getche()
    print("\nNow select motor directions to activate using W-A-S-D.")
    print("Press E to select a new intensity level. Q to exit training.")

    # Wait on input from user and send command for appropriate keypress
    while(True):
        direction = msvcrt.getche()
        if direction == b"w": # Forward
            user_command = b"1," + intensity
            await client.write_gatt_char(UUID_NORDIC_TX, bytearray(user_command[0:20]), True)
        elif direction == b"a": # Left
            user_command = b"2," + intensity
            await client.write_gatt_char(UUID_NORDIC_TX, bytearray(user_command[0:20]), True)
        elif direction == b"s": # Back
            user_command = b"3," + intensity
            await client.write_gatt_char(UUID_NORDIC_TX, bytearray(user_command[0:20]), True)
        elif direction == b"d": # Right
            user_command = b"4," + intensity
            await client.write_gatt_char(UUID_NORDIC_TX, bytearray(user_command[0:20]), True)
        elif direction == b"e": # Change intensity then continue training
            await client.write_gatt_char(UUID_NORDIC_TX, bytearray(command[0:20]), True)
            print("\nInput a new intensity level: ")
            intensity = msvcrt.getche()
            print()
        else: # All motors off and exit
            await client.write_gatt_char(UUID_NORDIC_TX, bytearray(command[0:20]), True)
            break

def StartLearnToWrite():
    white = [255,255,255]
    black = [0,0,0]
    nearBlack = [5,5,5]
    dWinList = []
    #letter = cv2.imread('bw_image.png', 1)
    pixDistance = 0
    pixDistFirst = []
    pixDirFirst = {}
    pixDistSecond = []
    pixDirSecond = {}
    pixDistStart = 100
    minPixDist = {}
    # grab the reference to the webcam
    camera = cv2.VideoCapture(0)
    # define the lower and upper boundaries of the "orange"
    colorLower = (0, 120, 70)
    colorUpper = (50, 255, 180)
    winNum = 0

    startFlag = False
    oldStartFlag = False
    endFlag = False
    score = 0
    print("STARTING LEARN TO WRITE!")
    init()
    letter = cv2.imread('bw_image.png', 1)
    # broker = "192.168.43.175"
    # client = mqtt.Client("computer2")
    # client.connect(broker)
    while True:
        cv2.imshow("Learn to Write!", letter)
        key = cv2.waitKey(1) & 0xFF

        # grab the current frame
        (grabbed, frame) = camera.read()
        frame = cv2.flip(frame, 1)

        # resize the frame, blur it, and convert it to the HSV color space
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color then perform a series of dilations and erosions to remove any small blobs left in the mask
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        #center = None #why is center none?

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            centerX = (int(M["m10"] / M["m00"])+50)
            centerY = (int(M["m01"] / M["m00"])+50)
            #print("X is %s, Y is %s"%(int(centerX),int(centerY))) #used for debugging
            #if centerX < 800 and centerY < 600:
            if startFlag == False: #Wait until input is near Dwin 0 to start game
                cv2.circle(letter, (centerX, centerY), 1, (0, 0, 255), -1)
                startFlag = start(letter, centerX,centerY)
            else:
                if oldStartFlag == False: #Clean the img on game start
                    oldStartFlag = True
                    letter = cv2.imread('bw_image.png', 1)
                    winNum, pixDistance, endFlag, score, direction = getMinDistance(letter, winNum, centerX, centerY, score)
                    cv2.circle(letter, (centerX, centerY), 1, (0, 0, 255), -1)
                else: #Play the game
                    print("first DW found, starting game!")
                    winNum, pixDistance, endFlag, score, direction = getMinDistance(letter, winNum, centerX, centerY, score)
                    cv2.circle(letter, (centerX, centerY), 1, (0, 0, 255), -1)
                    print ("Distance = %s, direction = %s, Win# %s"% (pixDistance, direction, winNum))
                    msg = ("{0},{1}".format(direction, pixDistance))
                    print(msg)
                    #send distance to arduino here!
                    #client.publish("motors",msg)
                    #ADD BLUETOOTH HERE
                    #
                    #with BleakClient(address, loop=loop) as client:
                        #print("Select a vibrational intensity using 1, 2, or 3.")
                        #intensity = msvcrt.getche()
                        #user_command = b"1," + intensity
                        #sends over the bluetooth
                        #client.write_gatt_char(UUID_NORDIC_TX, bytearray(user_command[0:20]), True)

                    #
                    #




        cv2.imshow("Learn to Write!", letter)
        key = cv2.waitKey(1) & 0xFF

        # if the q key is pressed, stop the loop
        if key == ord("q") or endFlag == True:
            msg = ("{0},{1}".format(0, 0 ))
            #ADD BLUETOOTH HERE!
            #
            #
            #
            # client.publish("motors",msg)
            print("Your Score is %s letter pixels hit out of 611 letter pixels"%(score))
            break

    camera.release()
    cv2.destroyAllWindows()

# Main coroutine
# Will attempt to connect to ESP32 via BLE MAC address
# Once connected, the program will then take user input to run tests
# The test cases are run as coroutines
# The main coroutine will wait on the test case coroutine before continuing the loop
async def main(address, loop):
    while True:  # Loop to allow reconnection
        try: # Attempt to connect to ESP32
            print("Connecting\n")
            async with BleakClient(address, loop=loop) as client:
                print("Connected!\n")
                print("Please input your name: ")
                username = input()
                logging.debug("User: " + username)
                while True: # Main loop, user selects test case
                    print("\n\nSelect the option you want to run then ENTER:")
                    print("0- Learn To Write")
                    print("1- Accuracy, 2- Speed")
                    print("3- Speed + Accuracy, 4- Intensity")
                    print("5- User Training, Any other int- QUIT")
                    select_test = int(input())

                    # Call coroutine function and wait on it to finish
                    if select_test == 0:
                        logging.debug("Starting Learn To Write!")
                        StartLearnToWrite()

                    elif select_test == 1:
                        logging.debug("Accuracy test started")
                        await run_test(client, loop, command_list, 13)
                        # 13 loop iterations * 4 motor commands/iteration = 52 responses
                    elif select_test == 2:
                        logging.debug("Speed test started")
                        await run_test(client, loop, command_list, 8)
                        # 8 loop iterations * 4 motor commands/iteration = 32 responses
                    elif select_test == 3:
                        logging.debug("Speed + Accuracy test started")
                        await run_test(client, loop, command_list, 13)
                    elif select_test == 4:
                        logging.debug("Intensity test started")
                        # Testing intensity levels on each motor
                        await run_test(client, loop, command_list_intensity1, 8)
                        await run_test(client, loop, command_list_intensity2, 8)
                        await run_test(client, loop, command_list_intensity3, 8)
                        await run_test(client, loop, command_list_intensity4, 8)
                    elif select_test == 5:
                        logging.debug("User training started")
                        await run_training(client)
                    else:
                        break
                break
        except Exception as e: # Catch connection exceptions, usually "device not found," then try to reconnect
            print(e)
            print('Trying to reconnect...')
            continue


if __name__ == "__main__":
    # Create an event loop to run the main coroutine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(address, loop))
