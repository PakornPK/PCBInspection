import cv2
import numpy as np
import os
import os.path
import glob
from PIL import Image
from matplotlib import pyplot as plt


def crop_center(img,startx,starty,cropx, cropy):
    return img[starty:starty+cropy, startx:startx+cropx]


DIR = 'C:\\Users\\PF1MNVJD\\Documents\\ปริญญานิพนธ์\\Code\\PCBInspection\\image\\Raw_OK'
DIR_ok = 'C:\\Users\\PF1MNVJD\\Documents\\ปริญญานิพนธ์\\Code\\PCBInspection\\image\\OK\\'
print('Count number of file :', len(
    [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))

image_list = []
for filename in glob.glob(DIR_ok+'*.bmp'):
    im = Image.open(filename)
    image_list.append(im)

for i in range(1,len(image_list)):
    np_img = np.array(image_list[i])
    #crop_img = crop_center(np_img, 350,500,1700, 750)
    #np_img2 = cv2.resize(crop_img, dsize=(448, 448), interpolation=cv2.INTER_CUBIC)
    #mask_img = 5 * np.ones((1942,2590,3),dtype= int)
    #result = np.add(np_img,mask_img)
    result = np.dot(3, np_img)
    #kernel = np.ones((5,5),np.float32)/25
    #result = cv2.filter2D(np_img,-1,kernel)
    #kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    #result = cv2.filter2D(np_img, -1, kernel)
    np.clip(result, 0, 255, out=result)
    im = Image.fromarray(np.uint8(result))
    #im.show()
    name = DIR_ok + str(i+2185) + '.bmp'
    im.save(name)
