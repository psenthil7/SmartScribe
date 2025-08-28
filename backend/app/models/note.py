from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    title: str
    content: str
    filename: Optional[str] = None

class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    filename: Optional[str] = None
    created_at: datetime
    