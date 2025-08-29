from typing import List, Dict
from app.services.vector_db_service import VectorDBService
from app.services.embedding_service import EmbeddingService
from app.services.cerebras_service import CerebrasService

class RAGService:
    def __init__(self):
        self.vector_db = VectorDBService()
        self.embedding_service = EmbeddingService()
        self.cerebras_service = CerebrasService()
        
    def search_with_context(self, query: str, n_results: int = 3) -> Dict:
        """Search with RAG - retrieve relevant context and generate answer using Cerebras"""
        
        # Get relevant documents
        results = self.vector_db.search_similar(query, n_results)
        
        if not results:
            return {"answer": "No relevant information found.", "sources": []}
        
        # Build context from retrieved documents
        context = "\n\n".join([doc["content"] for doc in results])
        
        # Generate answer using Cerebras
        answer = self.cerebras_service.generate_answer(query, context)
        
        return {
            "answer": answer,
            "sources": results,
            "context": context
        }
    
    def generate_flashcards_from_search(self, query: str, n_results: int = 3, num_cards: int = 5) -> Dict:
        """Generate flashcards based on search results"""
        
        # Get relevant documents
        results = self.vector_db.search_similar(query, n_results)
        
        if not results:
            return {"flashcards": [], "message": "No relevant information found."}
        
        # Combine content from all results
        combined_content = "\n\n".join([doc["content"] for doc in results])
        
        # Generate flashcards using Cerebras
        flashcards = self.cerebras_service.generate_flashcards(combined_content, num_cards)
        
        return {
            "flashcards": flashcards,
            "sources": results,
            "query": query
        } 