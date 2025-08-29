// Note types
export interface Note {
  id: string;
  title: string;
  content: string;
  filename?: string;
  created_at: string;
}

export interface NoteCreate {
  title: string;
  content: string;
  filename?: string;
}

// Upload types
export interface UploadResponse {
  message: string;
  filename: string;
  original_name: string;
  file_path: string;
  file_type: string;
  size_bytes: number;
}

// OCR types
export interface OCRResponse {
  filename: string;
  extracted_text: string;
  confidence: string;
  character_count: number;
}

// Combined upload and OCR result
export interface FileProcessResult {
  message: string;
  filename: string;
  original_name: string;
  file_path: string;
  file_type: string;
  size_bytes: number;
  extracted_text: string;
  confidence: string;
  character_count: number;
}

// Search types
export interface SearchResult {
  id: string;
  content: string;
  metadata: Record<string, any>;
  distance: number;
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
}

// RAG types
export interface RAGResponse {
  answer: string;
  sources: SearchResult[];
  context: string;
}

// Flashcard types
export interface Flashcard {
  question: string;
  answer: string;
  context?: string;
}

export interface FlashcardResponse {
  note_id?: string;
  flashcards: Flashcard[];
  sources?: SearchResult[];
  query?: string;
}

// Embedding types
export interface EmbeddingResponse {
  embedding: number[];
  dimensions: number;
}
