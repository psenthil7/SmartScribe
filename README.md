# SmartScribe - Handwritten Notes to Smart Flashcards

A full-stack web application that converts handwritten notes to text via OCR, generates embeddings, stores them in Chroma vector database, and enables semantic search and flashcard generation.


### Phase 1: Foundation
- [ ] Project structure setup
- [ ] Basic FastAPI backend
- [ ] Simple React frontend
- [ ] Docker containerization

### Phase 2: Core Features
- [ ] File upload functionality
- [ ] OCR integration
- [ ] Text processing and storage

### Phase 3: AI Integration
- [ ] Embedding generation
- [ ] Chroma vector database setup
- [ ] Semantic search implementation

### Phase 4: Advanced Features
- [ ] Flashcard generation
- [ ] User authentication
- [ ] Performance optimization

## Project Structure

```
smartscribe/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── api/           # API routes
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React application
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml      # Multi-container setup
└── README.md
```

## Getting Started

1. Clone this repository
2. Follow the learning path step by step
3. Each phase builds upon the previous one
4. Complete the exercises before moving to the next phase

## Technologies Used

- **Backend**: FastAPI, Python
- **Frontend**: React, JavaScript
- **Database**: Chroma (Vector Database)
- **AI**: OCR (Tesseract/Google Vision), Embeddings (OpenAI/sentence-transformers)
- **Containerization**: Docker
- **File Processing**: Pillow, OpenCV