import os
from typing import List

class Settings:
    # API Configuration
    API_TITLE = "SmartScribe"
    API_VERSION = "1.0.0"
    CORS_ORIGINS = ["http://localhost:3000"]
    
    # File Upload Configuration
    UPLOAD_DIR = "uploads"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {
        'image': ['.jpg', '.jpeg', '.png', '.tiff', '.bmp'],
        'pdf': ['.pdf'],
        'document': ['.doc', '.docx']
    }
    
    # OCR Configuration
    TESSERACT_CONFIG = '--oem 3 --psm 6'
    
    # Vector Database Configuration
    CHROMA_DB_PATH = "./chroma_db"
    COLLECTION_NAME = "notes"
    
    # Embedding Configuration
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    MAX_TEXT_LENGTH = 10000
    
    # Cerebras Configuration
    CEREBRAS_MODEL_NAME = "cerebras/btlm-3b-8k-base"
    CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY", None)
    CEREBRAS_MAX_LENGTH = 512
    CEREBRAS_TEMPERATURE = 0.7
    
    # RAG Configuration
    DEFAULT_SEARCH_RESULTS = 3
    DEFAULT_FLASHCARD_COUNT = 5
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = ENVIRONMENT == "development"

# Global settings instance
settings = Settings()