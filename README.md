# Sate2Wnd
Converting satellite images to wind field using the pix2pix model, i.e., retrieving atmospheric motion vectors(AMVs) based on generative adversarial networks(GAN)

# 使用方法
首先，需要准备连续三个时次的红外和水汽两个通道的卫星图像，共六张图像。
卫星图像可从 http://weather.is.kochi-u.ac.jp/sat/ALL/ 下载。
以反演2021年8月15日12:00 UTC风场为例，可打开 http://weather.is.kochi-u.ac.jp/sat/ALL/2021/08/15/ ，在其中找到这六个文件：
1. HMW821081511IR1.pgm.gz 
2. HMW821081512IR1.pgm.gz 
3. HMW821081513IR1.pgm.gz 
4. HMW821081511IR3.pgm.gz 
5. HMW821081512IR3.pgm.gz 
6. HMW821081513IR3.pgm.gz

