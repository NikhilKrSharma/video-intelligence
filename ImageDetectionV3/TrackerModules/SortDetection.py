import logging
from ultralytics import YOLO
import numpy as np
import queue
import cvzone
import csv
import math
import os
import cv2
from TrackerModules.sort import *
from tqdm import tqdm
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

class Person:
    def __init__(self, person_id, age, gender, snapshot, timestamp):
        self.person_id = person_id
        self.age_history = [age]
        self.gender_history = [gender]
        self.snapshot = snapshot
        self.timestamp_history = [timestamp]

    def add_result(self, age, gender, snapshot, timestamp):
        self.age_history.append(age)
        self.gender_history.append(gender)
        self.timestamp_history.append(timestamp)
        self.snapshot = snapshot  # Update snapshot to the latest

    def get_final_result(self):
        # Compute mode for age and gender
        age_mode = Counter(self.age_history).most_common(1)[0][0]
        gender_mode = Counter(self.gender_history).most_common(1)[0][0]
        # Use the first timestamp from history
        timestamp = self.timestamp_history[0]
        return age_mode, gender_mode, timestamp

# Suppress YOLO logging
logging.getLogger("ultralytics").setLevel(logging.ERROR)

def process_frame(frame, model, class_names, tracker, predefined_colors, people_list, labels):
    detections = np.empty((0, 5))
    results = model(frame, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cls = int(box.cls[0])
            conf = math.ceil(box.conf[0] * 100) / 100

            if conf > 0.5 and class_names[cls] == "person":
                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))

    resultTracker = tracker.update(detections) if detections.shape[0] > 0 else tracker.update(np.empty((0, 5)))
    snapshot_frame = frame.copy()

    for res in resultTracker:
        x1, y1, x2, y2, id = res
        x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
        w, h = x2 - x1, y2 - y1

        if x1 < 0 or y1 < 0 or x2 > frame.shape[1] or y2 > frame.shape[0]:
            continue

        face_region = frame[y1:y2, x1:x2]
        if face_region.size == 0:
            continue

        face_blob = cv2.dnn.blobFromImage(face_region, 1.0, (300, 300), (104.0, 177.0, 123.0))
        face_net.setInput(face_blob)
        face_detections = face_net.forward()

        confidence = 0
        if face_detections.shape[2] > 0:
            for i in range(face_detections.shape[2]):
                confidence = face_detections[0, 0, i, 2]
                if confidence > 0:
                    box = face_detections[0, 0, i, 3:7] * np.array([x2 - x1, y2 - y1, x2 - x1, y2 - y1])
                    (fx, fy, fx2, fy2) = box.astype("int")
                    fx += x1
                    fy += y1
                    fx2 += x1
                    fy2 += y1

                    if fx < 0 or fy < 0 or fx2 > frame.shape[1] or fy2 > frame.shape[0]:
                        continue

                    face = frame[fy:fy2, fx:fx2]
                    if face.size == 0:
                        continue

                    blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

                    gender_net.setInput(blob)
                    gender_preds = gender_net.forward()
                    gender = gender_list[gender_preds[0].argmax()]

                    age_net.setInput(blob)
                    age_preds = age_net.forward()
                    age = age_list[age_preds[0].argmax()]

                    person_idx = next((i for i, p in enumerate(people_list) if p.person_id == id), None)
                    timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)

                    if person_idx is None:
                        snapshot = snapshot_frame[y1:y2, x1:x2].copy()
                        people_list.append(Person(id, age, gender, snapshot, timestamp))
                        labels[id] = f"ID {id}: {gender}, {age}"
                    else:
                        existing_person = people_list[person_idx]
                        existing_person.add_result(age, gender, snapshot_frame[y1:y2, x1:x2].copy(), timestamp)
                        labels[id] = f"ID {id}: {gender}, {age}"

                    break

        if confidence == 0:
            people_list = [p for p in people_list if p.person_id != id]
            labels.pop(id, None)

        if id in labels:
            label = labels[id]
            color = predefined_colors[id % len(predefined_colors)]
            cvzone.cornerRect(frame, (x1, y1, w, h), l=9, rt=2, colorR=color)
            cvzone.putTextRect(frame, label, (x1, y1), scale=1, thickness=1, colorR=(0, 0, 255))

        if not people_list_queue.full():
            people_list_queue.put(people_list.copy())

    return frame, people_list, labels

def detectObject(mode, video=None, save_video=False, show_video=True):
    global cap, face_net, age_net, gender_net, age_list, gender_list, people_list_queue

    model = YOLO("yolov8n.pt")

    with open('ImageDetectionV3/Config/classes.txt', 'r') as f:
        class_names = [line.strip() for line in f.readlines()]

    predefined_colors = [
        (0, 0, 255),    # Red
        (255, 0, 0),    # Blue
        (0, 255, 0),    # Green
        (0, 255, 255),  # Yellow
        (0, 165, 255),  # Orange
        (0, 0, 0),      # Black
        (255, 255, 255) # White
    ]

    labels = {}
    paused = False
    people_list = []
    people_list_queue = queue.Queue()
    tracker = Sort(100, 3, 0.3)

    site = "ImageDetectionV3/DetectionModules/"
    face_net = cv2.dnn.readNet(f"{site}opencv_face_detector_uint8.pb", f"{site}opencv_face_detector.pbtxt")
    age_net = cv2.dnn.readNetFromCaffe(f"{site}age_deploy.prototxt", f"{site}age_net.caffemodel")
    gender_net = cv2.dnn.readNetFromCaffe(f"{site}gender_deploy.prototxt", f"{site}gender_net.caffemodel")

    age_list = ['(0-10)', '(11-20)', '(21-30)', '(31-40)', '(41-50)', '(51-60)', '(61-70)', '(71-100)']
    gender_list = ['Male', 'Female']

    cap = cv2.VideoCapture(0) if mode == 1 else cv2.VideoCapture(f"ImageDetectionV3/Media/{video}")

    if not os.path.exists("ImageDetectionV3/output"):
        os.makedirs("ImageDetectionV3/output")
    csv_file = open("ImageDetectionV3/output/people.csv", mode='w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['ID', 'Gender', 'Age', 'Timestamp', 'Photo'])

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    video_output = None
    if save_video:
        video_output = cv2.VideoWriter('ImageDetectionV3/output/imagedetection.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    progress_bar = tqdm(total=frame_count, desc="Processing Video")

    frame_idx = 0
    stop_processing = False

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []

        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_idx += 1

                if frame_idx % 5 == 0:
                    futures.append(executor.submit(process_frame, frame, model, class_names, tracker, predefined_colors, people_list, labels))

                if futures:
                    for future in futures:
                        frame, people_list, labels = future.result()

                if save_video and video_output is not None:
                    video_output.write(frame)

                if show_video:
                    cv2.imshow("Frame", frame)
                    key = cv2.waitKey(1) & 0xFF

                    if key == ord('q'):
                        stop_processing = True
                        break
                    elif key == ord('p'):
                        paused = not paused

            progress_bar.update(1)

            if stop_processing:
                break

        for person in people_list:
            age, gender, timestamp = person.get_final_result()
            filename = f"ImageDetectionV3/output/person_{person.person_id}.png"
            cv2.imwrite(filename, person.snapshot)
            csv_writer.writerow([person.person_id, gender, age, timestamp, filename])

    cap.release()
    if video_output is not None:
        video_output.release()
    cv2.destroyAllWindows()
    csv_file.close()
    progress_bar.close()