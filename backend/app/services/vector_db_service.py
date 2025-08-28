import chromadb 
from chromadb.config import Settings
from typing import List, Dict, Any

class VectorDBService:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet", # uses fst parquet file format
            persist_directory="./chroma_db" # save to folder
        ))
        self.collection = self.client.get_or_create_collection("notes")