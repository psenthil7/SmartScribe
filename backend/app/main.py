from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel # for data validation 
from typing import List, Optional 

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

@app.get("/api/notes") 
async def get_notes():
    """Get all notes (placeholder for now)"""
    return {"notes" : [], "message" : "No notes yet"}

@app.post("/api/notes")
async def create_note(note: NoteCreate):
    """Create a new note"""

    return {
        "id": 1,
        "title": note.title,
        "content": note.content,
        "message": "Note created successfully"
    }

@app.get(f"/api/notes/{note_id}")
async def get_note(note_id: int):
    """Get a specific note by ID"""

    return {
        "id": note_id,
        "title": f"Sample Note {note_id}",
        "content": "This is a sample note content",
        "message": "Note retrieved successfully"
    }

