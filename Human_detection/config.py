MODEL_NAME="yolov8l.pt"
DATA_PATH = "./data"
OUTPUT_YOLO = "./data/outputYOLO"

# set threshold for marking object as detected in required class
DETECTION_THRESHOLD=0.35
REQUIRED_PATHS = [DATA_PATH, OUTPUT_YOLO]
ANALYSIS = True
ANALYSIS_FILE_PATH = "./data/Analysis.yaml"