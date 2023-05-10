import os
import numpy as np
import cv2
from keras.models import load_model
from matplotlib import pyplot as plt


# Match contours to license plate or character template
def find_contours(dimensions, img) :

    # Find all contours in the image
    cntrs, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Retrieve potential dimensions
    lower_width = dimensions[0]
    upper_width = dimensions[1]
    lower_height = dimensions[2]
    upper_height = dimensions[3]
    
    # Check largest 5 or  15 contours for license plate or character respectively
    cntrs = sorted(cntrs, key=cv2.contourArea, reverse=True)[:15]
    
    # ii = cv2.imread('contour.jpg')
    
    x_cntr_list = []
    target_contours = []
    img_res = []
    for cntr in cntrs :
        # detects contour in binary image and returns the coordinates of rectangle enclosing it
        intX, intY, intWidth, intHeight = cv2.boundingRect(cntr)
        
        # checking the dimensions of the contour to filter out the characters by contour's size
        if intWidth > lower_width and intWidth < upper_width and intHeight > lower_height and intHeight < upper_height :
            x_cntr_list.append(intX) #stores the x coordinate of the character's contour, to used later for indexing the contours

            char_copy = np.zeros((44,24))
            # extracting each character using the enclosing rectangle's coordinates.
            char = img[intY:intY+intHeight, intX:intX+intWidth]
            char = cv2.resize(char, (20, 40))
            
            # cv2.rectangle(img, (intX,intY), (intWidth+intX, intY+intHeight), (50,21,200), 2)

            # Make result formatted for classification: invert colors
            char = cv2.subtract(255, char)

            # Resize the image to 24x44 with black border
            char_copy[2:42, 2:22] = char
            char_copy[0:2, :] = 0
            char_copy[:, 0:2] = 0
            char_copy[42:44, :] = 0
            char_copy[:, 22:24] = 0

            img_res.append(char_copy) # List that stores the character's binary image (unsorted)
            
    # Return characters on ascending order with respect to the x-coordinate (most-left character first)
            
    # arbitrary function that stores sorted list of character indeces
    indices = sorted(range(len(x_cntr_list)), key=lambda k: x_cntr_list[k])
    img_res_copy = []
    for idx in indices:
        img_res_copy.append(img_res[idx])# stores character images according to their index
    img_res = np.array(img_res_copy)

    return img_res


# Find characters in the resulting images
def segment_characters(image) :

    # Preprocess cropped license plate image
    h, w = image.shape[:2]
    # Preprocess cropped license plate image
    if h < 100 and w > 200: img_lp = cv2.resize(image, (333, 75))
    else : img_lp = cv2.resize(image, (333, 150))
    img_gray_lp = cv2.cvtColor(img_lp, cv2.COLOR_BGR2GRAY)
    img_gray_lp = cv2.GaussianBlur(img_gray_lp, (3, 3), 0)
    _, img_binary_lp = cv2.threshold(img_gray_lp, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernel = np.ones((5,5),np.uint8)
    img_binary_lp = cv2.dilate(img_binary_lp,kernel,iterations = 1)
    img_binary_lp = cv2.erode(img_binary_lp,kernel,iterations = 1)

    LP_WIDTH = img_binary_lp.shape[0]
    LP_HEIGHT = img_binary_lp.shape[1]

    # Make borders white
    img_binary_lp[0:3,:] = 255
    img_binary_lp[:,0:3] = 255
    img_binary_lp[72:75,:] = 255
    img_binary_lp[:,330:333] = 255

    # Estimations of character contours sizes of cropped license plates
    dimensions = [LP_WIDTH/6,
                       LP_WIDTH/2,
                       LP_HEIGHT/10,
                       2*LP_HEIGHT/3]

    # cv2.imwrite('contour.jpg',img_binary_lp)
    # Get contours within cropped license plate
    char_list = find_contours(dimensions, img_binary_lp)

    return char_list

# Predicting the output
def fix_dimension(img): 
    new_img = np.zeros((28,12,3))
    for i in range(3):
        new_img[:,:,i] = img
        return new_img

def detectChar(q1, img_path, e):
    model = load_model("E:/PBL5/server/hardware/ai/models/model.h5")
    image = cv2.imread(img_path)
    h, w = image.shape[:2]
    char=segment_characters(image)
    dic = {}
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i,c in enumerate(characters):
        dic[i] = c
    str = ""
    if h < 100 :
      for i in range(len(char)):
        img_ = cv2.resize(char[i], (12,28), interpolation=cv2.INTER_AREA)
        img = fix_dimension(img_)
        img = img.reshape(1,28,12,3) #preparing image for the model
        predictions = model.predict(img)
        index = np.argmax(predictions, axis = 1)
        str += dic[index[0]]
    else :
      str1 = ""
      str2 = ""
      for i in range(len(char)):
        img_ = cv2.resize(char[i], (12,28), interpolation=cv2.INTER_AREA)
        img = fix_dimension(img_)
        img = img.reshape(1,28,12,3) #preparing image for the model
        predictions = model.predict(img)
        index = np.argmax(predictions, axis = 1)
        if (i+1) % 2 == 0 and i+1 <= len(char) - 1:
          str1 += dic[index[0]]
        else : 
          str2 += dic[index[0]]
      str = str1 + str2
    e.set()
    q1.put(str)
    return str
