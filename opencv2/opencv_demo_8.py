import cv2
import numpy as np

"""
图像阀值
"""

"""
Otsu's二值化
我们前面说到，cv2.threshold函数是有两个返回值的，前面一直用的第二个返回值，也就是阈值处理后的图像，
那么第一个返回值（得到图像的阈值）将会在这里用到。
前面对于阈值的处理上，我们选择的阈值都是127，那么实际情况下，怎么去选择这个127呢？有的图像可能阈值不是127得到的效果更好。
那么这里我们需要算法自己去寻找到一个阈值，而Otsu’s就可以自己找到一个认为最好的阈值。
并且Otsu’s非常适合于图像灰度直方图具有双峰的情况，他会在双峰之间找到一个值作为阈值，对于非双峰图像，
可能并不是很好用。那么经过Otsu’s得到的那个阈值就是函数cv2.threshold的第一个参数了。
因为Otsu’s方法会产生一个阈值，那么函数cv2.threshold的的第二个参数（设置阈值）就是0了，
并且在cv2.threshold的方法参数中还得加上语句cv2.THRESH_OTSU。
"""

img = cv2.imread('F:/2.jpg', 0)

ret1, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# (5,5)为高斯核的大小，0为标准差
blur = cv2.GaussianBlur(img, (5, 5), 0)

# 阀值一定要设为0
ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

images = [img, 0, th1,
          img, 0, th2,
          img, 0, th3]
titles = ['original noisy image', 'histogram', 'global thresholding(v=127)',
          'original noisy image', 'histogram', "otsu's thresholding",
          'gaussian giltered image', 'histogram', "otus's thresholding"]
# 这里使用了pyplot中画直方图的方法，plt.hist要注意的是他的参数是一维数组
# 所以这里使用了（numpy）ravel方法，将多维数组转换成一维，也可以使用flatten方法

cv2.imshow("1", th1)
cv2.imshow("2", th2)
cv2.imshow("3", th3)
cv2.waitKey(0)

#释放窗口
cv2.destroyAllWindows()