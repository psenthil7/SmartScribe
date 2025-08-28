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
    
    # stores note with given parameters
    def store_notes(self, note_id: str, content: str, embedding: List[float], metadata: Dict[str, Any]):
        self.collection.add(
            embeddings = [embedding],
            documents = [content],
            metadatas = [metadata],
            ids = [note_id]
        )
    
    # searches similar note embeddings
    def search_similar(self, query_embedding: List[float], n_results: int = 5):
        results = self.collection.query(
            query_embeddings = [query_embedding],
            n_results = n_results
        )
        return results