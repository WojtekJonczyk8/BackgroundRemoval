# to run program please input into comand line:
# python test_removing_from_video.py --input 'D:/Wojtek/Projekt Jacek/Proba1BW/video.avi'
# python test_removing_from_video.py --input 'C:/Users/ejncwjc/Documents/Python/OpenCV/BackgroundRemoval/Video/video_bw1.avi'

from __future__ import print_function
import cv2 as cv
import argparse
parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2(history=5, varThreshold=20, detectShadows = True)
else:
    backSub = cv.createBackgroundSubtractorKNN(history=5, dist2Threshold=20, detectShadows = True)
    cv.createBackgroundSubtractorKNN()
capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
if not capture.isOpened:
    print('Unable to open: ' + args.input)
    exit(0)

count_frames = 0
mask_video_name = 'foreground_mask.avi'
# mask_video_name = 'foreground_mask_inverted.avi'
ret, frame = capture.read()
# reset frame index to 0 to read firs frame again in the loop
capture.set(cv.CAP_PROP_POS_FRAMES, 0)
height, width, layers = frame.shape
print(height, width, layers)
video = cv.VideoWriter(mask_video_name, 0, 15, (width, height))
while True:
    ret, frame = capture.read()
    if frame is None:
        #cv.destroyAllWindows()
        #video.release()
        break
    print(count_frames)
    fgMask = backSub.apply(frame)
    
    
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    
    cv.createBackgroundSubtractorMOG2()
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)

    fgMask_inv = cv.bitwise_not(fgMask)

    frame_to_save = cv.cvtColor(fgMask, cv.COLOR_GRAY2RGB) # not inverted
    # frame_to_save = cv.cvtColor(fgMask_inv, cv.COLOR_GRAY2RGB) # inverted

    height, width = fgMask_inv.shape
    # print(height, width)

    height1, width1, layers1 = frame.shape
    # print(height1, width1)

    name_mask = 'images/output/mask' + str(count_frames) + '.jpg'
    # cv.imwrite(name_mask, fgMask)

    video.write(frame_to_save)
    
    keyboard = cv.waitKey(100)
    count_frames += 1
    if keyboard == 'q' or keyboard == 27:
        cv.destroyAllWindows()
        video.release()
        break