import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import cv2 as cv
import os

video_name = ''

root = tk.Tk()

def callback():
    reset_all_labels()
    global video_name
    video_name = fd.askopenfile()
    if not video_name:
        file_string_var.set('Video not set!')
    else:
        file_string_var.set(video_name.name)

def correct_input(inp):
    reset_all_labels()
    if inp.isdigit():
        return True
    elif inp == '':
        return True
    else:
        return False

def update_video_progress(text):
    masks_saved_info.set(text)
    root.update_idletasks()

def reset_all_labels():
    update_video_progress("")
    progress_value.set(0)
    root.update_idletasks()

def calculate_masks():
    global video_name
    backSub = cv.createBackgroundSubtractorMOG2(history=10, varThreshold=20, detectShadows = False)
    if video_name:
        capture = cv.VideoCapture(cv.samples.findFileOrKeep(video_name.name))
        frame_total = int(capture.get(cv.CAP_PROP_FRAME_COUNT))
        ret, frame = capture.read()

        kernel_dim = int(kernel_size.get())
        time_between_masks = int(time_period.get())
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (kernel_dim, kernel_dim))
        count_frames = 1
        mask_default_raw = cv.imread('images/mask_default.jpg', -1)

        # reset frame index to 0 to read firs frame again in the loop
        capture.set(cv.CAP_PROP_POS_FRAMES, 0)
        height, width, layers = frame.shape
        mask_default = cv.resize(mask_default_raw, (height, width))
        while True:
            ret, frame = capture.read()
            # Break if frame is empty and loops
            if frame is None:
                cv.destroyAllWindows()
                progress_val = 100
                progress_value.set(progress_val)
                update_video_progress("Mask generated!")
                break

            info = str(count_frames) + " out of " + str(frame_total) + " saved!"
            progress_val = count_frames * 100 / frame_total
            update_video_progress(info)
            progress_value.set(progress_val)
            root.update_idletasks()

            fgMask = backSub.apply(frame)
            
            cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
            cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
            
            cv.createBackgroundSubtractorMOG2()

            mask_to_save = cv.cvtColor(fgMask, cv.COLOR_GRAY2RGB) # not inverted

            # apply additional mask to remove places where people are not visible at all
            frame_mask = cv.bitwise_and(mask_to_save, mask_default)
            ret_mask, mask_binary = cv.threshold(frame_mask, 100, 255, cv.THRESH_BINARY)

            if blurred_output.get():
                blur = cv.GaussianBlur(mask_binary, (kernel_dim, kernel_dim), 0)
                mask_binary = blur

            if median_output.get():
                median = cv.medianBlur(mask_binary, kernel_dim)
                mask_binary = median
            
            # morphological operations
            if closed_output.get():
                img_morph_closing = cv.morphologyEx(mask_binary, cv.MORPH_CLOSE, kernel)
                mask_binary = img_morph_closing

            if open_output.get():
                img_morph_opening = cv.morphologyEx(mask_binary, cv.MORPH_OPEN, kernel)
                mask_binary = img_morph_opening

            if dilated_output.get():
                img_morph_dilation = cv.morphologyEx(mask_binary, cv.MORPH_DILATE, kernel)
                mask_binary = img_morph_dilation
            
            if eroded_output.get():
                img_morph_erosion = cv.morphologyEx(mask_binary, cv.MORPH_ERODE, kernel)
                mask_binary = img_morph_erosion

            if inverted_output.get():
                mask_inverted = cv.bitwise_not(mask_binary)
                mask_binary = mask_inverted

            cv.imshow('mask', mask_binary)

            name_mask = 'images/output/mask' + str(count_frames) + '.jpg'
            cv.imwrite(name_mask, mask_binary)
            
            keyboard = cv.waitKey(time_between_masks)

            # pause program
            if keyboard == ord('p'):
                current_text = masks_saved_info.get()
                update_video_progress("Video paused!")
                keyboard = cv.waitKey()
                update_video_progress(current_text)

            if keyboard == ord('q') or keyboard == 27:
                cv.destroyAllWindows()
                progress_value.set(0)
                update_video_progress("Video stopped!")
                break

            count_frames += 1
    else:
        update_video_progress("No images found!")

errmsg = 'Error!'
button = tk.Button(root, text = 'Set Video', 
                command = callback).grid(row = 0, columnspan  = 1, sticky = 'nesw')

file_string_var = tk.StringVar()
file_string_var.set('File not set!')
file_label = tk.Label(root, textvariable = file_string_var).grid(row = 0, column = 1, columnspan = 3)

blurred_output = tk.IntVar()
blurred_checkbox = tk.Checkbutton(root, text = 'blur', variable = blurred_output).grid(row = 1, sticky = 'w')

median_output = tk.IntVar()
median_checkbox = tk.Checkbutton(root, text = 'median', variable = median_output).grid(row = 1, column = 1, sticky = 'w')

kernel_label = tk.Label(root, text = 'Kernel size').grid(row = 1, column = 2)
kernel_size = tk.Entry(root)
reg = root.register(correct_input)
kernel_size.insert(0, '9')
kernel_size.config(validate = "key", validatecommand = (reg, '%P'))
kernel_size.grid(row = 1, column = 3, sticky = 'w')

closed_output = tk.IntVar()
closing_checkbox = tk.Checkbutton(root, text = 'closing', variable = closed_output).grid(row = 2, column = 0, sticky = 'w')

open_output = tk.IntVar()
opening_checkbox = tk.Checkbutton(root, text = 'opening', variable = open_output).grid(row = 2, column = 1, sticky = 'w')

dilated_output = tk.IntVar()
dilation_checkbox = tk.Checkbutton(root, text = 'dilation', variable = dilated_output).grid(row = 2, column = 2, sticky = 'w')

eroded_output = tk.IntVar()
erosion_checkbox = tk.Checkbutton(root, text = 'erosion', variable = eroded_output).grid(row = 2, column = 3, sticky = 'w')

inverted_output = tk.IntVar()
erosion_checkbox = tk.Checkbutton(root, text = 'inverted', variable = inverted_output).grid(row = 3, column = 0, sticky = 'w')

time_period_label = tk.Label(root, text = 'Time period').grid(row = 4, column = 2)
time_period = tk.Entry(root)
time_period.insert(0, '1000')
time_period.config(validate = "key", validatecommand = (reg, '%P'))
time_period.grid(row = 4, column = 3, sticky = 'w')

masks_saved_info = tk.StringVar()
masks_saved_info.set("")
label_masks_saved = tk.Label(root, textvariable = masks_saved_info).grid(row = 5, column = 0, columnspan = 2)

button2 = tk.Button(root, text = 'Generate masks!', 
                    command = calculate_masks).grid(row = 5, column = 2, columnspan = 2, sticky = 'nesw')

progress_value = tk.IntVar()
progress = ttk.Progressbar(root, orient = 'horizontal', 
                           length = 100, variable = progress_value, mode = 'determinate').grid(row = 6, column = 0, columnspan = 4, sticky = "nesw")

tk.mainloop()

