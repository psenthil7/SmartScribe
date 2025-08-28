from fastapi import FastAPI, HTTPException, UploadFile, File 
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel # for data validation 
from typing import List
import os
import uuid

app = FastAPI(title="SmartScribe", version="1.0.0")

# configuring CORS middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000"], #requests from React frontend can be made to the backend 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
 ) 

 # Root endpoint
@app.get("/") 
async def root():
    return {'message': 'Welcome to SmartScribe API'}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# structure for creating a note
class NoteCreate(BaseModel):
    title: str
    content: str

# structure for what server sends back
class Note(BaseModel):
    id: int
    title: str
    content: str

# retrieves all notes
@app.get("/api/notes") 
async def get_notes():
    """Get all notes (placeholder for now)"""
    return {"notes" : [], "message" : "No notes yet"}

# create note request
@app.post("/api/notes")
async def create_note(note: NoteCreate):
    """Create a new note"""

    return {
        "id": 1,
        "title": note.title,
        "content": note.content,
        "message": "Note created successfully"
    }

# get request for a specific note
@app.get("/api/notes/{note_id}")
async def get_note(note_id: int):
    """Get a specific note by ID"""

    return {
        "id": note_id,
        "title": f"Sample Note {note_id}",
        "content": "This is a sample note content",
        "message": "Note retrieved successfully"
    }

ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.tiff', '.bmp'],
    'pdf': ['.pdf'],
    'document': ['.doc', '.docx'] # optional for typed notes
}

# check if file type is allowed
def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    ext = os.path.splitext(filename.lower())[1]
    return any(ext in extensions for extensions in ALLOWED_EXTENSIONS.values())

def get_file_type(filename: str) -> str:
    """Get the type of file based on extension"""
    ext = os.path.splitext(filename.lower())[1]
    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return file_type
    return "unknown"

@app.post("/api/upload")
async def upload_note_file(file: UploadFile = File(...)):
    """Upload a handwritten note file (image, PDF, etc.)"""

    # Validate file type
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed."
        )
