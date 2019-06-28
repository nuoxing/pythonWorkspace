import cv2
import numpy as np

"""
图像阀值
"""


"""
自适应阀值
根据图像上的每一个小区域计算与其对应的阀值。因此在同一幅图像上的不同区域采用的是不同的阀值，
从而使我们能在亮度不同的情况下得到更好的结果。
这种方法需要我们指定三个参数，返回值只有一个。
Adaptive Method 指定计算阀值的方法
-cv2.ADAPTIVE_THRESH_MEAN_C:阀值取自相邻区域的平均值
-cv2.ADAPTIVE_THRESH_GAUSSIAN_C:阀值取自相邻区域的加权和，权重为一个高斯窗口
Block Size 邻域大小（用来计算阀值的区域大小）
C这就是一个常数，阀值就等于的平均值或者加权平均值减去这个常数
"""

img = cv2.imread('F:/2.jpg',0)
#中值滤波
img = cv2.medianBlur(img,5)

ret , th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
# 11为block size，2为C值
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY,11,2 )
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,11,2)

titles = ['original image' , 'global thresholding (v=127)','Adaptive mean thresholding',
          'adaptive gaussian thresholding']
images = [img,th1,th2,th3]

for i in range(4):
    cv2.imshow(titles[i], images[i])
    cv2.waitKey(0)



#释放窗口
cv2.destroyAllWindows()
