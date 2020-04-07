# to run program please input into comand line:
# python test_removing_from_video.py --input 'D:/Wojtek/Projekt Jacek/Video/video_bw1.avi'
# python test_removing_from_video.py --input 'C:/Users/ejncwjc/Documents/Python/OpenCV/BackgroundRemoval/Video/video_bw1.avi'

from __future__ import print_function
import cv2 as cv
import numpy
import argparse
parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2(history=10, varThreshold=20, detectShadows = True)
else:
    backSub = cv.createBackgroundSubtractorKNN(history=10, dist2Threshold=20, detectShadows = True)
    cv.createBackgroundSubtractorKNN()
capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
ret, frame = capture.read()

if ret == False:
    print("Correct your path mate!")
    exit(0)

count_frames = 0
mask_video_name = 'foreground_mask.avi'
# mask_video_name = 'foreground_mask_inverted.avi'

# reset frame index to 0 to read firs frame again in the loop
capture.set(cv.CAP_PROP_POS_FRAMES, 0)
height, width, layers = frame.shape
print(height, width, layers)
video_loops_number = 1
video_loops_counter = 1
# video = cv.VideoWriter(mask_video_name, 0, 15, (width, height))
while True:
    ret, frame = capture.read()
    # Break if frame is empty and loops
    if frame is None and video_loops_counter == video_loops_number:
        #cv.destroyAllWindows()
        #video.release()
        break

    # if frame is empty but video_loops_number was not reached reset frame position and start again
    if frame is None:
        capture.set(cv.CAP_PROP_POS_FRAMES, 0)
        video_loops_counter += 1
        count_frames = 0
        continue

    print(count_frames)
    fgMask = backSub.apply(frame)
    
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    
    cv.createBackgroundSubtractorMOG2()
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)

    # morph operations
    # kernel_closing_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    kernel_opening_ellipse = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))

    # img_morph_closing = cv.morphologyEx(fgMask, cv.MORPH_CLOSE, kernel_closing_ellipse)
    img_morph_opening = cv.morphologyEx(fgMask, cv.MORPH_OPEN, kernel_opening_ellipse)

    # cv.imshow("morph", img_morph_closing)
    cv.imshow("morph", img_morph_opening)

    # print(numpy.amax(thresholded))

    fgMask_inv = cv.bitwise_not(fgMask)

    frame_to_save = cv.cvtColor(fgMask, cv.COLOR_GRAY2RGB) # not inverted
    # frame_to_save = cv.cvtColor(fgMask_inv, cv.COLOR_GRAY2RGB) # inverted

    height, width = fgMask_inv.shape
    # print(height, width)

    height1, width1, layers1 = frame.shape
    # print(height1, width1)

    name_mask = 'images/output/mask' + str(count_frames) + '.jpg'
    # cv.imwrite(name_mask, fgMask)

    # video.write(frame_to_save)
    
    keyboard = cv.waitKey(10)
    count_frames += 1
    if keyboard == 'q' or keyboard == 27:
        # cv.destroyAllWindows()
        # video.release()
        break