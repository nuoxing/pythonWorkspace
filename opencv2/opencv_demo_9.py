import cv2
import numpy as np

"""
车牌识别学习例子
"""

img = cv2.imread('F:/1.png')
#灰度化
image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.namedWindow("Image2")
cv2.imshow("Image2",image)
cv2.waitKey(0)
#高斯去噪
blurred = cv2.GaussianBlur(image, (9, 9),0)
cv2.namedWindow("Image3")
cv2.imshow("Image3",blurred)
cv2.waitKey(0)

#提取图像的梯度 图像边缘检测。提取特征
gradX = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=1, dy=0)
#gradY = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=0, dy=1)

#gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradX)
cv2.namedWindow("Image4")
cv2.imshow("Image4",gradient)
cv2.waitKey(0)
#去噪并二值化 就是将图像上的像素点的灰度值设置为0或255,图像呈现出明显的只有黑和白。
blurred = cv2.GaussianBlur(gradient, (9, 9),0)
(_, thresh) = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.namedWindow("Image5")
cv2.imshow("Image5",thresh)
cv2.waitKey(0)

#图像形态学（牛逼吧、唬人的） 闭操作 闭操作可以将目标区域连成一个整体，便于后续轮廓的提取。
"""
通常情况下，我们可以使用函数getStructuringElement()来制作操作内核。

Mat getStructuringElement(int shape, Size esize, Point anchor=Point(-1,-1));
参数：

shape:内核形状，主要有MORPH_RECT,MORPH_CROSS和MORPH_ELLIPSE,分别为矩形、椭圆形和交叉形，对应的值分别为0，1，2
 
enum { MORPH_RECT=0, MORPH_CROSS=1, MORPH_ELLIPSE=2 };
 
esize:内核大小。

anchor:内核锚点，默认为内核中心点。

"""
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,3))


#细节刻画 膨胀腐蚀
#通过膨胀连接相近的图像区域，通过腐蚀去除孤立细小的色块。
closed = cv2.dilate(thresh, kernel, iterations=2)#膨胀 iterations指的是次数，省略是默认为1
closed = cv2.erode(closed, kernel, iterations=4)#腐蚀
closed = cv2.dilate(closed, kernel, iterations=2)#




cv2.namedWindow("Image7")
cv2.imshow("Image7",closed)
cv2.waitKey(0)

#找出区域的轮廓
 # 这里opencv3返回的是三个参数
binary,cnts, hierarchy= cv2.findContours(closed.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


#画轮廓

draw_img = cv2.drawContours(img.copy(), cnts, -1, (0, 0, 255), 3)
cv2.namedWindow("Image8")
cv2.imshow("Image8",draw_img)
cv2.waitKey(0)


#提取车牌区域
for item in cnts:
    rect = cv2.boundingRect(item)
    x = rect[0]
    y = rect[1]
    weight = rect[2]
    height = rect[3]
    if weight > (height * 2):
        image = img[y:y + height, x:x + weight]
        cv2.namedWindow("Image9")
        cv2.imshow("Image9", image)
        cv2.waitKey(0)


#释放窗口
cv2.destroyAllWindows()