from PIL import Image
import numpy as np
import cv2
import xlwt

filename = 'bw_image.png'
letter = cv2.imread(filename, 1)
#controls whether the excel file will have 0s
fillEmptyWithZeros = True


White = [255,255,255]
Black = [0,0,0]
nearBlack = [5,5,5]
pixColor = []
pixLoc = []


class PixelLocation(object):
    def __init__(self, pixNum=0, yLoc=0, xLoc=0, pixR=0, pixG=0, pixB =0):
        self.pixNum =pixNum
        self.yLoc= yLoc
        self.xLoc= xLoc
        self.pixR= pixR
        self.pixG= pixG
        self.pixB= pixB


def changeToBW (img):
    """Change image to Black and White"""
    # find the height, width, of the image
    ys = img.shape[0]
    xs = img.shape[1]
    #iterate over entire image starting at top left
    for x in range(0, xs):
        for y in range(0, ys):
            pixC = img[y, x]
            if pixC > 5: #if a pixel is not black/near black make it true white
                img[y,x] = 255
            else: #if a pixel is black/near black make it true black
                img[y,x] = 0

def initLetter(img, class_type = "PixelLocation"):
 #change the image to black and white
    # find the height, width, of the image
    ys = img.shape[0]
    xs = img.shape[1]
    #iterate over image starting at bottom left to find most lower left pixel
    x = 0
    y = ys-1
    num = 0
    while x < xs-1:
        y = ys-1
        while  y > 0:
            #if  np.array_equal(img[y, x],Black):
            if np.array_equal(img[y, x],White) == False:
              #  num += 1
                pixLoc.append(PixelLocation(num, y, x))
            #    pixColor[num] = img[y,x]
                y -= 1
            else:
                y -= 1
        x += 1

def excelOutput(excelFilename, sheet, class_type = "PixelLocation"):
    i = 1
        height = letter.shape[0]
    width = letter.shape[1]

    #populates 0s
    #if (fillEmptyWithZeros):
    #    for x in range(0, width):
    #        for y in range(height, 0, -1):
    #            sh.write(y, x, 0)

    #populates and shades areas with 1s
    #xlwt.add_palette_colour("custom_colour", 0x21)
    #book.set_colour_RGB(0x21, 251, 228, 228)
    #style = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour')

    #sh._cell_overwrite_ok = True #allows values on excel doc to be overwritten
    #for pixelLocation in pixLoc:
    #    sh.write(pixelLocation.yLoc, pixelLocation.xLoc, 1, style) #populates 1 for where there is writing
    #sh._cell_overwrite_ok = False


    #creates name for excel file
    #fileOutput = excelFilename.replace(".png", "").replace(".jpeg", "")
    #fileOutput = fileOutput + "Excel.xls"

    #book.save(fileOutput)
    #print("Image written to", fileOutput)

#letter = resizeImage(letter)
initLetter(letter, pixLoc)

#excelOutput(filename, '1', pixLoc)



pixels = [
   [(54, 54, 54), (232, 23, 93), (71, 71, 71), (168, 167, 167)],
   [(204, 82, 122), (54, 54, 54), (168, 167, 167), (232, 23, 93)],
   [(71, 71, 71), (168, 167, 167), (54, 54, 54), (204, 82, 122)],
   [(168, 167, 167), (204, 82, 122), (232, 23, 93), (54, 54, 54)]
]

# Convert the pixels into an array using numpy
array = np.array(pixels, dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array)
new_image.save('new.png')
