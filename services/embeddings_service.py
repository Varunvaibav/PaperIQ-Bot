from langchain.embeddings.cohere import CohereEmbeddings
import os

# Initialize embedding model
embedding_model = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=os.getenv("COHERE_API_KEY"), user_agent="my-app")

def generate_query_embedding(query):
    return embedding_model.embed_query(query)
