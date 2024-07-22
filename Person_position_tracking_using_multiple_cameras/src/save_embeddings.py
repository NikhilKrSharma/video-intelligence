import face_recognition
import numpy as np
import cv2
import json
import config
from qdrant_client import models, QdrantClient

#connect to qdrant database
qdrantClient = QdrantClient(url=config.QDRANT_URL)

def save_embeddings(image_path, output_file, camera_details={"camera_no":0,"zone_no":0,"zone_name":"Entrance"}):
    # Load the image
    image = face_recognition.load_image_file(image_path)
    # Find all face locations in the image
    face_locations = face_recognition.face_locations(image)
    # Find face encodings for the detected faces
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    # Save embeddings and corresponding face locations
    embeddings_data = []
    for i, encoding in enumerate(face_encodings):
        face_data = {
            "id": f"face_{i+1}",
            "embedding": encoding.tolist(),
            "face_location": face_locations[i],
            "camera_details": camera_details
        }
        embeddings_data.append(face_data)
    
    with open(output_file, 'w') as f:
        json.dump(embeddings_data, f)
    
    # Save image with bounding boxes
    save_image_with_bounding_boxes(image, face_locations, f"{config.DATA_PATH}/temp/known_image_with_boxes.jpg")

def save_image_with_bounding_boxes(image, face_locations, output_path,matches=None):
    # Convert the image to RGB format (OpenCV uses BGR by default)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # Draw bounding boxes
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(rgb_image, (left, top), (right, bottom), (0, 255, 0), 2)
    print(matches)
    if matches:
        i=0
        for(top, right, bottom, left) in face_locations:
            print(f"top: {top},bottom: {bottom},left: {left},right: {right}")
            font = 0.02*((bottom-top))
            cv2.putText(rgb_image,matches[i],(left+1,bottom),cv2.FONT_HERSHEY_PLAIN,font,(0, 100, 500),1)
            i+=1
    # Save the image
    cv2.imwrite(output_path, rgb_image)

# Example usage
if __name__  == "__main__":
    save_embeddings("data/inputs/images/kohli1.jpg", f"{config.DATA_PATH}/embeddings.json")
else:
    print("Hurray")
