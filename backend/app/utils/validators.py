import re
from typing import List

def validate_text_content(text: str) -> bool:
    """Validate that text contains meaningful content"""
    if not text or len(text.strip()) < 50: 
        return False
    return True

