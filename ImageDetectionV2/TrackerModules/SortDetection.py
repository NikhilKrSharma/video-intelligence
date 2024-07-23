from ultralytics import YOLO
import numpy as np
import queue, cvzone, csv, math, os, cv2
from TrackerModules.sort import *
from tqdm import tqdm

class Person:
    def __init__(self, person_id, age, gender, snapshot, timestamp):
        self.person_id = person_id
        self.age = age
        self.gender = gender
        self.snapshot = snapshot
        self.timestamp = timestamp

def detectObject(mode, video=None, save_video=False, show_video=True):

    model = YOLO("yolov8n.pt")
    
    # Load class names from classes.txt
    with open('Config/classes.txt', 'r') as f:
        class_names = [line.strip() for line in f.readlines()]

    # Predefined colors for bounding boxes
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

    # Load face, age, and gender models
    site = "DetectionModules/"     
    face_net = cv2.dnn.readNet(f"{site}opencv_face_detector_uint8.pb", f"{site}opencv_face_detector.pbtxt")     
    age_net = cv2.dnn.readNetFromCaffe(f"{site}age_deploy.prototxt", f"{site}age_net.caffemodel")     
    gender_net = cv2.dnn.readNetFromCaffe(f"{site}gender_deploy.prototxt", f"{site}gender_net.caffemodel")

    age_list = ['(0-10)', '(11-20)', '(21-30)', '(31-40)', '(41-50)', '(51-60)', '(61-70)', '(71-100)']
    gender_list = ['Male', 'Female']

    # Capture video from camera or file
    if mode == 1:
        cap = cv2.VideoCapture(0)  # Use the laptop's camera
    else:
        cap = cv2.VideoCapture(f"Media/{video}")  # Use the provided video file

    # Prepare CSV file for output
    if not os.path.exists("output"):
        os.makedirs("output")
    csv_file = open("output/people.csv", mode='w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['ID', 'Gender', 'Age', 'Photo'])

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Define the codec and create VideoWriter object if saving video
    video_output = None
    if save_video:
        video_output = cv2.VideoWriter('output/imagedetection.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
    
    # Create a progress bar
    progress_bar = tqdm(total=frame_count, desc="Processing Video")
    
    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Perform object detection
            results = model(frame, stream=True)
            detections = np.empty((0, 5))
            for r in results:
                boxes = r.boxes     
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cls = int(box.cls[0])
                    conf = math.ceil(box.conf[0] * 100) / 100
    
                    # Check for "person" class with confidence > 0.5
                    if conf > 0.5 and class_names[cls] == "person":
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detections = np.vstack((detections, currentArray))
    
        # Update tracker with detections
        if detections.shape[0] > 0:
            resultTracker = tracker.update(detections)
        else:
            resultTracker = tracker.update(np.empty((0, 5)))
    
        snapshot_frame = frame.copy()
    
        for res in resultTracker:
            x1, y1, x2, y2, id = res
            x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
            w, h = x2 - x1, y2 - y1
    
            # Ensure bounding box is valid
            if x1 < 0 or y1 < 0 or x2 > frame.shape[1] or y2 > frame.shape[0]:
                continue  # Skip this detection if out of bounds
            
            label = f"ID {id}"
            color = predefined_colors[id % len(predefined_colors)]
    
            # Only create blob if the bounding box is valid
            face_region = frame[y1:y2, x1:x2]
            if face_region.size == 0:
                continue  # Skip if the face region is empty
            
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
    
                        # Ensure face bounding box is within the frame
                        if fx < 0 or fy < 0 or fx2 > frame.shape[1] or fy2 > frame.shape[0]:
                            continue
                        
                        face = frame[fy:fy2, fx:fx2]
    
                        if face.size == 0:
                            continue
                        
                        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
                        
                        # Detect Gender
                        gender_net.setInput(blob)
                        gender_preds = gender_net.forward()
                        gender = gender_list[gender_preds[0].argmax()]
    
                        # Detect Age
                        age_net.setInput(blob)
                        age_preds = age_net.forward()
                        age = age_list[age_preds[0].argmax()]
    
                        # Check if person is already in the list
                        person_idx = next((i for i, p in enumerate(people_list) if p.person_id == id), None)
                        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
    
                        if person_idx is None:
                            snapshot = snapshot_frame[y1:y2, x1:x2].copy() 
                            people_list.append(Person(id, age, gender, snapshot, timestamp))
                            labels[id] = f"ID {id}: {gender}, {age}"
                        else:
                            # Update existing label if age or gender changes
                            existing_person = people_list[person_idx]
                            existing_person.age = age
                            existing_person.gender = gender
                            labels[id] = f"ID {id}: {gender}, {age}"
    
                        break
                    
            # If confidence is 0, remove the person and continue
            if confidence == 0:
                people_list = [p for p in people_list if p.person_id != id]
                labels.pop(id, None)  # Safely remove label entry
                # Reassign IDs
                for idx, person in enumerate(people_list):
                    person.person_id = idx + 1
    
            if id in labels:
                label = labels[id]
                cvzone.cornerRect(frame, (x1, y1, w, h), l=9, rt=2, colorR=color)
                cvzone.putTextRect(frame, label, (x1, y1), scale=1, thickness=1, colorR=(0, 0, 255))
    
            # Update queue with the current people list
            if not people_list_queue.full():
                people_list_queue.put(people_list.copy())
    
        # Display total people count
        cv2.putText(frame, f"Total People: {len(people_list)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
        # Write the current people list to CSV file
        if not people_list_queue.empty():
            current_people_list = people_list_queue.get()
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
    
            with open('output/people.csv', mode='w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(["Timestamp", "ID", "Gender", "Age", "Photo"])
    
                for person in current_people_list:
                    photo_path = os.path.join(output_dir, f"person_{person.person_id}.png")
                    cv2.imwrite(photo_path, person.snapshot)
                    csv_writer.writerow([person.timestamp, person.person_id, person.gender, person.age, photo_path])
    
        # Save video frame if enabled
        if save_video and video_output:
            video_output.write(frame)
    
        # Display video frame if enabled
        if show_video:
            cv2.imshow("Img", frame)
    
        # Update progress bar
        progress_bar.update(1)
    
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key to exit
            break
        elif key == ord('p'):  # 'p' key to pause/unpause
            paused = not paused
    
    # Close CSV file
    csv_file.close()
    cap.release()
    
    # Release video writer if enabled
    if save_video and video_output:
        video_output.release()
    
    # Close progress bar
    progress_bar.close()
    
    # Close all OpenCV windows
    if show_video:
        cv2.destroyAllWindows()