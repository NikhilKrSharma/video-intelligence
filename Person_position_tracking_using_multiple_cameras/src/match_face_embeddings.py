import face_recognition
import numpy as np
import cv2
import json
from save_embeddings import save_embeddings, save_image_with_bounding_boxes
import config
from qdrant_client import models, QdrantClient
import uuid

#connect to qdrant database
print("connecting to Qdrant database")
qdrantClient = QdrantClient(url=config.QDRANT_URL)
print("connected to Qdrant Successfully.")

def recognize_faces(image_path, camera_details={"camera_no":0, "zone_no":0, "zone_name":"Entrance"}):
    # Load the image
    image = face_recognition.load_image_file(image_path)
    # Find all face locations in the image
    face_locations = face_recognition.face_locations(image)
    # Find face encodings for the detected faces
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    # Load known embeddings
    # try:
    #     with open(embeddings_file, 'r') as f:
    #         if f.read().strip():  # Check if the file is not empty
    #             f.seek(0)
    #             known_embeddings_data = json.load(f)
    #         else:
    #             known_embeddings_data = []
    # except (json.JSONDecodeError, FileNotFoundError):
    #     known_embeddings_data = []
    
    # print(len(known_embeddings_data))
    
    # Convert known embeddings to numpy arrays
    # known_embeddings = [np.array(data["embedding"]) for data in known_embeddings_data]
    
    results = []
    matched_to=[]
    for i, unknown_encoding in enumerate(face_encodings):
        face_results = qdrantClient.search(
            collection_name=config.FACE_CLUSTER['NAME'],
            query_vector=unknown_encoding.tolist(),
            with_vectors=True,
            with_payload=True,
            limit=1
        ) 
        if face_results:
            print("found some faces in qdrant")
        # print(f"search result::: {search_result}")      
        # if known_embeddings:
        #     # Calculate similarity scores
        #     print(f"Calculating similarity score for {i}th face in input image and known embeddings:")
        #     similarity_scores = [calculate_similarity(unknown_encoding, known_encoding) for known_encoding in known_embeddings]
        #     for j, score in enumerate(similarity_scores):
        #         print(f"Similarity Score of face {i} with known id:{j}: {score}")
            
        #     # Find the highest similarity score
        #     max_score = max(similarity_scores)
        #     max_index = similarity_scores.index(max_score)
        #     print(max_score)


            if face_results[0].score>config.FACE_MATCHING_THRESHOLD:
                print("face matches")
                results.append(f"Face {i+1} matches with {face_results[0].id} with a similarity score of {face_results[0].score}")
                matched_to.append(face_results[0].id)
            else:
                new_id = uuid.uuid4()
                results.append(f"Face {i+1} is a new face with id {new_id}")
                matched_to.append(f"{new_id}")
                # print(f"{new_id}")
                print(f"Adding ::::::::::1 to {config.FACE_CLUSTER['NAME']}")
                print(f"length::::::::::::::::::::::::::::{len(unknown_encoding)}")
                new_face_data = {
                    "id": f"{new_id}",
                    "embedding": unknown_encoding.tolist(),
                    "face_location": face_locations[i],
                }
                # print(f"Adding {new_face_data} ::::::::::2")
                upsert_result=qdrantClient.upsert(
                    collection_name = config.FACE_CLUSTER['NAME'],
                    wait=True,
                    points=[models.PointStruct(id=f"{new_id}", vector=unknown_encoding.tolist(), payload=new_face_data)]
                )
                print(f"upsert_result::::::::::::{upsert_result}")
                
        else:
            new_id = uuid.uuid4()
            results.append(f"Face {i+1} is a new face with id {new_id}")
            matched_to.append(f"{new_id}")
            new_face_data = {
                "id": f"{new_id}",
                "embedding": unknown_encoding.tolist(),
                "location": face_locations[i],
                "camera_details":camera_details
            }
            print(new_id)
            print(f"Adding ::::::::::2 to {config.FACE_CLUSTER['NAME']}")
            print(f"length::::::::::::::::::::::::::::{len(unknown_encoding)}")
            upsert_result=qdrantClient.upsert(
                collection_name = config.FACE_CLUSTER['NAME'],
                wait=True,
                points=[models.PointStruct(id=f"{new_id}", vector=unknown_encoding.tolist(), payload=new_face_data)]
            )
            print(f"upsert_result::::::::::::{upsert_result}")
            
    
    # Save image with bounding boxes
    save_image_with_bounding_boxes(image, face_locations, f"{config.DATA_PATH}/temp/detected_{image_path.split('/')[-1]}", matches=matched_to)
    
    return results

def calculate_similarity(encoding1, encoding2):
    # Calculate the Euclidean distance between two encodings
    distance = np.linalg.norm(encoding1 - encoding2)
    # Convert distance to a similarity score (closer to 1 means more similar)
    similarity_score = 1 / (1 + distance)
    return similarity_score

# Example usage
if __name__=="__main__":

    results = recognize_faces(f"{config.DATA_PATH}/inputs/images/kohli1.jpg", "embeddings.json")
    for result in results:
        print(result)
