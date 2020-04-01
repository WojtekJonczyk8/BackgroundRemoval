import cv2 as cv
from matplotlib import pyplot as plt

# load images = original image size is 2820x5640
background = cv.imread('images/background1.jpg', 0)
img1 = cv.imread('images/input/img1.jpg', 0)
img2 = cv.imread('images/input/img2.jpg', 0)

# resize images
# background = cv.resize(background, (1410, 705)) 
# img1 = cv.resize(img1, (1410, 705)) 
# img2 = cv.resize(img2, (1410, 705))

# remove background
img1_sub = cv.subtract(background, img1) 
img2_sub = cv.subtract(background, img2)

# thresholding
ret, thresholded = cv.threshold(img1_sub, 35, 255, cv.THRESH_TOZERO)
# ret, thresholded = cv.threshold(img1_sub, 35, 255, cv.THRESH_BINARY)

# invert image
img_inv = cv.bitwise_not(thresholded)

# morphological transformations

def perform_morph_operation(img, operation, kernel):
    return cv.morphologyEx(img, operation, kernel)

# kernel_closing_cross = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
# kernel_closing_rect = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
kernel_closing_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, (13, 13))
# kernel_opening_cross = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
# kernel_opening_rect = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
kernel_opening_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, (45, 45))
# opening = cv.morphologyEx(img_inv, cv.MORPH_OPEN, kernel_opening_cross)
# opening2 = cv.morphologyEx(img_inv, cv.MORPH_OPEN, kernel_opening_rect)
# opening3 = cv.morphologyEx(img_inv, cv.MORPH_OPEN, kernel_opening_ellipse)
# closing = cv.morphologyEx(img_inv, cv.MORPH_CLOSE, kernel_closing_cross)
# closing2 = cv.morphologyEx(img_inv, cv.MORPH_CLOSE, kernel_closing_rect)
# closing3 = cv.morphologyEx(img_inv, cv.MORPH_CLOSE, kernel_closing_ellipse)

# first closing the image, then two openings
img_morph_temp1 = perform_morph_operation(img_inv, cv.MORPH_CLOSE, kernel_closing_ellipse)
img_morph_temp2 = perform_morph_operation(img_morph_temp1, cv.MORPH_CLOSE, kernel_closing_ellipse)
img_morph_temp3 = perform_morph_operation(img_morph_temp2, cv.MORPH_OPEN, kernel_opening_ellipse)
img_morph_temp4 = perform_morph_operation(img_morph_temp3, cv.MORPH_OPEN, kernel_opening_ellipse)
img_morph_temp5 = perform_morph_operation(img_morph_temp4, cv.MORPH_OPEN, kernel_opening_ellipse)
img_morph = img_morph_temp5


img_morph = cv.resize(img_morph, (1410, 705))
img_inv = cv.resize(img_inv, (1410, 705))
# image_enhanced = cv.equalizeHist(img_inv)

# Gaussian blur
blur = cv.GaussianBlur(img_inv,(9,9),0)

# show images
# cv.imshow("background", background)
# cv.imshow("image1", img1)
cv.imshow("image1 inverted", img_inv)
# cv.imshow("image1 enhanced", image_enhanced)
# cv.imshow("image2", img2)
# cv.imshow("image1_sub", img1_sub)
# cv.imshow("image2_sub", img2_sub)
# cv.imshow("thresh1", thresh1)
cv.imshow("gaussian", blur)
# cv.imshow("opening", opening)
cv.imshow("after_morph", img_morph)

cv.waitKey()

# plot images
# images = [opening, closing, dilation, erosion]
# titles = ["opening", "closing", "dilation", "erosion"]
# for i in range(4):
#     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()

# cv.imwrite("bigger_mask.jpg", img_opened_second) 
# cv.imwrite("original.jpg", img1) 