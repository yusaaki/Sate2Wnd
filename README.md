# Sate2Wnd
Converting satellite images to wind field using the pix2pix model, i.e., retrieving atmospheric motion vectors(AMVs) based on generative adversarial networks(GAN).
使用pix2pix模型将卫星图像转换为风场，即基于生成对抗网络（GAN）反演大气运动矢量（AMVs）。

# 使用方法
## 卫星图像
首先，需要准备相邻三个时次的红外和水汽两个通道的卫星图像，一共六张图像。卫星图像可从 http://weather.is.kochi-u.ac.jp/sat/ALL/ 下载。  
以反演2021年8月15日12:00 UTC风场为例，可打开 http://weather.is.kochi-u.ac.jp/sat/ALL/2021/08/15/ ，在其中找到这六个文件并下载：  
1. HMW821081511IR1.pgm.gz 
2. HMW821081512IR1.pgm.gz 
3. HMW821081513IR1.pgm.gz 
4. HMW821081511IR3.pgm.gz 
5. HMW821081512IR3.pgm.gz 
6. HMW821081513IR3.pgm.gz
其中IR1即红外通道，IR3即水汽通道。  
下载完成后，将文件路径填写到 main.py 中的 SATE_PATH。  
