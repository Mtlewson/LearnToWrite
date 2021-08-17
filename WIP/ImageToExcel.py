#This program is used to take a png or jpeg image file and convert it into an excel file where decision windows can be added for the LearnToWrite program



import xlsxwriter
import numpy as np
import cv2

#image name
filename = 'circle_image.png'
letter = cv2.imread(filename, 1)

maxSize = 256 #adjusts image size for the excel output.  CANNOT EXCEED 256!
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

#function to resize image to fit into excel
# def resizeImage(img):
#
#   originalHeight = img.shape[0]
#   originalWidth = img.shape[1]
#   reduceRatio = 1
#   #calculates which side is bigger then resizes it
#   if originalHeight > originalWidth:
#       if originalHeight < maxSize: #no need for adjusting size as it is below max
#           return img
#       reduceRatio = float(originalHeight/maxSize)
#   else:
#       if originalWidth < maxSize:
#           return img
#       reduceRatio = float(originalWidth/maxSize)
#
#
#   adjustedWidth = int(originalWidth/reduceRatio)
#   adjustedHeight = int(originalHeight/reduceRatio)
#
#   print("Width is now", adjustedWidth, "Height is now", adjustedHeight)
#   dim = (adjustedWidth, adjustedHeight)
#
#   img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
#   return img


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
    # i = 1
    # book = xlwt.Workbook()
    # sh = book.add_sheet(sheet)
    #
    height = letter.shape[0]
    width = letter.shape[1]


     # Create a workbook and add a worksheet.
    fileOutput = filename.replace(".png", "").replace(".jpeg", "")
    workbook = xlsxwriter.Workbook(fileOutput + '_Excel.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0

    cell_format = workbook.add_format()
    cell_format.set_fg_color('gray')
    #worksheet.write(0, 0, 'Wheelbarrow', cell_format)
    for pixelLocation in pixLoc:
      worksheet.write(pixelLocation.yLoc, pixelLocation.xLoc, 0, cell_format) #populates 1 for where there is writing

    for x in range(0,width):
        worksheet.write(0, x, 0, cell_format)
        worksheet.write(height-1, x, 0, cell_format)
    for y in range(0, height):
        worksheet.write(y, 0, 0, cell_format)
        worksheet.write(y, width-1, 0, cell_format)

    workbook.close()


#letter = resizeImage(letter)
initLetter(letter, pixLoc)

excelOutput(filename, '1', pixLoc)
