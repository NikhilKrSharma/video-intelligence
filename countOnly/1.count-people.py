import cv2
import time
import cvzone
from ultralytics import YOLO 

# Class IDs from COCO dataset
class_names = {
    0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 
    6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 
    11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 
    16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 
    21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 
    26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 
    31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 
    36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 
    41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 
    46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 
    51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 
    56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 
    61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 
    66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 
    71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 
    76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'
}


# CONFIGURATIONS
video_path               = '../data/processed_8910_C1_5min.mp4'
image_write_path         = '../data/images'
output_file_name         = '../data/processed_8910_C1_5min_output.mp4'
model_name               = '../yolo-models/yolov8n.pt'
model_name_for_file_name = model_name.split('/')[-1].split('.')[0]


# MODEL INITIALIZATION
global model
model = YOLO(model_name)

# Open the video file
cap = cv2.VideoCapture(video_path)


time_start = time.time()

if not cap.isOpened():
    print(f"Error: Unable to open video file {video_path}")

# Get the frames per second (fps) of the video
fps = int(cap.get(cv2.CAP_PROP_FPS))
print(f'Detected FPS: {fps}')

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

    frame_original = frame.copy()

    # Process the results

    # Perform detection on the current frame
    results = model(frame, classes=[0])
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