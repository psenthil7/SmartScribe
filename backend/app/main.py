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

    # creates upload directory if it doesn't already exist
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # creates a unique filename w uuid
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename) # combines folder and fileName into full path

    # save the file
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save fule: {str(e)}")

    # get file type for processing
    file_type = get_file_type(file.filename)

    return {
        "message": "File uploaded successfully",
        "filename": unique_filename,
        "original_name": file.filename,
        "file_path": file_path,
        "file_type": file_type,
        "size_bytes": len(content)
    }

@app.get("/api/files")
async def list_uploaded_files():
    """List all uploaded files with their types"""

    upload_dir = "uploads"

    # if directory doesn't exist, return empty value
    if not os.path.exists(upload_dir)
        return {"files": []}

    files = []
    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        if os.path.isfile(file_path):
            file_type = get_file_type(filename)
            file_size = os.path.getsize(file_path)
            files.append({
                "filename": filename,
                "path": file_path,
                "type": file_type,
                "size_bytes": file_size
            })
    
    return {"files": files}