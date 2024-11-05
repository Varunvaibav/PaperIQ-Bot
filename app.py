import streamlit as st
from services.cohere_service import generate_answer
from services.qdrant_service import retrieve_relevant_docs
from services.utils import extract_filename, get_metadata_by_filename, get_image_data_by_pdf_file, display_image

st.title("PapersIQ")

st.write("Ask questions about research papers, and the bot will retrieve answers based on the available data.")

query = st.text_input("Ask a question:")
if query:
    response = generate_answer(query)
    st.write(response)