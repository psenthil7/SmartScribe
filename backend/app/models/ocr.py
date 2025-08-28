from pydantic import BaseModel

class OCRResponse(BaseModel):
    filename: str
    extracted_text: str
    character_count: int

