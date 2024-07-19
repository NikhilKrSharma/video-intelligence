import cv2
from ultralytics import YOLO
import numpy as np

def detectObject(mode, peopleOnly, video=None):
    model = YOLO("yolov8m.pt")

    # Load class names from classes.txt
    with open('classes.txt', 'r') as f:
        class_names = [line.strip() for line in f.readlines()]

    # List of predefined colors
    predefined_colors = [
        (0, 0, 255),    # Red
        (255, 0, 0),    # Blue
        (0, 255, 0),    # Green
        (0, 255, 255),  # Yellow
        (0, 165, 255),  # Orange
        (0, 0, 0),      # Black
        (255, 255, 255) # White
    ]

    color_dict = {}
    paused = False

    # Prompt user for input source
    if mode == 1: cap = cv2.VideoCapture(0)  # Use the laptop's camera
    else: cap = cv2.VideoCapture(f"Media/{video}")  # Use the provided video file

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break
            
            result = model(frame, device="mps")[0]
            bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
            classes = np.array(result.boxes.cls.cpu(), dtype="int")
    
            # Count the number of people in the frame
            people = sum(1 for cls in classes if class_names[cls] == "person")
    
            for idx, (cls, bbox) in enumerate(zip(classes, bboxes)):
                class_name = class_names[cls] if cls < len(class_names) else str(cls)
                if (peopleOnly and class_name == "person") or not peopleOnly:
                    (x, y, x2, y2) = bbox
                    if idx not in color_dict:
                        if idx < len(predefined_colors):
                            color_dict[idx] = predefined_colors[idx]
                        else:
                            color_dict[idx] = (0, np.random.randint(0, 255), np.random.randint(0, 255))

                    color = color_dict[idx]
                    cv2.rectangle(frame, (x, y), (x2, y2), color, 2)
                    cv2.putText(frame, class_name, (x, y - 5), cv2.FONT_HERSHEY_DUPLEX, 1, color, 2)
    
            # Display the total number of people in the frame
            cv2.putText(frame, f"Total People: {people}", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
    
        cv2.imshow("Img", frame)
        key = cv2.waitKey(1)
    
        if key == 27: break # ESC key to exit
        elif key == ord('p'):  # 'p' key to pause/unpause
            paused = not paused
    
    cap.release()
    cv2.destroyAllWindows()