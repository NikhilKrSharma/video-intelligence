import os
import config
import cv2
from qdrant_client import models, QdrantClient

def createRequiredPaths():
	for path in config.REQUIRED_PATHS:
		if os.path.exists(path):
			os.makedirs(path,exist_ok=True)

def save_image_with_bounding_boxes(image, face_locations, output_path,matches=None):
    # Convert the image to RGB format (OpenCV uses BGR by default)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # Draw bounding boxes
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(rgb_image, (left, top), (right, bottom), (0, 255, 0), 2)
    # print(matches)
    if matches:
        i=0
        for(top, right, bottom, left) in face_locations:
            # print(f"top: {top},bottom: {bottom},left: {left},right: {right}")
            font = 0.02*((bottom-top))
            cv2.putText(rgb_image,matches[i],(left+1,bottom),cv2.FONT_HERSHEY_PLAIN,font,(0, 100, 500),1)
            i+=1
    # Save the image
    cv2.imwrite(output_path, rgb_image)