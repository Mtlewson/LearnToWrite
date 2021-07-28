from os import listdir
from os.path import isfile, join
mypath = "letter_images"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
option_list = []
file_dict = {}


for i in range (0, len(onlyfiles)):
    file_dict[str(i)]=onlyfiles[i]
    filename = onlyfiles[i].replace("_Excel", "").replace(".xlsx", "").replace(".xls","").replace("_", " ")
    #filename.replace(".png", "").replace(".jpeg", "")
    print("option:", i, filename)
    #option_list.append(str(i))

valid_input = False
filename = ""
while valid_input == False:
    user_input = input("Please enter number of file to select")
    if user_input in file_dict.keys():
        valid_input = True
        print(file_dict[user_input], "selected!")
    elif user_input.lower() == "quit":
        print("quit")
    else:
        print("invalid input")
