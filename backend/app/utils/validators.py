import re
from typing import List

def validate_text_content(text: str) -> bool:
    """Validate that text contains meaningful content"""
    if not text or len(text.strip()) < 50: 
        return False
    return True

def clean_text_for_embedding(text: str) -> str:
    """Clean text for better embedding generation"""

    cleaned = re.sub(r'\s+', ' ', text.strip())
    return cleaned

def validate_file_type(filename: str, allowed_extensions: List[str]) -> bool:
    """Validate file extension"""
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)
