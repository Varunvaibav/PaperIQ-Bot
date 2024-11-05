from pymongo import MongoClient
import certifi
from config.config import MONGO_DB_URL

# Initialize MongoDB client
client = MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
db = client["asapp"]
collection = db["images_v1"]

def get_image_data_by_pdf_file(pdf_file):
    return collection.find({"pdf_file": pdf_file})
