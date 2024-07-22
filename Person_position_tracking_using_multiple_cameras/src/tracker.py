from camera import Camera
from match_face_embeddings import recognize_faces
import config

class Tracker:
    def __init__(self, tracker_name="Tracker1", max_camera_count=config.MAX_CAMERA_COUNT):
        self.max_camera_count = max_camera_count
        self.tracker_name=tracker_name
        self.cameras = []


    def addCamera(self,location,zone_no,zone_name,interval,source):
        camera_no = len(self.cameras)+1
        newCamera = Camera(camera_no,location,zone_no,zone_name,interval,source)
        self.cameras.append(newCamera)
    
    # def removeCamera(camera_no):
    #     cameras = [camera for camera in cameras if camera.camera_no is not camera_no]

    def startCameras(self, cameras_to_start):
        for camera in self.cameras:
            camera.release()
        for camera_no in cameras_to_start:
            print(f"starting camera {camera_no}")
            self.cameras[camera_no-1].startCapturing()

    def printCamerasDetails(self):
        for camera in self.cameras:
            print(camera.camera_no)
            print(camera.zone_name)


if __name__=="__main__":
    tracker = Tracker()
    tracker.addCamera("Enterance",1,"Main Enterance",config.FRAME_CAPTURE_INTERVAL,0)
    # tracker.addCamera("Floor1-center-left",2,"Fitness Club",config.FRAME_CAPTURE_INTERVAL,f"{config.DATA_PATH}/inputs/videos/Two_ankers.mp4")
    tracker.printCamerasDetails()
    tracker.startCameras([1])

    

