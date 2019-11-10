import cv2 
import numpy as py 
import os, os.path
import glob
from PIL import Image
import time
DIR = 'C:\\Users\\PF1MNVJD\\Documents\\ปริญญานิพนธ์\\Code\\PCBInspection\\image\\Raw_OK'
print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))

ddir = dir(cv2)
for i in ddir:
    if i == "imread":
        print("this have")
n =0 
image_list = []
for filename in glob.glob(DIR+'*.bmp'): #assuming gif
    im=Image.open(filename)
    im.show()
    image_list.append(im)
    time.sleep(1)
    print(n = n +1)
    
#img = cv2.imread('C:\\Users\\PF1MNVJD\\Documents\\ปริญญานิพนธ์\\Code\\PCBInspection\\image\\Raw_OK\\Image__2019-11-09__18-51-53.bmp')
#res = cv2.resize()
#if img == None:
#    print("emtry")
#else:    
    #cv2.imshow('image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
