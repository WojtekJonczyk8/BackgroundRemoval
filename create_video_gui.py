import tkinter as tk
from tkinter import filedialog as fd
import cv2 as cv
import os

folder_path = ''

root = tk.Tk()

def callback():
    global folder_path
    folder_path = fd.askdirectory()
    folder_name.set(folder_path) 
    video_saved_info.set("")

def correct_input(inp):
    video_saved_info.set("")
    if inp.isdigit():
        return True
    elif inp == '':
        return True
    else:
        return False
    
errmsg = 'Error!'
button = tk.Button(root, text = 'Set Folder', 
                command = callback).grid(row = 0, columnspan  = 1, sticky = 'nesw')

folder_name = tk.StringVar()
folder_name.set("Folder not set!")
label_folder_path = tk.Label(root, textvariable = folder_name).grid(row = 0, column = 1, columnspan = 3, sticky = 'nsw')

label_video_name = tk.Label(root, text = 'Video name').grid(row = 1)
video_name = tk.Entry(root)
video_name.insert(0, 'video')
video_name.grid(row = 1, column = 1)

print(video_name.get())

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
    video_saved_info.set("")
    vid_name = video_name.get() + ".avi"
    vid_width = int(frame_width.get())
    vid_height = int(frame_height.get())
    fram_rate = int(frame_rate.get())
    print("folder path: ", folder_path)

    images = [img for img in os.listdir(folder_path) if img.endswith(".JPG")]
    frame_large = cv.imread(os.path.join(folder_path, images[0]))
    frame = cv.resize(frame_large, (vid_width, vid_height))
    height, width, layers = frame.shape

    print(height, width, layers)

    video = cv.VideoWriter(vid_name, 0, fram_rate, (width, height))

    for idx, image in enumerate(images):
        print(idx)
        img_large = cv.imread(os.path.join(folder_path, image))
        img = cv.resize(img_large, (vid_width, vid_height))
        video.write(img)

    cv.destroyAllWindows()
    video.release()
    video_saved_info.set("Video succesfully saved!")

button2 = tk.Button(root, text='Create video', 
                    command=create_video).grid(row = 4, column = 2, columnspan = 2, sticky = "nesw")

tk.mainloop()
