# LearnToWrite
Learn To Write Code
Contains the code for the Learn To Write Software as well as code for creating images for the software.

Files Included:
LearnToWrite.py
ImageToExcel.py
letter_images folder
log_files folder

LearnToWrite.py: Run the program.  Upon start, select the excel file containing your image with decision windows.

ImageToExcel.py: The program that converts image files into excel for labeling.  On Excel, you will see the image drawn on the columns and the rows.
To label the decision windows, find the area you want the user to start when writing.  Once there, we will begin making decision window 1.
To create the first decision window, place two number 1s in a way that they make a box (such as one 1 is the top left and the other 1 is the bottom right of a 2d box).  LearnToWrite will read this and create a decision window at this location.  To make additional decision windows, proceed to the number 2 with two coordinates of the number 2.
Once the decision window labeling is finished, place the finished excel file in the letter_images file.  Upon running LearnToWrite, you can select it and see if it runs.
