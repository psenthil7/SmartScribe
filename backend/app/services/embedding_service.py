from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2') # model for embeddings

    def generate_embeddings(self, text: str):
        return self.model.encode(text).tolist() # creates embeddigns for signle text
    
    def generate_embeddings_batch(self, texts: list):
        return self.model.encode(texts).tolist()  # creates embeddings for list of text

    