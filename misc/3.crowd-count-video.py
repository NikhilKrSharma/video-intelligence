import cv2
from ultralytics import YOLO

def count_people_in_video(video_input_path, video_output_path):
    # Load the YOLOv8 model
    model = YOLO('./yolo-models/yolov8n.pt')

    # Open the input video file
    cap = cv2.VideoCapture(video_input_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_input_path}")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'FFMPEG')  # Codec for mp4 files
    out = cv2.VideoWriter(video_output_path, fourcc, fps, (frame_width, frame_height))
    if not out.isOpened():
        print(f"Error: Unable to open video writer for {video_output_path}")
        return

    frame_count = 0
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print(f"Finished processing {frame_count} frames")
                break

            frame_count += 1

            # Perform detection on the current frame
            results = model(frame)

            # Process the results
            person_count = 0
            for result in results:
                if hasattr(result, 'boxes'):
                    boxes = result.boxes
                    for box in boxes:
                        class_id = box.cls.item()  # Class ID
                        if class_id == 0:  # Assuming '0' is the class ID for 'person'
                            person_count += 1

            # Draw the count of people at the top right corner of the frame
            text = f"People count: {person_count}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
            text_x = frame.shape[1] - text_size[0] - 10
            text_y = text_size[1] + 10

            cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 255, 0), font_thickness)

            # Write the frame to the output video file
            out.write(frame)

            # Optionally display the frame (remove this in the final script if not needed)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Script interrupted by user. Releasing resources...")

    finally:
        # Release the video capture and writer objects
        cap.release()
        out.release()
        cv2.destroyAllWindows()

# Example usage
count_people_in_video(
    video_input_path='./Data/RawFromBusiness/processed_8667_C2.mp4',
    video_output_path='output_video.mp4'
)



# results = model(source=..., stream=True)  # generator of Results objects
#     for r in results:
#         boxes = r.boxes  # Boxes object for bbox outputs
#         masks = r.masks  # Masks object for segment masks outputs
#         probs = r.probs  # Class probabilities for classification outputs