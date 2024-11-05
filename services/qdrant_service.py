from qdrant_client import QdrantClient
from config.config import QDRANT_URL, QDRANT_API_KEY
from services.embeddings_service import generate_query_embedding

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    https=True,
    prefer_grpc=True
)

def retrieve_relevant_docs(query):
    query_embedding = generate_query_embedding(query)
    search_result = qdrant_client.search(
        collection_name="asapp_hackathon",
        query_vector=query_embedding,
        limit=5
    )
    return search_result
