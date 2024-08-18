# CONFIGURATIONS
video_path: str = '../data/processed_8910_C1_2min.mp4'
image_write_path: str = '../data/images'
video_output_file_path: str = '../data/processed_8910_C1_5min_output.mp4'
model_name: str = '../yolo-models/yolov8n.pt'
model_name_for_file_name = model_name.split('/')[-1].split('.')[0]
frames_per_second: int = 2
skip_frame: bool = True
# mask_path: str = './store-mask.jpg'
mask_path: bool = False

