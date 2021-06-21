import numpy as np
import cv2
import math
import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw
import pandas as pd
############################################################ Global Variables ###############################################
filename = 'bw_imageTinyExcel.xls'#'bw_imageTinyModifiedExcel.xls'
df = pd.read_excel(filename, index_col=0)
#df.fillna(0.5)

letter = df.to_numpy()

#grabs a numpy array of excel
letter_array = np.array(letter, dtype=np.uint8)

height = letter_array.shape[0]
width = letter_array.shape[1]

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
      if letter_array[yRow][xColumn] == 0: #white
          image_arr[yRow][xColumn] = (255, 255, 255)
      else:
          image_arr[yRow][xColumn] = (0, 0, 0)


# array = np.array(arr, dtype=np.uint8)
# #print(arr)
# new_image = Image.fromarray(array)
# new_image.save('DWTest1.png')
image_array_numpy = np.array(image_arr, dtype=np.uint8)

new_image = Image.fromarray(image_array_numpy)
#new_image.show()
new_image.save('ImageFromExcel.png')
#new_image.show()
# Use PIL to create an image from the new array of pixels

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
