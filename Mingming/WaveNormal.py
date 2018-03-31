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
        half_height=img_height//2
        half_width=img_width//2
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
        #下面对图片进行小波变换
        for j in range(half_width):
            #行上面的小波变换
            row_waved_img[:,j,:]=(img_array[:,2*j,:]+img_array[:,2*j+1,:])/2
            row_waved_img[:,j+half_width,:]=(img_array[:,2*j,:]-img_array[:,2*j+1,:])/2
        img_array=row_waved_img
        for k in range(half_height):
            #列上面的小波变换
            column_waved_img[k,:,:]=(img_array[2*k,:,:]+img_array[2*k+1,:,:])/2
            column_waved_img[k+half_height,:,:]=(img_array[2*k,:,:]-img_array[2*k+1,:,:])/2
        waved_img=column_waved_img
        return waved_img

    def multi_wave_img(img,depth):
        #多级小波变换函数
        wave_img_list=[]
        img=wave.storage2storage(img)
        wave_img_list.append(img)
        for depth_count in range(depth-1):
        #多级小波变换，存放在一个list中
            img_height=img.shape[0]
            img_width=img.shape[1]
            img_channel=img.shape[2]
            img=wave.storage2storage(img[:img_height//2,:img_width//2,:])
            wave_img_list.append(img)
        #最后一级小波变换的低频部分减去127
        last_low_height=wave_img_list[depth-1].shape[0]//2
        last_low_width=wave_img_list[depth-1].shape[1]//2
        wave_img_list[depth-1][:last_low_height,:last_low_width,:]=\
                wave_img_list[depth-1][:last_low_height,:last_low_width,:]-\
                np.full((last_low_height,last_low_width,3),127)
        for index in range(depth-1):
        # 变换后的图像拼接
            this_img_height=wave_img_list[depth-1-index].shape[0]
            this_img_width=wave_img_list[depth-1-index].shape[1]
            wave_img_list[depth-1-index-1][:this_img_height,:this_img_width,:]= \
                    wave_img_list[depth-1-index][:,:,:]
        return wave_img_list[0]
    def pic2pic(input_directory,output_directory):
        img=cv2.imread(input_directory)
        cv2.imwrite(output_directory,wave.storage2storage(img))
        if cv2.waitKey(0)== 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()

    def multi_wave_list(img,depth):
        # 多级小波变换函数
        wave_img_list=[]
        img=wave.storage2storage(img)
        wave_img_list.append(img)
        for depth_count in range(depth-1):
        # 多级小波变换，存放在一个list中
            img_height=img.shape[0]
            img_width=img.shape[1]
            img_channel=img.shape[2]
            img=wave.storage2storage(img[:img_height//2,:img_width//2,:])
            wave_img_list.append(img)
        '''
        for index in range(depth-1):
        # 变换后的图像拼接
            this_img_height=wave_img_list[depth-1-index].shape[0]
            this_img_width=wave_img_list[depth-1-index].shape[1]
            wave_img_list[depth-1-index-1][:this_img_height,:this_img_width,:]= \
                    wave_img_list[depth-1-index][:,:,:]
        '''
        return wave_img_list
    def wave_extract(img,extract_depth,area,depth):
        if extract_depth<=depth:
            # 找到所要提取的图片高和宽
            wave_img_list=wave.multi_wave_list(img,depth)
            extract_img_height=wave_img_list[extract_depth-1].shape[0]
            extract_img_width=wave_img_list[extract_depth-1].shape[1]
            if area==1:
                return \
                        wave_img_list[extract_depth-1][:extract_img_height//2,:extract_img_width//2,:]
            elif area==2:
                return \
                        wave_img_list[extract_depth-1][:extract_img_height//2,extract_img_width//2:,:]
            elif area==3:
                return \
                        wave_img_list[extract_depth-1][extract_img_height//2:,extract_img_width//2:,:]
            else:
                return\
                        wave_img_list[extract_depth-1][extract_img_height//2:,:extract_img_width//2,:]
            # return wave
        else:
            print("Illegal Parameter")
    def bri_wave_img_show(img,depth):
        wave_img_list=[]
        img=wave.storage2storage(img)
        wave_img_list.append(img)
        for depth_count in range(depth-1):
        #多级小波变换，存放在一个list中
            img_height=img.shape[0]
            img_width=img.shape[1]
            img_channel=img.shape[2]
            img=wave.storage2storage(img[:img_height//2,:img_width//2,:])
            wave_img_list.append(img)
        bri_img_height=wave_img_list[-1].shape[0]
        bri_img_width=wave_img_list[-1].shape[1]
        bri_img_channel=wave_img_list[-1].shape[2]
        wave_img_list[-1]=wave_img_list[-1]+np.full((bri_img_height,bri_img_width,bri_img_channel),128)
        wave_img_list[-1][:bri_img_height//2,:bri_img_width//2,:]=\
                wave_img_list[-1][:bri_img_height//2,:bri_img_width//2,:]-\
                np.full((bri_img_height//2,bri_img_width//2,bri_img_channel),128)
        for index in range(depth-1):
            bri_img_height=wave_img_list[index].shape[0]
            bri_img_width=wave_img_list[index].shape[1]
            bri_img_channel=wave_img_list[index].shape[2]
            wave_img_list[index]=wave_img_list[index]+np.full((bri_img_height,bri_img_width,bri_img_channel),128)
        for index in range(depth-1):
        # 变换后的图像拼接
            this_img_height=wave_img_list[depth-1-index].shape[0]
            this_img_width=wave_img_list[depth-1-index].shape[1]
            wave_img_list[depth-1-index-1][:this_img_height,:this_img_width,:]= \
                    wave_img_list[depth-1-index][:,:,:]
        cv2.imwrite("wave.jpg",wave_img_list[0])
        if cv2.waitKey(0)== 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()


        


#class light_

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
img=cv2.imread("1.jpg")
cv2.imwrite("2.jpg",wave.multi_wave_img(img,2))
if cv2.waitKey(0)==27:
    cv2.destroyWindow()
#测试wave_extract()
img=cv2.imread("1.jpg")
cv2.imwrite("2.jpg",wave.wave_extract(img,2,3,3))
'''
'''
#测试bri_wave_img_show()
img=cv2.imread("1.jpg")
wave.bri_wave_img_show(img,3)
'''
'''
#测试multi_wave_img()
img=cv2.imread("1.jpg")
cv2.imwrite("2.jpg",wave.multi_wave_img(img,3))
'''
