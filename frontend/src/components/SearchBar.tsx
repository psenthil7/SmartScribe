import React, { useState } from 'react';
import { 
  TextField, 
  Button, 
  Box, 
  Typography,
  Chip,
  Paper
} from '@mui/material';
import { Search, SmartToy } from '@mui/icons-material';
import { searchNotes, ragSearch } from '../services/api';
import { SearchResult, RAGResponse } from '../types';

interface SearchBarProps {
  onSearchResults: (results: SearchResult[]) => void;
  onRAGResults: (results: RAGResponse) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearchResults, onRAGResults }) => {
  const [query, setQuery] = useState('');
  const [searching, setSearching] = useState(false);
  const [ragSearching, setRagSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRegularSearch = async () => {
    if (!query.trim()) return;
    
    setSearching(true);
    setError(null);
    
    try {
      const response = await searchNotes(query);
      onSearchResults(response.results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
    } finally {
      setSearching(false);
    }
  };

  const handleRAGSearch = async () => {
    if (!query.trim()) return;
    
    setRagSearching(true);
    setError(null);
    
    try {
      const response = await ragSearch(query);
      onRAGResults(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'RAG search failed');
    } finally {
      setRagSearching(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleRegularSearch();
    }
  };

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        Search Your Notes
      </Typography>
      
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField
          fullWidth
          label="Search query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter your search query..."
          disabled={searching || ragSearching}
        />
      </Box>
      
      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
        <Button
          variant="contained"
          startIcon={<Search />}
          onClick={handleRegularSearch}
          disabled={searching || ragSearching || !query.trim()}
        >
          {searching ? 'Searching...' : 'Search'}
        </Button>
        
        <Button
          variant="outlined"
          startIcon={<SmartToy />}
          onClick={handleRAGSearch}
          disabled={searching || ragSearching || !query.trim()}
        >
          {ragSearching ? 'AI Searching...' : 'AI Search (RAG)'}
        </Button>
      </Box>
      
      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}
      
      <Box sx={{ mt: 2 }}>
        <Chip 
          label="Regular search finds similar notes" 
          size="small" 
          variant="outlined" 
          sx={{ mr: 1 }}
        />
        <Chip 
          label="AI search provides intelligent answers" 
          size="small" 
          variant="outlined"
        />
      </Box>
    </Paper>
  );
};

export default SearchBar;
