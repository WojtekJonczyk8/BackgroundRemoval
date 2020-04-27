import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import cv2 as cv
import os

folder_path = ''

root = tk.Tk()

def callback():
    reset_all_labels()
    global folder_path
    folder_path = fd.askdirectory()
    if not folder_path:
        folder_name.set("Folder not set!")
    else:
        folder_name.set(folder_path)

def correct_input(inp):
    reset_all_labels()
    if inp.isdigit():
        return True
    elif inp == '':
        return True
    else:
        return False
    
def update_video_progress(text):
    video_saved_info.set(text)
    root.update_idletasks()

def reset_all_labels():
    update_video_progress("")
    progress_value.set(0)
    root.update_idletasks()

errmsg = 'Error!'
button = tk.Button(root, text = 'Set Folder', 
                command = callback).grid(row = 0, columnspan  = 1, sticky = 'nesw')

folder_name = tk.StringVar()
folder_name.set("Folder not set!")
label_folder_path = tk.Label(root, textvariable = folder_name).grid(row = 0, column = 1, columnspan = 3)

label_video_name = tk.Label(root, text = 'Video name').grid(row = 1)
video_name = tk.Entry(root)
video_name.insert(0, 'video')
video_name.grid(row = 1, column = 1)

label_width = tk.Label(root, text = 'Video width').grid(row = 2, column = 0)
frame_width = tk.Entry(root)
reg = root.register(correct_input)
frame_width.insert(0, '1410')
frame_width.config(validate = "key", validatecommand = (reg, '%P'))
frame_width.grid(row = 2, column = 1)

label_height = tk.Label(root, text = 'Video height').grid(row = 2, column = 2)
frame_height = tk.Entry(root)
frame_height.insert(0, '705')
frame_height.config(validate = "key", validatecommand = (reg, '%P'))
frame_height.grid(row = 2, column = 3)

label_rate = tk.Label(root, text = 'Frame rate').grid(row = 3, column = 0)
frame_rate = tk.Entry(root)
frame_rate.insert(0, '5')
frame_rate.config(validate = "key", validatecommand = (reg, '%P'))
frame_rate.grid(row = 3, column = 1)

video_saved_info = tk.StringVar()
video_saved_info.set("")
label_video_saved = tk.Label(root, textvariable = video_saved_info).grid(row = 4, column = 0, columnspan = 2)

def create_video():
    global folder_path
    vid_name = video_name.get() + ".avi"
    vid_width = int(frame_width.get())
    vid_height = int(frame_height.get())
    fram_rate = int(frame_rate.get())

    images = [img for img in os.listdir(folder_path) if (img.endswith(".JPG") or img.endswith(".jpg"))]

    if images:
        frame_large = cv.imread(os.path.join(folder_path, images[0]))
        frame = cv.resize(frame_large, (vid_width, vid_height))
        height, width, layers = frame.shape

        video = cv.VideoWriter(vid_name, 0, fram_rate, (width, height))
        frame_number = len(images)
        reset_all_labels()

        for idx, image in enumerate(images):
            info = str(idx) + " out of " + str(frame_number) + " saved!"
            progress_val = idx * 100 / frame_number
            update_video_progress(info)
            progress_value.set(progress_val)
            root.update_idletasks()
            img_large = cv.imread(os.path.join(folder_path, image))
            img = cv.resize(img_large, (vid_width, vid_height))
            video.write(img)
            keyboard = cv.waitKey(20)
            cv.imshow("image", img)
            if keyboard == ord('q') or keyboard == 27:
                break

        progress_val = 100
        progress_value.set(progress_val)
        update_video_progress("Video succesfully saved!")
        cv.destroyAllWindows()
        video.release()
        
        root.update_idletasks()
    else:
        update_video_progress("No images found!")

button2 = tk.Button(root, text='Create video', 
                    command=create_video).grid(row = 4, column = 2, columnspan = 2, sticky = "nesw")

progress_value = tk.IntVar()
progress = ttk.Progressbar(root, orient = 'horizontal', 
              length = 100, variable = progress_value, mode = 'determinate').grid(row = 5, column = 0, columnspan = 4, sticky = "nesw")

tk.mainloop()
