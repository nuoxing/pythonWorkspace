
import numpy as np
from PIL import Image

# 先打开传入的原始图片
img = Image.open("E:/0.jpg")
# 使用消除锯齿的方法resize图片
reIm = img.resize((28, 28), Image.ANTIALIAS)
# 变成灰度图，转换成矩阵
im_arr = np.array(reIm.convert("L"))
threshold = 50  # 对图像进行二值化处理，设置合理的阈值，可以过滤掉噪声，让他只有纯白色的点和纯黑色点
for i in range(28):
    for j in range(28):
        im_arr[i][j] = 255 - im_arr[i][j]
        if (im_arr[i][j] < threshold):
            im_arr[i][j] = 0
        else:
            im_arr[i][j] = 255
# 将图像矩阵拉成1行784列，并将值变成浮点型（像素要求的仕0-1的浮点型输入）
nm_arr = im_arr.reshape([1, 784])
nm_arr = nm_arr.astype(np.float32)
img_ready = np.multiply(nm_arr, 1.0 / 255.0)
cv2.imwrite('E:/01.jpg', img_ready)  # 预处理后图像保存位置
