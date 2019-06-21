import cv2
import numpy as np

"""
读图像用cv2.imread()，可以按照不同模式读取，一般最常用到的是读取单通道灰度图，或者直接默认读取多通道。
"""
img = cv2.imread("F:/a.jpg")
#创建窗口并显示图像
cv2.namedWindow("Image")
cv2.imshow("Image",img)
cv2.waitKey(0)

# 直接读取单通道
img2 = cv2.imread('F:/a.jpg', cv2.IMREAD_GRAYSCALE)
cv2.namedWindow("Image2")
cv2.imshow("Image2",img2)
cv2.waitKey(0)


#高斯去噪
img3 = cv2.imread('F:/a.jpg', cv2.IMREAD_GRAYSCALE)
blurred = cv2.GaussianBlur(img3, (9, 9),0)
cv2.namedWindow("Image3")
cv2.imshow("Image3",img3)
cv2.waitKey(0)

#提取图像的梯度
gradX = cv2.Sobel(img3, ddepth=cv2.CV_32F, dx=1, dy=0)
gradY = cv2.Sobel(img3, ddepth=cv2.CV_32F, dx=0, dy=1)

gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)
cv2.namedWindow("Image4")
cv2.imshow("Image4",gradient)
cv2.waitKey(0)
#去噪并二值化
blurred = cv2.GaussianBlur(gradient, (9, 9),0)
(_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
cv2.namedWindow("Image5")
cv2.imshow("Image5",thresh)
cv2.waitKey(0)

#图像形态学（牛逼吧、唬人的）
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
cv2.namedWindow("Image6")
cv2.imshow("Image6",closed)
cv2.waitKey(0)

#细节刻画
closed = cv2.erode(closed, None, iterations=4)
closed = cv2.dilate(closed, None, iterations=4)
cv2.namedWindow("Image7")
cv2.imshow("Image7",closed)
cv2.waitKey(0)

#找出区域的轮廓
 # 这里opencv3返回的是三个参数
cnts, hierarchy= cv2.findContours(closed.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


#画轮廓
c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
box = np.int0(cv2.boxPoints(rect))
# draw a bounding box arounded the detected barcode and display the image
draw_img = cv2.drawContours(img3.copy(), [box], -1, (0, 0, 255), 3)
cv2.namedWindow("Image8")
cv2.imshow("Image8",draw_img)
cv2.waitKey(0)


#释放窗口
cv2.destroyAllWindows()