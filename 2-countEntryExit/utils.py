# -*- coding: utf-8 -*-

import os
import cv2
import time
import cvzone
from ultralytics import YOLO
import ffmpeg
from pprint import pprint


def get_class_names(verbose=None):
    '''Class IDs from COCO dataset'''
    
    if verbose is None:
        verbose = True if os.environ.get('VERBOSE') in ['yes', 'y', 1] else False

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

    if verbose:
        print('+ Classes available in COCO dataset, used in YOLO models...')
        for key, val in class_names.items():
            print(f'[+] {key}: {val:<15}', end='\t')
            if (key+1)%5==0:
                print()


    return class_names


def create_video_writer(video_cap, output_file_name, frame_rate=None):

    frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if frame_rate is None:
        frame_rate = int(video_cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    writer = cv2.VideoWriter(
        filename=output_file_name,
        fourcc=fourcc,
        fps=frame_rate,
        frameSize=(frame_width, frame_height)
    )

    return writer

def get_video_properties(video_input_path, verbose=None):

    if not verbose:
        verbose = True if os.environ.get('VERBOSE') in ['yes', 'y', 1] else False

    # Capture the video from the input path
    cap = cv2.VideoCapture(video_input_path)

    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_input_path}")
        return

    # Get video properties
    properties = {
        "Frame Width": cap.get(cv2.CAP_PROP_FRAME_WIDTH),
        "Frame Height": cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
        "Frame Count": cap.get(cv2.CAP_PROP_FRAME_COUNT),
        "FPS": int(cap.get(cv2.CAP_PROP_FPS)),
        "Duration (seconds)": round(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS), 2),
        "FourCC Codec": int(cap.get(cv2.CAP_PROP_FOURCC)),
        "Brightness": cap.get(cv2.CAP_PROP_BRIGHTNESS),
        "Contrast": cap.get(cv2.CAP_PROP_CONTRAST),
        "Saturation": cap.get(cv2.CAP_PROP_SATURATION),
        "Hue": cap.get(cv2.CAP_PROP_HUE),
        "Gain": cap.get(cv2.CAP_PROP_GAIN),
        "Exposure": cap.get(cv2.CAP_PROP_EXPOSURE),
        "Convert RGB": cap.get(cv2.CAP_PROP_CONVERT_RGB),
    }

    # Print video properties
    if verbose:
        print('+ Video properties:')
        for prop, value in properties.items():
            if prop == "FourCC Codec":
                # Decode FourCC codec
                codec = (
                    chr((value & 0XFF)),
                    chr((value & 0XFF00) >> 8),
                    chr((value & 0XFF0000) >> 16),
                    chr((value & 0XFF000000) >> 24)
                )
                value = ''.join(codec)
            print(f"- {prop:<20}: {value}")

    # Release the video capture object
    cap.release()

    print(f'+ Video properties fetched: {properties.keys()}')

    return properties


def yolo_model_pred(model, frame, classes=None, verbose=None):

    if not verbose:
        verbose = True if os.environ.get('VERBOSE') in ['yes', 'y', 1] else False

    if classes is None:
        results = model(frame)
    else:
        results = model(frame, classes=classes)

    return results


def split_video(video_input_path, video_output_dir='output_chunks', chunk_in_min=2, no_of_chunks=None):
    # Ensure the output directory exists
    os.makedirs(video_output_dir, exist_ok=True)

    # Capture the video from the input path
    cap = cv2.VideoCapture(video_input_path)

    # Get the video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_in_sec = frame_count / fps
    chunk_in_sec = chunk_in_min * 60

    # Calculate the number of chunks
    num_chunks = int(duration_in_sec // chunk_in_sec) + 1

    # Get the video width and height
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    counter = 0
    for chunk_index in range(num_chunks):
        # Define the codec and create VideoWriter object
        output_path = os.path.join(video_output_dir, f"chunk_{chunk_index + 1}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # Write frames for this chunk
        for frame_index in range(int(chunk_in_sec * fps)):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        out.release()

        counter += 1

        if no_of_chunks is not None and counter == no_of_chunks:
            break

    cap.release()
    print("Video has been split into chunks and saved to:", video_output_dir)


def extract_frames(video_path, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not video.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"FPS: {fps}")
    print(f"Total frames: {frame_count}")

    # Read frames and save as images
    frame_number = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Generate output file path
        output_path = os.path.join(output_folder, f"frame_{frame_number:06d}.jpg")

        # Save frame as image
        cv2.imwrite(output_path, frame)

        frame_number += 1

        # Print progress
        if frame_number % 100 == 0:
            print(f"Extracted {frame_number} frames")

    # Release video capture object
    video.release()

    print(f"Extraction complete. {frame_number} frames extracted.")


def detect_n_draw_bounding_boxes(yolo_res, frame, draw_bb=True, verbose=False):

    detection_count = len(yolo_res[0])
    # if detection_count > 1 and draw_bb:
    if draw_bb:

        for result in yolo_res:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = [int(x) for x in [x1, y1, x2, y2]]
                xyxy = (x1, y1, x2, y2)

                w, h = x2 - x1, y2 - y1

                conf = round(float(box.conf[0]), 2)
                detected_class_index = int(box.cls[0])
                detected_class_name = get_class_names(verbose=False).get(detected_class_index, 'N/A').title()

                # Draw rectangle
                cvzone.cornerRect(img=frame, bbox=(x1, y1, w, h), rt=1, colorR=(255, 0, 255), t=2,
                                  colorC=(0, 255, 0), l=10)

                # Put ID, class and conf on the bounding box
                cvzone.putTextRect(img=frame, text=f'{detected_class_name} | {conf}', pos=(max(x1, 0), max(y1, 35)),
                                   scale=0.7, thickness=1, offset=3)

    return detection_count, frame


def detect_n_draw_bounding_boxes_new(results, frame, draw_bb=True, verbose=False):

    detection_count = len(results[0])
    frame_xy = frame.shape
    # if detection_count > 1 and draw_bb:
    if draw_bb:
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = [int(x) for x in box.xyxy[0]]
                xyxy = (x1, y1, x2, y2)

                # x, y, w, h = [int(x) for x in box.xywh[0]]

                w, h = x2 - x1, y2 - y1

                conf = round(float(box.conf[0]), 2)
                detected_class_index = int(box.cls[0])
                detected_class_name = get_class_names(verbose=False).get(detected_class_index, 'N/A').title()

                # Draw rectangle around detected objects
                cvzone.cornerRect(img=frame, bbox=(x1, y1, w, h), rt=1, colorR=(255, 0, 255), t=2,
                                  colorC=(0, 255, 0), l=10)

                # Put ID, class and conf on the bounding box
                cvzone.putTextRect(img=frame, text=f'{detected_class_name} | {conf}', pos=(max(x1, 0), max(y1, 35)),
                                   scale=0.7, thickness=1, offset=3)

            # Put total count of detections to top right corner
            cvzone.putTextRect(img=frame, text=f'Count: {len(result)}', pos=(max(5, 5), max(20, 35)),
                               scale=1, thickness=3, offset=3)

    return detection_count, frame


def split_video(video_input_path, video_output_dir='output_chunks', chunk_in_min=2, no_of_chunks=None):
    # Ensure the output directory exists
    os.makedirs(video_output_dir, exist_ok=True)

    # Capture the video from the input path
    cap = cv2.VideoCapture(video_input_path)

    # Get the video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_in_sec = frame_count / fps
    chunk_in_sec = chunk_in_min * 60

    # Calculate the number of chunks
    num_chunks = int(duration_in_sec // chunk_in_sec) + 1

    # Get the video width and height
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    counter = 0
    for chunk_index in range(num_chunks):
        # Define the codec and create VideoWriter object
        output_path = os.path.join(video_output_dir, f"chunk_{chunk_index + 1}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # Write frames for this chunk
        for frame_index in range(int(chunk_in_sec * fps)):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        out.release()

        counter += 1

        if no_of_chunks is not None and counter == no_of_chunks:
            break

    cap.release()
    print("Video has been split into chunks and saved to:", video_output_dir)


def extract_frames(video_path, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not video.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"FPS: {fps}")
    print(f"Total frames: {frame_count}")

    # Read frames and save as images
    frame_number = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Generate output file path
        output_path = os.path.join(output_folder, f"frame_{frame_number:06d}.jpg")

        # Save frame as image
        cv2.imwrite(output_path, frame)

        frame_number += 1

        # Print progress
        if frame_number % 100 == 0:
            print(f"Extracted {frame_number} frames")

    # Release video capture object
    video.release()

    print(f"Extraction complete. {frame_number} frames extracted.")


def probe_metadata(video_path):
    try:
        # Get the metadata of the video file
        probe = ffmpeg.probe(video_path)

        # Print the full metadata
        pprint(probe)

    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")
