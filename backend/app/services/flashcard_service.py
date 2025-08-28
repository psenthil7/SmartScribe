class FlashcardService:
    def generate_flashcards(self, content: str) -> List[Dict[str, str]]:
        # Placeholder, creating simple flashcards for now

        sentences = content.split('.')
        flashcards = []
        
        for i, sentence in enumerate(sentences[:5]): # limit to 5 flashcards
            if len(sentence.strip()) > 20:
                question = f"What is the main point about: {sentence[:50]}...?"
                answer = sentence.strip()
                flashcards.append({"question": question, "answer": answer})
        
        return flashcards