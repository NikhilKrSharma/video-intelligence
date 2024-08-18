import os
import cv2
import time
import cvzone
import numpy as np
import pandas as pd
from ultralytics import YOLO

import utils as u
from conf import *

# Set an environment variable
os.environ['VERBOSE'] = 'yes'

# Get an environment variable
verbose = True if os.environ.get('VERBOSE') in ['yes', 'y', 1] else False

if verbose:
    print('+ Important inputs/paths')
    print(
        f'{video_path=}\n{image_write_path=}\n{video_output_file_path=}\n{model_name=}\n{model_name_for_file_name=}\n{frames_per_second=}\n{skip_frame=}')

# MODEL INITIALIZATION AND LOAD THE MASK
global model
model = YOLO(model_name)
if mask_path:
    mask = cv2.imread(mask_path)

class_names = u.get_class_names(verbose=verbose)
video_properties = u.get_video_properties(video_input_path=video_path)

time_start = time.time()
# Get the frames per second (fps) of the video
fps = video_properties.get('FPS')
if verbose:
    print(f'Detected FPS: {fps}')

# Open the video file
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error: Unable to open video file {video_path}")
writer = u.create_video_writer(cap, output_file_name=video_output_file_path, frame_rate=frames_per_second)

df_data = []
frame_nth = int(fps / frames_per_second)
frame_index = 1
frame_count = 0
while cap.isOpened():

    # Set the frame position to the targeted frame
    if skip_frame:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()

    # Mirror the image
    # frame = cv2.flip(frame, 1)

    frame_count += 1

    # Check if we have reached the end of the video
    if not ret:
        print(f"Finished processing {frame_count} frames")
        break

    frame_original = np.copy(frame)

    if mask_path:
        target_region = cv2.bitwise_and(src1=frame, src2=mask)
        frame = target_region

    # Perform detection on the current frame
    results = u.yolo_model_pred(model=model, frame=frame, classes=[0], verbose=verbose)

    # Bounding boxes
    detection_count, frame_processed = u.detect_n_draw_bounding_boxes_new(
        results=results, frame=frame_original, draw_bb=True, verbose=verbose
    )

    df_data.append((frame_count, frame_index, detection_count))

    cv2.imshow('Frame', frame_processed)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    writer.write(frame_processed)

    # Move to the next nth frame
    if skip_frame:
        # frame_index += int(fps) * 1
        frame_index += frame_nth

cap.release()
writer.release()
cv2.destroyAllWindows()

time_end = time.time()
print(f'''- Time Total    : {round(time_end - time_start, 2)} sec''')

df = pd.DataFrame(data=df_data, columns=['frame_count', 'frame_index', 'detection_count'])
df.to_csv('../data/people-count.csv', index=False)
df.to_markdown()
