# PaperIQ-Bot

## Overview
The **PaperIQ-Bot** is a scalable and maintainable solution built to provide users with accurate answers to questions about research papers. It utilizes a combination of **Cohere** for natural language understanding, **Qdrant** for efficient vector-based retrieval, and **Streamlit** for a user-friendly interface. Users can interact with the bot, ask questions, and receive answers based on the content of indexed research papers.

## Features
- **Question Answering**: Retrieves relevant documents from a Qdrant vector store and generates precise answers.
- **Metadata Utilization**: Provides detailed context by including metadata (title, author, abstract) to enhance answers.
- **Image Retrieval**: Supports the display of diagrams and images from research papers.
- **Streamlit Interface**: A simple and interactive frontend for seamless user interaction.
- **Scalability**: Easily scales to support a large dataset of research papers.

## Tech Stack
- **Python**: The core language used for development.
- **Cohere**: For generating embeddings and answering questions using a pre-trained language model.
- **Qdrant**: Vector database to store and retrieve embeddings.
- **Streamlit**: Frontend interface for easy interaction with the bot.
- **MongoDB**: Storage for images and metadata.

## Getting Started

### Prerequisites
Make sure you have the following installed:
- Python 3.8 or above
- Required Python packages:
  - `qdrant-client`
  - `cohere`
  - `langchain`, `langchain-openai`, `langchain-experimental`, etc.
  - `fastembed`, `sentence-transformers`
  - `PyPDF2`, `pypdf`
  - `pymongo`, `certifi`
  - `streamlit`
  - `pandas`

Install all required packages by running:
```bash
pip install -r requirements.txt
```

### Running the Application
Run the Streamlit app with:
```bash
streamlit run app.py
```

## File Structure
```
.
├── app.py                      # Main entry point for the Streamlit app
├── services/
│   ├── cohere_service.py       # Handles Cohere API interactions
│   ├── qdrant_service.py       # Functions for retrieving data from Qdrant
│   ├── mongo_service.py        # Functions for interacting with MongoDB
│   └── utils.py                # Utility functions for data handling
├── data/
│   ├── meta_data.csv           # CSV containing research paper metadata
│   └── data_images_preprocessed_v1.csv  # CSV for image data association
├── requirements.txt            # Required Python packages
└── README.md                   # Project README file
```

## Usage

### Interacting with the Q&A Bot
1. **Start the app**: After running the Streamlit command, the app will open in your browser.
2. **Ask Questions**: Type your question in the input field and hit enter. The bot will retrieve relevant documents and provide an answer.
3. **Image Queries**: If your question relates to images or diagrams, the bot will attempt to display relevant images from the research papers.

## Example Questions
- "What are the basics of Machine Learning?"
- "Can you show me a diagram of a neural network?"
- "Who authored the paper on deep learning?"

## Future Enhancements
- **Improved Image Retrieval**: Enhance the bot to provide more precise image retrieval based on the context of the query.
- **Document Upload**: Allow users to upload their own PDFs for ad-hoc question answering.
- **Multi-Language Support**: Expand to support queries in multiple languages.
