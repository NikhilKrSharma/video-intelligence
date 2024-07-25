import cv2 
import os
from ultralytics import YOLO 
import config
import utils 
from argparse import ArgumentParser
import time 

utils.setupRequiredPaths()
demo_video = f"{config.DATA_PATH}/input_videos/8972_C9_2m_chuncks/chunk_1.mp4"
parser = ArgumentParser("Human Detection", "Use parser to provide input audio path to perform human detection in a video")
parser.add_argument("--input_video",default=demo_video,help="Please provide the input video path")

args = parser.parse_args()
dataPath = config.DATA_PATH
detection_threshold=config.DETECTION_THRESHOLD
output_dir = config.OUTPUT_YOLO
model_name = config.MODEL_NAME
model = YOLO(model_name)

def detect_human(input_video):
    st = time.time()
    cap = cv2.VideoCapture(input_video)
    output_path = f'{output_dir}/{input_video.split("/")[-1]}'
    writer = utils.createVideoWriter(cap,output_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result_img,prediction = utils.predict_and_detect(model, frame, classes=[0], conf=detection_threshold)
        writer.write(result_img)
        cv2.imshow("Image",result_img)

        cv2.waitKey(1)
    writer.release()
    et = time.time()
    time_taken = et-st
    print(f"time taken : {time_taken}")
    if config.ANALYSIS:
        utils.add_result_to_analysis_report(input_video,time_taken)


if __name__ == "__main__":
    if args.input_video:
        if os.path.isdir(args.input_video):
            # Get all .mp4 files in the directory
            video_files = [os.path.join(args.input_video, f) for f in os.listdir(args.input_video) if f.endswith('.mp4')]
            
            # Call detect_human for each .mp4 file
            for video_file in video_files:
                detect_human(video_file)
        else:
            input_video = args.input_video
            detect_human(input_video)
    else:
        input_video=demo_video
        detect_human(input_video)