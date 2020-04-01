import cv2 as cv
import os

image_folder = 'D:/Wojtek/Projekt Jacek/Proba1BW'
video_name = 'video.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".JPG")]
print(len(images))
frame_large = cv.imread(os.path.join(image_folder, images[0]))
frame = cv.resize(frame_large, (1410, 705))
height, width, layers = frame.shape

video = cv.VideoWriter(video_name, 0, 1, (width,height))

for idx, image in enumerate(images):
    print(idx)
    img_large = cv.imread(os.path.join(image_folder, image))
    img = cv.resize(img_large, (1410, 705))
    video.write(img)

cv.destroyAllWindows()
video.release()