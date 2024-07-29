# import cv2
# from match_face_embeddings import recognize_faces
# import os
# import time
# import config
# from utils import createRequiredPaths
# from multiprocessing import Process, Queue

# class Camera:
#     def __init__(self, camera_no, location, zone_no, zone_name, interval, source, results_queue):
#         self.camera_no = camera_no
#         self.location = location
#         self.zone_no = zone_no
#         self.zone_name = zone_name
#         self.interval = interval
#         self.source = source
#         self.results_queue = results_queue

#     def process_frame(self, cap):
#         ret, frame = cap.read()
#         if not ret:
#             print(f"Failed to capture frame from camera {self.camera_no}")
#             return []

#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         temp_image_path = f"{config.DATA_PATH}/temp/temp_frame_{self.camera_no}.jpg"
#         cv2.imwrite(temp_image_path, rgb_frame)

#         camera_details = {"camera_no": self.camera_no, "zone_no": self.zone_no, "zone_name": self.zone_name}
#         results = recognize_faces(temp_image_path, camera_details)
#         return results

#     def release(self, cap):
#         if cap:
#             cap.release()
#             cv2.destroyAllWindows()

#     def startCapturing(self):
#         cap = cv2.VideoCapture(self.source)
#         try:
#             print(f"Started capturing frame for camera {self.camera_no}")
#             while True:
#                 start_time = time.time()
#                 results = self.process_frame(cap)
#                 for result in results:
#                     print(result)
#                     self.results_queue.put(result)

#                 time_to_wait = self.interval - (time.time() - start_time)
#                 if time_to_wait > 0:
#                     time.sleep(time_to_wait)
#         except KeyboardInterrupt:
#             print(f"Stopping the camera feed processing. Error in Capturing Frame in Camera No: {self.camera_no}")
#         finally:
#             print(f"Stopping the camera feed processing in Camera No: {self.camera_no}")
#             self.release(cap)

#     def start(self):
#         process = Process(target=self.startCapturing)
#         process.start()
#         return process

import cv2
from match_face_embeddings import recognize_faces
import os
import time
import config
from utils import createRequiredPaths
from multiprocessing import Process, Queue

class Camera:
    def __init__(self, camera_no, location, zone_no, zone_name, interval, source, results_queue):
        self.camera_no = camera_no
        self.location = location
        self.zone_no = zone_no
        self.zone_name = zone_name
        self.interval = interval
        self.source = source
        self.results_queue = results_queue

    def process_frame(self, cap, frame_no):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to capture frame from camera {self.camera_no}")
            return []

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        temp_image_path = f"{config.DATA_PATH}/temp/temp_frame_{self.camera_no}.jpg"
        cv2.imwrite(temp_image_path, rgb_frame)

        camera_details = {"camera_no": self.camera_no, "zone_no": self.zone_no, "zone_name": self.zone_name}
        results = recognize_faces(temp_image_path, camera_details)
        return results

    def release(self, cap):
        if cap:
            cap.release()
            cv2.destroyAllWindows()

    def startCapturing(self):
        cap = cv2.VideoCapture(self.source)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * self.interval)
        frame_no = 0

        try:
            print(f"Started capturing frame for camera {self.camera_no}")
            while True:
                start_time = time.time()
                results = self.process_frame(cap, frame_no)
                for result in results:
                    print(result)
                    self.results_queue.put(result)

                frame_no += frame_interval

                # Wait until one interval time have passed since the start of the loop
                time_to_wait = self.interval - (time.time() - start_time)
                if time_to_wait > 0:
                    time.sleep(time_to_wait)
        except KeyboardInterrupt:
            print(f"Stopping the camera feed processing. Error in Capturing Frame in Camera No: {self.camera_no}")
        finally:
            print(f"Stopping the camera feed processing in Camera No: {self.camera_no}")
            self.release(cap)

    def start(self):
        process = Process(target=self.startCapturing)
        process.start()
        return process
