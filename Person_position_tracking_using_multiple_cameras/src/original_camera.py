import cv2
from match_face_embeddings import recognize_faces
import os
import time
import threading
import config

class Camera:
    def __init__(self, camera_no, location, zone_no, zone_name,interval, source):
        self.camera_no = camera_no
        self.location = location
        self.zone_no = zone_no
        self.zone_name = zone_name
        self.source = source
        self.interval = config.FRAME_CAPTURE_INTERVAL
        self.cap = cv2.VideoCapture(source)

    def process_frame(self):
        # Capture a frame from the video source
        ret, frame = self.cap.read()
        if not ret:
            print(f"Failed to capture frame from camera {self.camera_no}")
            return []

        # Convert frame to RGB (face_recognition uses RGB format)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame to recognize faces and update the embeddings database
        # results = recognize_faces_from_frame(rgb_frame, embeddings_file)
        temp_image_path = f"{config.DATA_PATH}/temp/temp_frame.jpg"
        cv2.imwrite(temp_image_path, frame)
        # Use the recognize_faces function to process the frame
        camera_details = {"camera_no":self.camera_no,"zone_no":self.zone_no,"zone_name":self.zone_name}
        results = recognize_faces(temp_image_path, camera_details)
        return results

    def release(self):
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()

    def startCapturing(self):
        try:
            print("Started capturing frame")
            while True:
                start_time = time.time()
                results = self.process_frame()
                for result in results:
                    print(result)

                # Wait until one interval time have passed since the start of the loop
                time_to_wait = self.interval - (time.time() - start_time)
                if time_to_wait > 0:
                    time.sleep(time_to_wait)
        except KeyboardInterrupt:
            print(f"Stopping the camera feed processing. Some Error in Capturing Frame in Camera No:{self.camera_no}")
        finally:
            print(f"Stopping the camera feed processing in Camera No:{self.camera_no}")
            self.release()

def run_camera(camera):
    camera.startCapturing()



#   Example usage
if __name__ == "__main__":
    import time
    
    # Create a Camera object for a video file or camera feed (use 0 for default camera)
    camera1 = Camera(camera_no=1, location="Entrance", zone_no=1, zone_name="Main Entrance", interval=config.FRAME_CAPTURE_INTERVAL, source=0)
    camera1.startCapturing()



