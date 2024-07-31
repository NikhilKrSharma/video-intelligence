# Image Detection
- Image Detection Module using the Ultralytics ```YoloV8n``` module for image detection.
- The AI keeps track of the number of people in each frame of the video, along with different colours for each person.
- It also labels objects and people based on their classes in the ```classes.txt``` file.
- The Video can be paused to view a single frame by pressing 'p'.

## SortDetection.py
- Contains the backend driver algorithm for image detection.
- The function ```detectObject``` takes in the mode (Laptop Camera or Existing Video File) as a parameter.
- It utilises the Sort algorithm to identify and categorise people's faces. It also carries out age and gender detection.
- It generates a CSV file displaying the mode age and gender of a person.
- Gives the option to save the tracked video once complete.
- Detects every 5th Frame to increase processing time.

## Sort.py
- Contains the backend driver algorithm for the SortTracker face tracking module.

## Runner.py
- Main code to run the algorithm using the ```tkinter``` library which creates a user interface.
- The mode can be selected (Video File or Camera), along with the video file name. It also allows the user to decide whether only people must be selected.
- The ```fetchVideos``` function enables all videos in the Media folder to automatically become available in the GUI, without having to modify the code.

## Main.py
- Allows terminal input of settings as opposed to the Graphic UI in Runner.py

## Media Folder
- Video files should be uploaded here (.mp4 format only)
- All video files automatically show up in the Runner.py GUI.

## Requirements.text
- Contains all the necessary imports and libraries.
- Execute this by running ```pip install -r requirements.txt```

## Dockerfile
- Creates a dockerfile of the ```main.py``` file.
- Build using: ```docker build -t imagedetection .```
- Execute using: ```docker run --rm -it imagedetection``` 