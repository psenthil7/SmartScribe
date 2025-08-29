import requests
import json
from typing import List, Dict, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

from app.config import settings

class CerebrasService:
    def __init__(self, api_key: Optional[str] = None, model_name: str = None):
        """
        Initialize Cerebras service
        
        Args:
            api_key: Cerebras API key (if using their cloud service)
            model_name: Hugging Face model name for Cerebras models
        """
        self.api_key = api_key or settings.CEREBRAS_API_KEY
        self.model_name = model_name or settings.CEREBRAS_MODEL_NAME
        self.tokenizer = None
        self.model = None
        
        # Initialize model and tokenizer
        self._load_model()
    
    def _load_model(self):
        """Load the Cerebras model and tokenizer"""
        try:
            print(f"Loading Cerebras model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True
            )
            print("Cerebras model loaded successfully!")
        except Exception as e:
            print(f"Error loading Cerebras model: {e}")
            # Fallback to API if model loading fails
            self.model = None
            self.tokenizer = None
    
    def generate_answer(self, query: str, context: str, max_length: int = None) -> str:
        """
        Generate an answer using Cerebras model
        
        Args:
            query: The user's question
            context: Relevant context from vector search
            max_length: Maximum length of generated response
            
        Returns:
            Generated answer
        """
        if self.model is None or self.tokenizer is None:
            return self._generate_answer_api(query, context)
        
        # Use configuration defaults
        max_length = max_length or settings.CEREBRAS_MAX_LENGTH
        temperature = settings.CEREBRAS_TEMPERATURE
        
        # Create prompt
        prompt = self._create_prompt(query, context)
        
        try:
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part (remove the prompt)
            generated_text = response[len(prompt):].strip()
            
            return generated_text if generated_text else "I couldn't generate a specific answer based on the provided context."
            
        except Exception as e:
            print(f"Error generating with local model: {e}")
            return self._generate_answer_api(query, context)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create a prompt for the Cerebras model"""
        prompt = f"""Based on the following context, please answer the question.

Context:
{context}

Question: {query}

Answer:"""
        return prompt
    
    def _generate_answer_api(self, query: str, context: str) -> str:
        """
        Fallback method using Cerebras API (if available)
        This is a placeholder - you would need to implement based on Cerebras API documentation
        """
        # Placeholder implementation
        return f"Based on the context provided, here's what I found: {query} - The relevant information from your notes includes: {context[:200]}..."
    
    def generate_flashcards(self, content: str, num_cards: int = 5) -> List[Dict]:
        """
        Generate flashcards from content using Cerebras
        
        Args:
            content: The note content
            num_cards: Number of flashcards to generate
            
        Returns:
            List of flashcard dictionaries
        """
        if self.model is None or self.tokenizer is None:
            return self._generate_flashcards_simple(content, num_cards)
        
        try:
            # Create prompt for flashcard generation
            prompt = f"""Generate {num_cards} flashcards from the following content. 
            Format each flashcard as: Question: [question] Answer: [answer]

            Content:
            {content}

            Flashcards:"""
            
            # Tokenize and generate
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=1024,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            generated_text = response[len(prompt):].strip()
            
            # Parse flashcards from generated text
            flashcards = self._parse_flashcards(generated_text, num_cards)
            
            return flashcards
            
        except Exception as e:
            print(f"Error generating flashcards with model: {e}")
            return self._generate_flashcards_simple(content, num_cards)
    
    def _generate_flashcards_simple(self, content: str, num_cards: int) -> List[Dict]:
        """Simple flashcard generation without AI model"""
        sentences = content.split('.')
        flashcards = []
        
        for i, sentence in enumerate(sentences[:num_cards]):
            if len(sentence.strip()) > 20:
                words = sentence.strip().split()
                if len(words) > 3:
                    question = f"What is {words[0]}?"
                    answer = sentence.strip()
                    flashcards.append({
                        "question": question,
                        "answer": answer,
                        "context": content[:100] + "..."
                    })
        
        return flashcards
    
    def _parse_flashcards(self, text: str, num_cards: int) -> List[Dict]:
        """Parse flashcards from generated text"""
        flashcards = []
        lines = text.split('\n')
        
        current_question = ""
        current_answer = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith("Question:"):
                if current_question and current_answer:
                    flashcards.append({
                        "question": current_question,
                        "answer": current_answer,
                        "context": ""
                    })
                current_question = line.replace("Question:", "").strip()
            elif line.startswith("Answer:"):
                current_answer = line.replace("Answer:", "").strip()
        
        # Add the last flashcard
        if current_question and current_answer:
            flashcards.append({
                "question": current_question,
                "answer": current_answer,
                "context": ""
            })
        
        return flashcards[:num_cards]
