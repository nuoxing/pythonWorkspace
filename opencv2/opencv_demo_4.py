import cv2
"""
分离、合并通道
"""
img = cv2.imread('F:/1.png')
b, g, r = cv2.split(img)
cv2.imshow("Blue", r)
cv2.imshow("Red", g)
cv2.imshow("Green", b)
cv2.waitKey(0)
cv2.destroyAllWindows()