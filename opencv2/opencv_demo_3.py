import cv2
"""
保存图片 imwrite函数 对于不同格式的图片 第三个参数对应不同的含义
"""
img = cv2.imread('F:/1.png')
cv2.imwrite('F:/test_imwrite.jpg', img, (cv2.IMWRITE_JPEG_QUALITY, 100))