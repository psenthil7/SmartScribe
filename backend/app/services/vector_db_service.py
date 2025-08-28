import chromadb 
from chromadb.config import Settings
from typing import List, Dict, Any

class VectorDBService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path = "./chroma_db")
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
    
