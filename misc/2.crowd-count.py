import cv2
from ultralytics import YOLO

# # ultralytics.checks()

def count_people_in_video(input_source=0):
    # Load the YOLOv8 model
    model = YOLO('yolov8n.pt')  # Using the YOLOv8 nano model for demo purposes

    print(f'[+] {input_source=}')

    # Open the camera
    cap = cv2.VideoCapture(input_source)
    if not cap.isOpened():
        print("Error: Unable to open the camera or provided media!")
        return

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read the frame")
                break

            # Mirror the frame
            if input_source==0:
                frame = cv2.flip(frame, 1)

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

            # Display the frame
            cv2.imshow('Video with People Count', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Script interrupted by user. Releasing resources...")

    finally:
        # Release the camera and destroy all windows
        cap.release()
        cv2.destroyAllWindows()

# Example usage
count_people_in_video(input_source='/Users/nikhil20.sharma/Downloads/officeMovie.mov')
