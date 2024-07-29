from camera import Camera
import config
import time
from multiprocessing import Queue

class Tracker:
    def __init__(self, tracker_name="Tracker1", max_camera_count=config.MAX_CAMERA_COUNT):
        self.max_camera_count = max_camera_count
        self.tracker_name = tracker_name
        self.cameras = []
        self.processes = []
        self.results_queue = Queue()

    def addCamera(self, location, zone_no, zone_name, interval, source):
        camera_no = len(self.cameras) + 1
        newCamera = Camera(camera_no, location, zone_no, zone_name, interval, source, self.results_queue)
        self.cameras.append(newCamera)

    def startCameras(self, cameras_to_start):
        for camera_no in cameras_to_start:
            print(f"Starting camera {camera_no}")
            process = self.cameras[camera_no - 1].start()
            self.processes.append(process)

    def printCamerasDetails(self):
        for camera in self.cameras:
            print(f"Camera No: {camera.camera_no}, Zone Name: {camera.zone_name}")

    def collectResults(self):
        while True:
            try:
                result = self.results_queue.get(timeout=1)
                print("Collected result:", result)
            except:
                break

if __name__ == "__main__":
	tracker = Tracker()
	tracker.addCamera("Entrance", 1, "Main Entrance", config.FRAME_CAPTURE_INTERVAL, 0)
	tracker.addCamera("Floor1-center-left", 2, "Fitness Club", config.FRAME_CAPTURE_INTERVAL, f"{config.DATA_PATH}/inputs/videos/input1.mp4")
	tracker.addCamera("Floor2-main-playzone", 3, "Playzone", config.FRAME_CAPTURE_INTERVAL, f"{config.DATA_PATH}/inputs/videos/input2.mp4")
	tracker.addCamera("Floor2-main-playzone", 4, "Playzone", config.FRAME_CAPTURE_INTERVAL, f"{config.DATA_PATH}/inputs/videos/input3.mp4")
	tracker.printCamerasDetails()
	tracker.startCameras([1, 2, 3, 4])
	try:
	    while True:
	        tracker.collectResults()
	        time.sleep(1)
	except KeyboardInterrupt:
	    print("Stopping all camera feeds.")
	    for process in tracker.processes:
	        process.terminate()
	        process.join()
