import React, { useState } from 'react';
import { 
  Button, 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  CardActions,
  Paper,
  TextField,
  Grid,
  Chip
} from '@mui/material';
import { School, Refresh } from '@mui/icons-material';
import { generateFlashcardsFromSearch } from '../services/api';
import { Flashcard } from '../types';

interface FlashcardGeneratorProps {
  query?: string;
}

const FlashcardGenerator: React.FC<FlashcardGeneratorProps> = ({ query: initialQuery }) => {
  const [query, setQuery] = useState(initialQuery || '');
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);

  const handleGenerateFlashcards = async () => {
    if (!query.trim()) return;
    
    setGenerating(true);
    setError(null);
    
    try {
      const response = await generateFlashcardsFromSearch(query, 3, 5);
      setFlashcards(response.flashcards);
      setCurrentCardIndex(0);
      setShowAnswer(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Flashcard generation failed');
    } finally {
      setGenerating(false);
    }
  };

  const handleNextCard = () => {
    if (currentCardIndex < flashcards.length - 1) {
      setCurrentCardIndex(currentCardIndex + 1);
      setShowAnswer(false);
    }
  };

  const handlePreviousCard = () => {
    if (currentCardIndex > 0) {
      setCurrentCardIndex(currentCardIndex - 1);
      setShowAnswer(false);
    }
  };

  const toggleAnswer = () => {
    setShowAnswer(!showAnswer);
  };

  const currentCard = flashcards[currentCardIndex];

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Generate Flashcards
      </Typography>
      
      <Box sx={{ mb: 3 }}>
        <TextField
          fullWidth
          label="Topic for flashcards"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter a topic to generate flashcards..."
          sx={{ mb: 2 }}
        />
        
        <Button
          variant="contained"
          startIcon={<School />}
          onClick={handleGenerateFlashcards}
          disabled={generating || !query.trim()}
        >
          {generating ? 'Generating...' : 'Generate Flashcards'}
        </Button>
      </Box>

      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}

      {flashcards.length > 0 && (
        <Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Card {currentCardIndex + 1} of {flashcards.length}
            </Typography>
            <Chip 
              label={`${flashcards.length} cards generated`} 
              size="small" 
              variant="outlined"
            />
          </Box>

          <Card sx={{ mb: 2, minHeight: 200 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Question:
              </Typography>
              <Typography variant="body1" sx={{ mb: 2 }}>
                {currentCard.question}
              </Typography>
              
              {showAnswer && (
                <>
                  <Typography variant="h6" gutterBottom>
                    Answer:
                  </Typography>
                  <Typography variant="body1">
                    {currentCard.answer}
                  </Typography>
                </>
              )}
            </CardContent>
            
            <CardActions>
              <Button 
                size="small" 
                onClick={toggleAnswer}
              >
                {showAnswer ? 'Hide Answer' : 'Show Answer'}
              </Button>
            </CardActions>
          </Card>

          <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center' }}>
            <Button
              variant="outlined"
              onClick={handlePreviousCard}
              disabled={currentCardIndex === 0}
            >
              Previous
            </Button>
            
            <Button
              variant="outlined"
              onClick={handleNextCard}
              disabled={currentCardIndex === flashcards.length - 1}
            >
              Next
            </Button>
            
            <Button
              variant="outlined"
              startIcon={<Refresh />}
              onClick={handleGenerateFlashcards}
              disabled={generating}
            >
              Regenerate
            </Button>
          </Box>
        </Box>
      )}
    </Paper>
  );
};

export default FlashcardGenerator;
