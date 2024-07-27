from qdrant_client import QdrantClient
from qdrant_client import models
from qdrant_client.models import Distance, VectorParams
import config
import uuid

class Qdrant:
	def __init__(self,URL):
		self.url = URL
		self.client = QdrantClient(url=URL)

	
	def isCollectionExist(self,collection_name):
		# print(self.client.collection_exists(collection_name=collection_name))
		return self.client.collection_exists(collection_name=collection_name)


	def createCollection(self,collection_name):
		self.client.create_collection(
		    collection_name="faces",
		    vectors_config=VectorParams(size=128, distance=Distance.COSINE),
		)

	def save_embedding(self,unknown_encoding,face_location):
		try:
			new_id = uuid.uuid4()
			new_face_data = {
    	        "id": f"{new_id}",
    	        "embedding": unknown_encoding.tolist(),
    	        "face_location": face_location,
    	    }
			# print(f"{new_id}")
			print(f"Adding New face to {config.FACE_COLLECTION['NAME']} with encoding of length: {len(unknown_encoding)}")
			upsert_result=self.client.upsert(
    		    collection_name = config.FACE_COLLECTION['NAME'],
    		    wait=True,
    		    points=[models.PointStruct(id=f"{new_id}", vector=unknown_encoding.tolist(), payload=new_face_data)]
    		)
			# print(f"upsert_result::::::::::::{upsert_result}")
			# print(f"Inserted face_data: {new_face_data}")
			print("Embedding saved Successfully.")
			return new_id
		except Exception as e:
			print(f"Some Error in saving embeddings of new face : {e}")
			return -1

	def search_nearest_face_embeddings(self,unknown_encoding,k_nn=1):
		face_results = self.client.search(
    	    collection_name=config.FACE_COLLECTION['NAME'],
    	    query_vector=unknown_encoding.tolist(),
    	    with_vectors=True,
    	    with_payload=True,
    	    limit=k_nn
    	) 
		return face_results
