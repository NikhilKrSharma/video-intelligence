# # import cv2
# # import os

# # def play_video(video_path):

# #     # Check if the file exists
# #     if not os.path.isfile(video_path):
# #         print(f"Error: File does not exist {video_path}")
# #         return

# #     # Open video capture with FFMPEG backend
# #     cap = cv2.VideoCapture(video_path)
    
# #     if not cap.isOpened():
# #         print(f"Error: Could not open video {video_path}")
# #         return

# #     # Print video properties
# #     frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# #     frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# #     frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
# #     fps = cap.get(cv2.CAP_PROP_FPS)
    
# #     print(f"Frame width: {frame_width}")
# #     print(f"Frame height: {frame_height}")
# #     print(f"Frame count: {frame_count}")
# #     print(f"FPS: {fps}")

# #     frames = 0
# #     while cap.isOpened():
# #         print(f'Reading frame no: {frames}')
# #         frames += 1
# #         ret, frame = cap.read()
# #         if not ret:
# #             print("Error: Could not read frame")
# #             break

# #         # Display the frame
# #         cv2.imshow('Video', frame)
        
# #         # Press 'q' to exit the loop
# #         if cv2.waitKey(1) & 0xFF == ord('q'):
# #             break
    
# #     cap.release()
# #     cv2.destroyAllWindows()


# # # play_video(video_path='officeMovie.avi')
# # play_video(video_path='/Users/nikhil20.sharma/Downloads/officeMovie.mov')

# # ##########################################################################
# # # INFERENCE ARGUMENTS
# # # vid_stride: Frame stride for video inputs. Allows skipping frames in videos to speed up processing at the cost of temporal resolution. A value of 1 processes every frame, higher values skip frames.
# # # visualize: Activates visualization of model features during inference, providing insights into what the model is "seeing". Useful for debugging and model interpretation.
# # # augment: Enables test-time augmentation (TTA) for predictions, potentially improving detection robustness at the cost of inference speed.
# # # classes: Filters predictions to a set of class IDs. Only detections belonging to the specified classes will be returned. Useful for focusing on relevant objects in multi-class detection tasks.
# # # retina_masks: Uses high-resolution segmentation masks if available in the model. This can enhance mask quality for segmentation tasks, providing finer detail.

# # # VISUALISATION ARGUMENTS
# # # show: If True, displays the annotated images or videos in a window. Useful for immediate visual feedback during development or testing.
# # # save: Enables saving of the annotated images or videos to file. Useful for documentation, further analysis, or sharing results.
# # # save_frames: When processing videos, saves individual frames as images. Useful for extracting specific frames or for detailed frame-by-frame analysis.
# # # save_txt: Saves detection results in a text file, following the format [class] [x_center] [y_center] [width] [height] [confidence]. Useful for integration with other analysis tools.
# # # save_conf: Includes confidence scores in the saved text files. Enhances the detail available for post-processing and analysis.
# # # save_crop: Saves cropped images of detections. Useful for dataset augmentation, analysis, or creating focused datasets for specific objects.
# # # show_labels: Displays labels for each detection in the visual output. Provides immediate understanding of detected objects.
# # # show_conf: Displays the confidence score for each detection alongside the label. Gives insight into the model's certainty for each detection.
# # # show_boxes: Draws bounding boxes around detected objects. Essential for visual identification and location of objects in images or video frames.
# # # line_width: Specifies the line width of bounding boxes. If None, the line width is automatically adjusted based on the image size. Provides visual customization for clarity.

# # # Classes
# # # names = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}

# # ##########################################################################

# # from ultralytics import YOLO

# # # Load a model
# # model = YOLO("yolov8n.pt")  # pretrained YOLOv8n model

# # # Run batched inference on a list of images
# # results = model(["im1.jpg", "im2.jpg"])  # return a list of Results objects

# # # Process results list
# # for result in results:
# #     boxes = result.boxes  # Boxes object for bounding box outputs
# #     masks = result.masks  # Masks object for segmentation masks outputs
# #     keypoints = result.keypoints  # Keypoints object for pose outputs
# #     probs = result.probs  # Probs object for classification outputs
# #     obb = result.obb  # Oriented boxes object for OBB outputs
# #     result.show()  # display to screen
# #     result.save(filename="result.jpg")  # save to disk




# # ##########################################################################





import os
import sys
import cv2
import yaml
from box import Box



with open('./config.yaml', 'r') as file:
    config = yaml.safe_load(file)


# Convert to Box
config = Box(config)


def create_video_writer(video_cap, output_file_name):
    frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(video_cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    writer = cv2.VideoWriter(
        filename=output_file_name,
        fourcc=fourcc,
        fps=frame_rate,
        frameSize=(frame_width, frame_height)
    )
    return writer

cap = cv2.VideoCapture(config.input.video_file_path)

output_file_name = 'output-' + os.path.basename(config.input.video_file_path)
output_file_name = os.path.join(config.output.path, output_file_name)
writer = create_video_writer(cap, output_file_name=output_file_name)

print(f'{config.input.video_file_path=}')
print(f'{output_file_name=}')

while cap.isOpened():

    success, image = cap.read()

    if success:
        cv2.imshow("Media Player", image)
        try:
            writer.write(image)
        except Exception as e:
            print(f"Error writing to video: {e}")
    else:
        print("Video finished")
        break

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
writer.release()
cv2.destroyAllWindows()









