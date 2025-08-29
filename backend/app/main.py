from fastapi import FastAPI, HTTPException, UploadFile, File 
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel # for data validation 
from typing import List, Dict
import os
import uuid
import cv2
import pytesseract
from PIL import Image
import numpy as np 
from app.models import NoteCreate, NoteResponse, OCRResponse, UploadResponse
from datetime import datetime
from app.services.embedding_service import EmbeddingService
from app.services.vector_db_service import VectorDBService
from app.services.flashcard_service import FlashcardService
from app.services.rag_service import RAGService

app = FastAPI(title="SmartScribe", version="1.0.0")

# configuring CORS middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], #requests from React frontend can be made to the backend 
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

# retrieves all notes - REMOVED DUPLICATE

# create note request - REMOVED DUPLICATE

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
    if not os.path.exists(upload_dir):
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

# OCR processing 
@app.post("/api/process-ocr/{filename}")
async def process_ocr(filename: str):
    """Processes uploaded file with OCR to extract text"""

    # creates path to uploaded file in uploads directory
    upload_dir = "uploads"
    file_path = os.path.join(upload_dir, filename)

    # check if file exists 
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    try:
        file_extension = os.path.splitext(filename.lower())[1]

        if file_extension == '.pdf':
            try:
                from pdf2image import convert_from_path
            except ImportError:
                raise HTTPException(
                    status_code=500, 
                    detail="PDF processing requires pdf2image. Install with: pip install pdf2image"
                )

            # convert pdf to images
            images = convert_from_path(file_path)
            all_text = ""

            # Process each page
            for i, image in enumerate(images):
                # Convert PIL image to OpenCV format
                opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                # Convert to grayscale
                gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
                denoised = cv2.medianBlur(gray, 3)
                _, threshold = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # extract text w tesseract
                text = pytesseract.image_to_string(threshold)
                all_text += f"\n--- Page {i+1} ---\n\n{text}"
            
            cleaned_text = all_text.strip()

        else: 
            # read image with open cv
            image = cv2.imread(file_path)
            if image is None:
                raise HTTPException(status_code=400, detail=f"Invalid image file")
        
            # grayscale so its easier for OCR + preprocessing 
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            denoised = cv2.medianBlur(gray, 3)
            _, threshold = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            #extract text w tesseract
            text = pytesseract.image_to_string(threshold)
            cleaned_text = text.strip() # clean any whitespace

        # Return statement for both PDF and image processing
        return {
            "filename": filename,
            "extracted_text": cleaned_text,
            "confidence": "OCR processing completed",
            "character_count": len(cleaned_text)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

notes_db = [] # for in memory storage

# creates notee
@app.post("/api/notes", response_model=NoteResponse)
async def create_note(note: NoteCreate):
    note_id = str(uuid.uuid4())
    new_note = NoteResponse(
        id = note_id,
        title = note.title, 
        content = note.content,
        filename = note.filename,
        created_at = datetime.now()
    )
    notes_db.append(new_note.dict())
    return new_note
    
@app.get("/api/notes")
async def get_notes():
    return {"notes": notes_db}

embedding_service = EmbeddingService()

@app.post("/api/generate-embeddings")
async def generate_embeddings(text: str):
    embedding = embedding_service.generate_embeddings(text)
    return {
        "embedding": embedding,
        "dimensions": len(embedding)
    }


vector_db = VectorDBService()

@app.post("/api/store-note-with-embeddings")
async def store_note_with_embeddings(note: NoteCreate):
    # convert text to embedding 
    embedding = embedding_service.generate_embeddings(note.content)
    
    # store in vector db
    note_id = str(uuid.uuid4())
    metadata = {"title": note.title, "filename": note.filename}
    vector_db.store_notes(note_id, note.content, embedding, metadata)

    return {"message": "Note stored with embeddings", "note_id": note_id}

@app.post("/api/search")
async def search_notes(query: str, n_results: int = 3):
    # create embedding for query
    query_embedding = embedding_service.generate_embeddings(query)

    # search for similar in vector db
    results = vector_db.search_similar(query_embedding, n_results)

    return {
        "query": query,
        "results": results
    }

flashcard_service = FlashcardService()

@app.post("/api/generate-flashcards")
async def generate_flashcards(note_id: str):

    # Find note in database
    note = next((n for n in notes_db if n["id"] == note_id), None)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # create flashcards
    flashcards = flashcard_service.generate_flashcards(note["content"])

    return {
        "note_id": note_id,
        "flashcards": flashcards
    }

# Initialize RAG service with Cerebras
rag_service = RAGService()

@app.post("/api/rag-search")
async def rag_search(query: str, n_results: int = 3):
    """Search with RAG using Cerebras for intelligent answers"""
    try:
        result = rag_service.search_with_context(query, n_results)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG search failed: {str(e)}")

@app.post("/api/generate-flashcards-from-search")
async def generate_flashcards_from_search(query: str, n_results: int = 3, num_cards: int = 5):
    """Generate flashcards from search results using Cerebras"""
    try:
        result = rag_service.generate_flashcards_from_search(query, n_results, num_cards)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Flashcard generation failed: {str(e)}")

