import base64
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient
import certifi
from config.config import MONGO_DB_URL
import streamlit as st

meta_data = pd.read_csv('./data/meta_data.csv')
image_df = pd.read_csv('./data/data_images_preprocessed_v1.csv')

client = MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
db = client["asapp"]
collection = db["images_v1"]

def extract_filename(path):
    return path.split('/')[-1]

def get_metadata_by_filename(filename):
    metadata_row = meta_data[meta_data['Filename'] == filename]
    if not metadata_row.empty:
        return metadata_row.iloc[0].to_dict()
    return {}

def get_image_data_by_pdf_file(pdf_file):
    return image_df[image_df['pdf_file'] == pdf_file]['image_data'].values

def extract_image_path(image_data):
    if isinstance(image_data, str) and "<img file_path=" in image_data:
        start_index = image_data.find("<img file_path=") + len("<img file_path=(")
        end_index = image_data.find(")", start_index)  # Stop at the closing parenthesis
        #print(image_data[start_index:end_index].strip('\'"'))
        return image_data[start_index:end_index].strip('\'"')
    return None


def display_image(file_name, image_data=None):
    image_data = collection.find_one({"file_name": file_name})
    if image_data:
        # Decode the base64 encoded image
        encoded_val = image_data["encoded_val"]
        img_data = base64.b64decode(encoded_val)

        # Display the image in Streamlit
        image = Image.open(BytesIO(img_data))
        st.image(image, use_column_width=True)
    else:
        st.write("Image not found in the database.")
