from typing import List, Dict
from app.services.cerebras_service import CerebrasService

class FlashcardService:
    def __init__(self):
        self.cerebras_service = CerebrasService()
    
    def generate_flashcards(self, content: str, num_cards: int = 5) -> List[Dict]:
        """Generate flashcards from content using Cerebras"""
        return self.cerebras_service.generate_flashcards(content, num_cards)
    
    def generate_flashcards_from_notes(self, note_ids: List[str], num_cards: int = 5) -> List[Dict]:
        """Generate flashcards from multiple notes"""
        # This would need to fetch notes from your database
        # For now, return empty list
        return []