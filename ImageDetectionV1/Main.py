from ObjectDetection import detectObject
import os

os.system('clear')
source = int(input("Camera (1), Preloaded Video (2): "))
people = True if input("People Only (Y/N): ").strip().lower() == 'y' else False
videoPath = f"{input('Enter Video File Name: ').strip()}.mp4" if source == 2 else None

detectObject(source, people, videoPath)