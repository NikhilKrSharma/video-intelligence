# Image Detection
- Image Detection Module using the Ultralytics ```YoloV8``` module for image detection.
- The AI keeps track of the number of people in each frame of the video, along with different colours for each person.
- It also labels objects and people based on their classes in the ```classes.txt``` file.
- The Video can be paused to view a single frame by pressing 'p'.

## SortDetection.py
- Contains the backend driver algorithm for image detection.
- The function ```detectObject``` takes in the mode (Laptop Camera or Existing Video File) as a parameter.
- It utilises the Sort algorithm to identify and categorise people's faces. It also carries out age and gender detection.
- This file also gives the option to save the tracked video once complete.

## Runner.py
- Main code to run the algorithm using the ```tkinter``` library which creates a user interface.
- The mode can be selected (Video File or Camera), along with the video file name. It also allows the user to decide whether only people must be selected.
- The ```fetchVideos``` function enables all videos in the Media folder to automatically become available in the GUI, without having to modify the code.

## Main.py
- Allows terminal input of settings as opposed to the Graphic UI in Runner.py

## Media Folder
- Video files should be uploaded here (.mp4 format only)
- All video files automatically show up in the Runner.py GUI.