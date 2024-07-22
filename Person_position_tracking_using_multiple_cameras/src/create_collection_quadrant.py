from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
client = QdrantClient(url="http://localhost:6333")


client.create_collection(
    collection_name="faces",
    vectors_config=VectorParams(size=128, distance=Distance.COSINE),
)