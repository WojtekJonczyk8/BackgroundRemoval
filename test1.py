import cv2

img1 = cv2.imread('images/img1.jpg', -1)
img1 = cv2.resize(img1, (960, 540)) 
cv2.imshow("image", img1, )
cv2.waitKey()