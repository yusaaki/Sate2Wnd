# Sate2Wnd
Converting satellite images to wind field using the pix2pix model, i.e., retrieving atmospheric motion vectors(AMVs) based on generative adversarial networks(GAN).  
使用pix2pix模型将卫星图像转换为风场，即基于生成对抗网络（GAN）反演大气运动矢量（AMVs）。

# 使用方法
## 卫星图像
首先，需要准备相邻三个时次的红外和水汽两个通道的卫星图像，一共六张图像。 作为示例，该仓库已提供某时次的这六张图像的.gz文件，直接下载即可。
其余时刻的卫星图像可从 http://weather.is.kochi-u.ac.jp/sat/ALL/ 下载。  
以反演2021年8月15日12:00 UTC风场为例，可打开 http://weather.is.kochi-u.ac.jp/sat/ALL/2021/08/15/ ，在其中找到这六个文件并下载：  
1. HMW821081511IR1.pgm.gz 
2. HMW821081512IR1.pgm.gz 
3. HMW821081513IR1.pgm.gz 
4. HMW821081511IR3.pgm.gz 
5. HMW821081512IR3.pgm.gz 
6. HMW821081513IR3.pgm.gz
  
其中，IR1为红外通道，IR3为水汽通道。  
下载完成后，将卫星图像路径填写到 main.py 中的 SATE_PATH。  

## 模型
模型已上传至百度云。  
链接: https://pan.baidu.com/s/1n_kRSMpepAKj76o9au8akw  提取码: j2zy  
下载完成后，将模型路径依次填写到 main.py 中的 MODEL_PATH。  

## 运行
### 脚本依赖下边这些库，需要先安装
库|参考版本
---|---
gzip| -
numpy|1.19.3
PIL|8.3.1
keras|2.6.0
matplotlib|3.4.2
cartopy|0.20.0

最后运行脚本即可，运行完成后将生成如下图片。
![运行结果](https://raw.githubusercontent.com/yusaaki/Sate2Wnd/main/Figure_1.jpg)
