# -*- coding: utf-8 -*-



""" 路径 """
### 模型文件位置 ###
MODEL_PATH = "model_0500000.h5"

### 卫星图像位置 ###
# 共6张图。按以下顺序排列：t-1h、t、t+1h时刻的红外通道图像，t-1h、t、t+1h时刻的水汽通道图像。
# 卫星图像可从 http://weather.is.kochi-u.ac.jp/sat/ALL/ 下载
SATE_PATH = [
"HMW821072311IR1.pgm.gz", 
"HMW821072311IR1.pgm.gz", 
"HMW821072312IR1.pgm.gz", 
"HMW821072312IR3.pgm.gz", 
"HMW821072313IR3.pgm.gz", 
"HMW821072313IR3.pgm.gz"]



""" 常量 """
### 输入卫星图像的宽度和高度 ###
SOURCE_WIDTH   = 512
SOURCE_HEIGHT  = 512

### 输入卫星图像的区域范围 ###
EXTENT = [70, 210, 70, -70]

### 输出风场的宽度和高度 ###
TARGET_WIDTH   = 64
TARGET_HEIGHT  = 64

### 再分析资料中风速的极大极小值，用于反归一化数据 ###
U850_MAX, U850_MIN = 48.92, -41.12
V850_MAX, V850_MIN = 45.33, -45.33
U200_MAX, U200_MIN = 109.11, -58.98
V200_MAX, V200_MIN = 73.70, -91.11



""" 函数 """
import gzip
import numpy as np
from PIL import Image

def read_gz_file(gz_file):
    ''' 读取单个.gz文件中卫星图像 '''
    with gzip.open(gz_file, 'rb') as f:
        img = Image.open(f)
        img = img.resize((SOURCE_WIDTH, SOURCE_HEIGHT)) # 缩放以适应模型输入
        img = np.array(img)

    img = img / 255
    return img

def read_gz_files(gz_files):
    ''' 读取多个.gz文件中卫星图像，并拼成一个多通道数组 '''
    img = []
    for gz_file in gz_files:
        img.append(read_gz_file(gz_file))

    # 将通道置于最后维度
    img = np.transpose(img, (1, 2, 0))
    return img

def inverse_rescale(x, x_max, x_min, a=0, b=1):
    ''' 反归一化 '''
    x = (x-a)*(x_max-x_min)/(b-a) + x_min
    return x



""" 主程序 """
if __name__ == '__main__':

    # 读取卫星图像
    img = read_gz_files(SATE_PATH) # img.shape = (512, 512, 6)
    img = img[None,:]              # img.shape = (1, 512, 512, 6)


    # 加载模型
    from keras.models import load_model
    model = load_model(MODEL_PATH)


    # 使用模型反演风场
    wind = model.predict(img)

    # 反归一化
    u850_p = inverse_rescale(wind[0,:,:,0], U850_MAX, U850_MIN)
    v850_p = inverse_rescale(wind[0,:,:,1], V850_MAX, V850_MIN)
    u200_p = inverse_rescale(wind[0,:,:,2], U200_MAX, U200_MIN)
    v200_p = inverse_rescale(wind[0,:,:,3], V200_MAX, V200_MIN)


    ### 绘图 ###
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeat

    fig = plt.figure(figsize=(8, 8))

    ### 画卫星图像 ###
    LON = np.linspace(EXTENT[0], EXTENT[1], SOURCE_WIDTH, endpoint=True)
    LAT = np.linspace(EXTENT[2], EXTENT[3], SOURCE_HEIGHT, endpoint=True)
    X, Y = np.meshgrid(LON, LAT)

    # 红外通道
    ax = fig.add_subplot(2, 2, 1, projection=ccrs.PlateCarree(central_longitude=180))
    ax.set_extent(EXTENT, crs=ccrs.PlateCarree())
    ax.add_feature(cfeat.LAND.with_scale("110m"), edgecolor="gold", facecolor="none", linewidths=0.6, zorder=2)
    ax.pcolormesh(X, Y, img[0,:,:,1], cmap='Greys_r', shading='auto', transform=ccrs.PlateCarree())
    ax.set_title("Input Infrared Image")

    # 水汽通道
    ax = fig.add_subplot(2, 2, 2, projection=ccrs.PlateCarree(central_longitude=180))
    ax.set_extent(EXTENT, crs=ccrs.PlateCarree())
    ax.add_feature(cfeat.LAND.with_scale("110m"), edgecolor="gold", facecolor="none", linewidths=0.6, zorder=2)
    ax.pcolormesh(X, Y, img[0,:,:,4], cmap='Greys_r', shading='auto', transform=ccrs.PlateCarree())
    ax.set_title("Input Water Vapor Image")

    ### 画反演风场 ###
    LON = np.linspace(EXTENT[0], EXTENT[1], TARGET_WIDTH, endpoint=True)
    LAT = np.linspace(EXTENT[2], EXTENT[3], TARGET_HEIGHT, endpoint=True)
    X, Y = np.meshgrid(LON, LAT)

    # 850 hPa
    ax = fig.add_subplot(2, 2, 3, projection=ccrs.PlateCarree(central_longitude=180))
    ax.set_extent(EXTENT, crs=ccrs.PlateCarree())
    ax.add_feature(cfeat.LAND.with_scale("110m"), edgecolor="k", facecolor="none", linewidths=0.6, zorder=2)
    ax.streamplot(X-180, Y, u850_p, v850_p, density=2.2, linewidth=1, arrowsize=0.8, color=(u850_p**2 + v850_p**2)**0.5, cmap='jet', transform=ccrs.PlateCarree(central_longitude=180))
    ax.set_title("Output 850-hPa Winds")

    # 200 hPa
    ax = fig.add_subplot(2, 2, 4, projection=ccrs.PlateCarree(central_longitude=180))
    ax.set_extent(EXTENT, crs=ccrs.PlateCarree())
    ax.add_feature(cfeat.LAND.with_scale("110m"), edgecolor="k", facecolor="none", linewidths=0.6, zorder=2)
    ax.streamplot(X-180, Y, u200_p, v200_p, density=2.2, linewidth=1, arrowsize=0.8, color=(u200_p**2 + v200_p**2)**0.5, cmap='jet', transform=ccrs.PlateCarree(central_longitude=180))
    ax.set_title("Output 200-hPa Winds")

    plt.tight_layout()
    plt.show()

import code
code.interact(banner = "", local = locals())