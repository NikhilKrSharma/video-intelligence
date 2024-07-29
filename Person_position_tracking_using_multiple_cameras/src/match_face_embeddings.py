import face_recognition
import numpy as np
import cv2
import json
from utils import  save_image_with_bounding_boxes
# from utils import save_embedding, search_nearest_face_embeddings
import config
import uuid
from qdrant import Qdrant
qdrantHandler = Qdrant(config.QDRANT_URL)
if not qdrantHandler.isCollectionExist(config.FACE_COLLECTION['NAME']):
    qdrantHandler.createCollection(config.FACE_COLLECTION['NAME'])

def recognize_faces(image_path, camera_details={"camera_no":0, "zone_no":0, "zone_name":"Entrance"}):
    # Load the image
    image = face_recognition.load_image_file(image_path)
    # Find all face locations in the image
    face_locations = face_recognition.face_locations(image)
    # Find face encodings for the detected faces
    face_encodings = face_recognition.face_encodings(image, face_locations)  
    results = []
    matched_to=[]
    for i, unknown_encoding in enumerate(face_encodings):
        face_results = qdrantHandler.search_nearest_face_embeddings(unknown_encoding,k_nn=1)
        # if search results is not empty i.e. there exist some entry in db
        if face_results:
            # if face matched
            if face_results[0].score>config.FACE_MATCHING_THRESHOLD:
                # print("face matches")
                results.append(f"Face {i+1} in Camera{camera_details['camera_no']} matches with {face_results[0].id} with a similarity score of {face_results[0].score}")
                matched_to.append(face_results[0].id)
            else:
                new_id = qdrantHandler.save_embedding(unknown_encoding,face_locations[i])
                if new_id!=-1:
                    results.append(f"Face {i+1} in Camera{camera_details['camera_no']} is a new face with id {new_id}")
                    #As this is a new face, match it to itself.
                    matched_to.append(f"{new_id}")
        # if search result is empty        
        else:
            new_id = qdrantHandler.save_embedding(unknown_encoding,face_locations[i])
            if new_id!=-1:
                results.append(f"Face {i+1} in Camera{camera_details['camera_no']} is a new face with id {new_id}")
                matched_to.append(f"{new_id}")
            
    
    # Save image with bounding boxes
    save_image_with_bounding_boxes(image, face_locations, f"{config.DATA_PATH}/temp/detected_{image_path.split('/')[-1]}", matches=matched_to) 
    return results


# Example usage
if __name__=="__main__":
    results = recognize_faces(f"{config.DATA_PATH}/inputs/images/kohli1.jpg", camera_details={"camera_no":0, "zone_no":0, "zone_name":"Entrance"})
    for result in results:
        print(result)
