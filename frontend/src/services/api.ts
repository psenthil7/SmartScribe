import axios from 'axios';
import { 
  UploadResponse, 
  OCRResponse, 
  Note, 
  NoteCreate, 
  SearchResponse, 
  RAGResponse, 
  FlashcardResponse,
  EmbeddingResponse 
} from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// File upload
export const uploadFile = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post<UploadResponse>('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// OCR processing
export const processOCR = async (filename: string): Promise<OCRResponse> => {
  const response = await api.post<OCRResponse>(`/process-ocr/${filename}`);
  return response.data;
};

// Notes management
export const createNote = async (note: NoteCreate): Promise<Note> => {
  const response = await api.post<Note>('/notes', note);
  return response.data;
};

export const getNotes = async (): Promise<{ notes: Note[] }> => {
  const response = await api.get<{ notes: Note[] }>('/notes');
  return response.data;
};

export const getNote = async (noteId: string): Promise<Note> => {
  const response = await api.get<Note>(`/notes/${noteId}`);
  return response.data;
};

// Search functionality
export const searchNotes = async (query: string, nResults: number = 3): Promise<SearchResponse> => {
  const response = await api.post<SearchResponse>('/search', { query, n_results: nResults });
  return response.data;
};

// RAG search with Cerebras
export const ragSearch = async (query: string, nResults: number = 3): Promise<RAGResponse> => {
  const response = await api.post<RAGResponse>('/rag-search', { query, n_results: nResults });
  return response.data;
};

// Embeddings
export const generateEmbeddings = async (text: string): Promise<EmbeddingResponse> => {
  const response = await api.post<EmbeddingResponse>('/generate-embeddings', { text });
  return response.data;
};

// Store note with embeddings
export const storeNoteWithEmbeddings = async (note: NoteCreate): Promise<{ message: string; note_id: string }> => {
  const response = await api.post<{ message: string; note_id: string }>('/store-note-with-embeddings', note);
  return response.data;
};

// Flashcard generation
export const generateFlashcards = async (noteId: string): Promise<FlashcardResponse> => {
  const response = await api.post<FlashcardResponse>('/generate-flashcards', { note_id: noteId });
  return response.data;
};

export const generateFlashcardsFromSearch = async (query: string, nResults: number = 3, numCards: number = 5): Promise<FlashcardResponse> => {
  const response = await api.post<FlashcardResponse>('/generate-flashcards-from-search', { 
    query, 
    n_results: nResults, 
    num_cards: numCards 
  });
  return response.data;
};

export default api; 