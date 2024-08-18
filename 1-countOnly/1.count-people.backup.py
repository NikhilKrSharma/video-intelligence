import os
import cv2
import time
import cvzone
from ultralytics import YOLO 

import utils as u


# Set an environment variable
os.environ['VERBOSE'] = 'yes'

# Get an environment variable
verbose = True if os.environ.get('VERBOSE') in ['yes', 'y', 1] else False


# CONFIGURATIONS
video_path               = '../data/processed_8910_C1_5min.mp4'
image_write_path         = '../data/images'
output_file_name         = '../data/processed_8910_C1_5min_output.mp4'
model_name               = '../yolo-models/yolov8n.pt'
model_name_for_file_name = model_name.split('/')[-1].split('.')[0]
if verbose:
    print('+ Important inputs/paths')
    print(f'{video_path=}\n{image_write_path=}\n{output_file_name=}\n{model_name=}\n{model_name_for_file_name=}')


# MODEL INITIALIZATION
global model
model = YOLO(model_name)

class_names = u.get_class_names(verbose=verbose)
video_properties = u.get_video_properties(video_input_path=video_path)


time_start = time.time()
# Get the frames per second (fps) of the video
fps = video_properties.get('FPS')
if verbose: print(f'Detected FPS: {fps}')


# Open the video file
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error: Unable to open video file {video_path}")

# List to store frames
frame_index = 0
frame_count = 0
while cap.isOpened():

    # Set the frame position to the targeted frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()
    frame_count +=1

    # Check if we have reached the end of the video
    if not ret:
        print(f"Finished processing {frame_count} frames")
        break

    frame_original = frame.copy(deep=True)

    # Process the results

    # Perform detection on the current frame
    results = u.yolo_model_pred(frame, classes=[0])
    person_count = 0

    if len(results) > 1:
        for result in results:
            person_count = len(results)
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = [int(x) for x in [x1, y1, x2, y2]]
                xyxy = (x1, y1, x2, y2)

                w, h = x2 - x1, y2 - y1

                conf = round(float(box.conf[0]), 2)
                detected_class_index = int(box.cls[0])
                detected_class_name = class_names.get(detected_class_index, 'N/A').title()

                # Draw rectangle
                cvzone.cornerRect(img=frame, bbox=(x1, y1, w, h), rt=1, colorR=(255, 0, 255), t=2, colorC=(0, 255, 0), l=10)

                # Put ID, class and conf on the bounding box
                cvzone.putTextRect(img=frame, text=f'{detected_class_name} | {conf}', pos=(max(x1, 0), max(y1, 35)), scale=0.7, thickness=1, offset=3)


    # Optionally display the frame (remove this in the final script if not needed)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


    image_write_path1 = f'{image_write_path}/{frame_index}.jpeg'
    image_write_path2 = f'{image_write_path}/{frame_index}-{model_name_for_file_name}.jpeg'

    cv2.imwrite(image_write_path1, frame_original)
    cv2.imwrite(image_write_path2, frame)

    # Move to the next second
    frame_index += int(fps) * 10

cap.release()
cv2.destroyAllWindows()




time_end = time.time()
print(f'''- Time Total    : {round(time_end - time_start, 2)} sec''')