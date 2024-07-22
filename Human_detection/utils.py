import cv2
import config 
import os
import time
import yaml
def predict(model, img, classes = [], conf=0.5):
    if classes:
        results = model.predict(img,classes=classes,conf=conf)
    else:
        results = model.predict(img,classes=classes,conf=conf)
    return results

def predict_and_detect(model, img, classes=[], conf=0.5):
    results = predict(model, img, classes=classes, conf=conf)

    for result in results:
        for box in result:
            boxes = box.boxes
            for i in range(len(boxes)):
            # Create bounding rectangle
                x1, y1, x2, y2 = int(boxes.xyxy[i][0]), int(boxes.xyxy[i][1]), int(boxes.xyxy[i][2]), int(boxes.xyxy[i][3])

                # Draw rectangle on the image
                cv2.rectangle(img, (x1, y1), (x2, y2), (105, 140, 80), 2)  # 2 is the thickness of the rectangle border

                # Text label
                class_id = int(boxes.cls[i])
                class_name = result.names[class_id]  # Assuming 'result.names' is a list of class names
                confidence = float(boxes.conf[i])   # Confidence score
                label = f"{class_name} {confidence:.2f}"
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
    return img, results
            # break
    return

def createVideoWriter(video_cap,output_file_name):
    frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(video_cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_file_name,fourcc, frame_rate, (frame_width, frame_height))
    return writer

def setupRequiredPaths():
    required_paths = config.REQUIRED_PATHS
    for path in required_paths:
        os.makedirs(path,exist_ok=True)


def convert_seconds_to_hhmmss(time_in_seconds):
    time_in_seconds = int(time_in_seconds)
    hours = time_in_seconds//3600
    minutes = (time_in_seconds%3600)//60
    time_in_seconds = time_in_seconds%60
    return f"{int(hours):02}:{int(minutes):02}:{int(time_in_seconds):02}"

def get_video_length(input_video):
    print("getting video length")
    cap = cv2.VideoCapture(input_video)
    if cap.isOpened():
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        length = frame_count/fps
    else:
        length=0
    cap.release()
    return length

def write_report_file(report_file, input_video_name, video_length, time_taken):
    print("writing report")
    data = {
        'input_video_name': input_video_name,
        'video_length': convert_seconds_to_hhmmss(video_length),
        'time_taken': convert_seconds_to_hhmmss(time_taken)
    }

    existing_data = []
    if os.path.exists(report_file):
        try:
            with open(report_file, 'r') as file:
                existing_data = yaml.safe_load(file) or []
        except yaml.YAMLError:
            print("Error reading YAML file. Starting with an empty list.")
        except Exception as e:
            print(f"Unexpected error reading file: {e}. Starting with an empty list.")
    else:
        # Create the file if it doesn't exist
        with open(report_file, 'w') as file:
            pass

    existing_data.append(data)

    with open(report_file, 'w') as file:
        yaml.dump(existing_data, file)


def add_result_to_analysis_report(input_video_name, time_taken):
    print("Adding result to analysis report")
    video_length = get_video_length(input_video_name)
    write_report_file(config.ANALYSIS_FILE_PATH, input_video_name, video_length, time_taken)
    return


