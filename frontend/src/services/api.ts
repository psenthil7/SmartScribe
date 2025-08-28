import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        }
    });
    return response.data;
}

export const processOCR = async (filename: string) => {
    const response = await api.post(`/process-ocr/${filename}`);
    return response.data;
};

export const createNote = async (note: {title: string; content: string; filename?: string }) => {
    const response = await api.post('/notes', note);
    return response.data;
};

export const searchNotes = async (query: string, nResults: number = 3) => {
    const response = await api.get(`/search?query=${encodeURIComponent(query)}&n_results=${nResults}`);
    return response.data;
};

export const generateFlashcards = async (noteId: string) => {
    const response = await api.post(`/generate-flashcards/${noteId}`);
};

export default api; 