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

# structr
class Note(BaseModel):
