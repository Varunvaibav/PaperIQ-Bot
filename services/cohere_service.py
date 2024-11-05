from cohere import Client
import os
import pandas as pd
from services.qdrant_service import retrieve_relevant_docs
from services.utils import extract_filename, get_metadata_by_filename,get_image_data_by_pdf_file,extract_image_path,display_image
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Initialize Cohere client
cohere_client = Client(api_key=os.getenv("COHERE_API_KEY"))
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_top_k_similar(query, column, k=2):
    # Convert the column to a list of values
    values = column.tolist()
    
    # Filter out NaN or non-string values
    values = [val for val in values if isinstance(val, str) and pd.notna(val)]
    
    # If values is empty, return an empty list
    if not values:
        print("")
        return []
    
    # Get the embeddings for both the query and the column values
    query_embedding = model.encode([query])
    values_embeddings = model.encode(values)
    
    # Ensure embeddings are 2D before computing cosine similarity
    if values_embeddings.size == 0:
        return []
    
    # Compute cosine similarity between the query and the values
    similarities = cosine_similarity(query_embedding, values_embeddings)[0]
    
    # Create a DataFrame to hold values and their similarity scores
    similarity_df = pd.DataFrame({'value': values, 'similarity': similarities})
    
    # Sort by similarity score in descending order and get the top k
    top_k = similarity_df.sort_values(by='similarity', ascending=False).head(k)
    
    # Return as a list of tuples (value, similarity_score)
    return list(zip(top_k['value'], top_k['similarity']))

def generate_answer(query):
    # Step 1: Retrieve relevant documents
    retrieved_docs = retrieve_relevant_docs(query)

    # Extract document paths and file names
    docs_names = [doc.payload['metadata']['source'] for doc in retrieved_docs]

    # Prepare context and metadata for the prompt
    context = "\n\n".join([doc.payload.get("content", "") or doc.payload.get("text", "") for doc in retrieved_docs])
    metadata_info = []
    for doc_name in docs_names:
        filename = extract_filename(doc_name)
        metadata = get_metadata_by_filename(filename)
        if metadata:
            metadata_string = f"Title: {metadata.get('Title')}\nAuthor: {metadata.get('Author')}\nAbstract: {metadata.get('Abstract')}"
            metadata_info.append(metadata_string)
    
    # Include metadata in the context
    metadata_context = "\n\n".join(metadata_info)

    # Use the modified prompt
    prompt = (
        f"You are an advanced research assistant and can provide answers using both text and image content. "
        f"If images are available for the requested information, include them without mentioning if any are missing. "
        f"Here is the context and metadata from relevant research papers:\n\n{context}\n\n{metadata_context}\n\n"
        f"Question: {query}\n\nAnswer:"
    )
    
    response = cohere_client.generate(
        model='command',
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )

    # Flag to check if any images were found and displayed
    images_found = False

    if "image" in query.lower() or "images" in query.lower():
        related_images = []
        for doc_name in docs_names:
            filename = extract_filename(doc_name)
            images_summary = get_image_data_by_pdf_file(filename)
            images = get_top_k_similar(query, pd.Series(images_summary))  # Ensure images is a pandas Series
            for image_data in images:
                if pd.notna(image_data):  # Check if the image_data is not NaN
                    image_path = extract_image_path(image_data[0])
                    if image_path:
                        related_images.append(image_path)

        # Display any related images if found
        if related_images:
            images_found = True
            for image_path in related_images:
                print(f"Displaying image: {image_path}")
                display_image(image_path)

    # If images were found, remove any comments about missing images from the response text
    if images_found:
        response_text = response.generations[0].text.strip()
        response_text = response_text.replace(
            "I'm sorry, I can't retrieve images for this research paper, as it is not related to this topic.", ""
        )
        return response_text.strip()
    
    return response.generations[0].text.strip()
