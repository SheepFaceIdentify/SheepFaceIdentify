import cv2
import os
import random
import numpy as np
"""
    用作小波变换，采用哈尔小波
    类中含有三个函数：
    1.storage2storage(img)：
    所需参数--cv2的读入图像格式（多维数组），返回一个numpy数组，数组结构与
    读入的参量结构一致
    2.pic2pic(input_directory,output_directory):
    所需参数--一张图片的输入路径,图片的输出路径，返回一个小波变换后的图片
    示例：
    wave.pic2pic("/Users/mingcao/Desktop/1.jpg","/Users/mingcao/Desktop/2.jpg")
    3.
    

"""
class wave:
    def __init__(self):
        return
    def storage2storage(img):
        img_height=img.shape[0]
        img_width=img.shape[1]
        img_channel=img.shape[2]
        row_waved_img=np.zeros((img_height,img_width,img_channel),dtype=np.int16)       
        #储存行变换后的图片
        column_waved_img=np.zeros((img_height,img_width,img_channel),dtype=np.int16)
        #储存列变换后的图片
        half_height=img_height//2-1
        half_width=img_width//2-1
        img_array=np.array(img,dtype=np.int16)
        '''
        for i in range(img_channel):
            for j in range(img_height):
                for k in range(half_width):
                    row_waved_img[j,k,i]=(img[j,2*k,i]+img[j,2*k+1,i])/2
                    row_waved_img[j,k+half_width,i]=(img[j,2*k,i]-img[j,2*k+1,i])/2
        img=row_waved_img
        for i in range(img_channel):
            for j in range(img_width):
                for k in range(half_height):
                    column_waved_img[k,j,i]=(img[2*k,j,i]+img[2*k+1,j,i])/2
                    column_waved_img[k+half_height,j,i]=(img[2*k,j,i]-img[2*k+1,j,i])/2
        '''
        #使用numpy的科学计算比上面的做法速度快了近十倍
        for j in range(half_width):
            row_waved_img[:,j,:]=(img_array[:,2*j,:]+img_array[:,2*j+1,:])/2
            row_waved_img[:,j+half_width,:]=(img_array[:,2*j,:]-img_array[:,2*j+1,:])/2
        img_array=row_waved_img
        for k in range(half_height):
            column_waved_img[k,:,:]=(img_array[2*k,:,:]+img_array[2*k+1,:,:])/2
            column_waved_img[k+half_height,:,:]=(img_array[2*k,:,:]-img_array[2*k+1,:,:])/2
        return column_waved_img
    def pic2pic(input_directory,output_directory):
        img=cv2.imread(input_directory)
        cv2.imwrite(output_directory,wave.storage2storage(img))
        if cv2.waitKey(0)== 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()

'''
#下面是测试类功能的代码，去掉注释即可测试
#测试时需要在当前目录下准备一张名为"1.jpg"的图片
#测试storage2storage(img)功能：
img=cv2.imread("1.jpg")
cv2.imwrite("2.jpg",wave.storage2storage(img))
if cv2.waitKey(0)== 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
#测试pic2pic(input_directory,output_directory)功能：
wave.pic2pic("./1.jpg","./2.jpg")

cv2.imwrite("2.jpg",wave.storage2storage(img))
if cv2.waitKey(0)== 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.destroyAllWindows()
'''

