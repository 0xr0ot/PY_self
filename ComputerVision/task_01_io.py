# coding=utf-8

# import numpy as np
# import cv2



# img1 = np.zeros((3,3),dtype=np.uint8)
# print(img1)
# print(img1.shape)
#
# img2 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
# print(img2)
# print(img2.shape) #3通道rgb


# image = cv2.imread('jj1.jpg')
# cv2.imwrite('jj1.png',image)

# imgArray = bytearray(image)
# print(imgArray)
#grayArray = np.array(imgArray).reshape(108,103)


# grayImage = cv2.imread('jj1.jpg', cv2.IMREAD_GRAYSCALE)
# # cv2.imwrite('jj1_gray.jpg', grayImage)
#
# cv2.imshow('grayImage_name',grayImage)
# cv2.waitKey(1000*9)
# cv2.destroyAllWindows()




## homework_1:

# method_1:
import cv2

imageArray = cv2.imread('jj1.jpg')
print(imageArray,type(imageArray),imageArray.shape)

cv2.imshow('give_name',imageArray)
cv2.waitKey(1000*9)
cv2.destroyAllWindows()


# method_2:
import numpy as np
from PIL import Image

img = Image.open('jj1.jpg')
imgData = img.getdata()
width,height = img.size
imgArray = np.array(imgData,dtype=np.uint8).reshape(height,width,3)
print(imgArray,type(imgArray),imgArray.shape)

#print(imageArray == imgArray) rgb,gbr
print(imageArray == imgArray[:,:,::-1]) # True

img.show()
