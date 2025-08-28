import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #db
    chroma_db_path: str = "./chroma_db"

    #uplod file
    upload_dir: str = "./uploads"
    max_file_size: int = 10 * 1024 * 1024 # 10mb
    allowed_extensions: list = [".jpg", ".jpeg", ".png", ".pdf"]

    #ML
    embedding_model: str = "all-MiniLM-L6-v2"
    max_text_length: int = 1000

    # API
    cors_origins: list = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
    
settings = Settings()