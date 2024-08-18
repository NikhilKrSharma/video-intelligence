# https://youtu.be/WgPbbWmnXJ8

import os
import sys
import cv2
import time
import yaml
import cvzone
import numpy as np
from box import Box
from ultralytics import YOLO
from sort import *



def create_video_writer(video_cap, output_file_name):

    frame_width  = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate   = int(video_cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    writer = cv2.VideoWriter(
        filename=output_file_name,
        fourcc=fourcc,
        fps=frame_rate,
        frameSize=(frame_width, frame_height)
    )

    return writer


with open('./config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    
# Convert to Box
config = Box(config)


# Load YOLO model and mask
model = YOLO(model=config.model.nano_model_path, verbose=False)
mask = cv2.imread(config.input.mask_file_path)


# READ: Load video file
if config.input.mode=='cam':
    cap = cv2.VideoCapture(0)
else:
    video_file_path = config.input.video_file_path
    cap = cv2.VideoCapture(config.input.video_file_path)
    # cap.set(3, config.input.video_dim_x)
    # cap.set(4, config.input.video_dim_y)

frame_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(3, frame_width)
cap.set(4, frame_height)


# WRITE: Write the video file
output_file_name = 'output-' + os.path.basename(config.input.video_file_path)
output_file_name = os.path.join(config.output.path, output_file_name)
writer = create_video_writer(cap, output_file_name=output_file_name)


# TRACK: Initialize SORT tracker
car_tracker = Sort(max_age=20, min_hits=2, iou_threshold=0.1)
# video_dim_x = config.input.video_dim_x
# video_dim_y = config.input.video_dim_y

# lx, ly, rx, ry = [
#     (video_dim_x*1)//5, video_dim_y//3,
#     (video_dim_x*7)//8, video_dim_y//3
# ]

lx, ly, rx, ry = [
    (frame_width*1)//5, frame_height//3,
    (frame_width*7)//8, frame_height//3
]

total_car_count = []


# MISC
frames_dropped = 0
frames_total = 0
time_start = time.time()

# MAIN
while cap.isOpened():
    success, image = cap.read()
    if not success:
        frames_dropped += 1
        break

    frames_total += 1

    target_region = cv2.bitwise_and(src1=image, src2=mask)
    final_image = target_region

    # YOLO MODEL: OBJECT DETECTION
    results = model(
        source=final_image,
        stream=False,
        classes=[2],  # Only detect cars
        visualize=False
    )

    detections = np.empty((0, 5))

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = [int(x) for x in [x1, y1, x2, y2]]
            xyxy = (x1, y1, x2, y2)

            w, h = x2 - x1, y2 - y1

            conf = round(float(box.conf[0]), 2)
            detected_class_index = int(box.cls[0])
            detected_class_name = config.class_names.get(detected_class_index, 'N/A').title()

            if conf >= config.model_configs.threshold and detected_class_index == 2:  # Only consider 'car' class with confidence >= 0.4
                current_array = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, current_array))

            # Corner Circles (BGR) - For Debugging Purpose
            # cv2.circle(img=image, center=(x1, y1), radius=8, color=(255,0,0), thickness=5)    # Top left - BLUE
            # cv2.circle(img=image, center=(x1+w, y1), radius=8, color=(0,0,0), thickness=5)    # Top right - BLACK
            # cv2.circle(img=image, center=(x2, y2), radius=8, color=(0,255,0), thickness=5)    # Bottom right - GREEN
            # cv2.circle(img=image, center=(x2-w, y2), radius=8, color=(0,0,255), thickness=5)  # Bottom left - RED

    # Update tracker with detections
    tracked_objects = car_tracker.update(detections)
    cv2.line(img=image, pt1=(lx, ly), pt2=(rx, ry), color=(0, 0, 255), thickness=3)
  
    # Draw bounding boxes and IDs on the image
    for tracker_result in tracked_objects:
        x1, y1, x2, y2, obj_id = tracker_result
        x1, y1, x2, y2, obj_id = [int(x) for x in [x1, y1, x2, y2, obj_id]]
        w, h = x2 - x1, y2 - y1

        cx, cy = x1+(w//2), y1+(h//2)

        # Draw circle
        cv2.circle(img=image, center=(cx, cy), radius=2, color=(255, 0, 255), thickness=2)  # Center

        # Corner Circles (BGR) - For Debugging Purpose
        # cv2.circle(img=image, center=(x1, y1), radius=3, color=(0,0,255), thickness=5)    # Top left
        # cv2.circle(img=image, center=(x1+w, y1), radius=3, color=(0,255,0), thickness=5)    # Top right
        # cv2.circle(img=image, center=(x2, y2), radius=3, color=(255,0,0), thickness=5)    # Bottom right
        # cv2.circle(img=image, center=(x2-w, y2), radius=3, color=(0,0,0), thickness=5)    # Bottom left

        if lx < cx < rx and ly - 10 < cy < ly + 10:
            if obj_id not in total_car_count:
                total_car_count.append(obj_id)
                cv2.line(img=image, pt1=(lx, ly), pt2=(rx, ry), color=(0, 255, 0), thickness=3)


        # DRAWING SECTION

        # Draw rectangle
        cvzone.cornerRect(
            img=image,
            bbox=(x1, y1, w, h),
            rt=1,  # Rectangle thickness
            colorR=(255, 0, 255),  # Rectangle colour
            t=2,  # Corner thickness
            colorC=(0, 255, 0),  # Corner Colour
            l=10  # Corner Length
        )

        # Put ID, class and conf on the bounding box
        cvzone.putTextRect(
            img=image,
            text=f'ID: {obj_id} | {detected_class_name} | {conf}',
            pos=(max(x1, 0), max(y1, 35)),
            scale=0.7,
            thickness=1,
            offset=3
        )

    # Draw total count
    cvzone.putTextRect(img=image, text=f'Total Count: {len(total_car_count)}', pos=(30, 30), scale=1, thickness=2)

    # Save output to the disk
    try:
        writer.write(image)
    except Exception as e:
        print(f"Error writing to video: {e}")

    # Show the video
    cv2.imshow("Media Player", image)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # cv2.waitKey(0)

    
cap.release()
writer.release()
cv2.destroyAllWindows()

time_end = time.time()
print(f'''
[+] Some important stats
    - Frames Total  : {frames_total}
    - Frames Dropped: {frames_dropped}
    - Time Total    : {round(time_end - time_start, 2)} sec

    - {video_file_path=}
    - {output_file_name=}
''')

