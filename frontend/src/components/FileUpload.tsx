import React, { useState } from 'react';
import { 
  Button, 
  Box, 
  Typography, 
  LinearProgress, 
  Alert 
} from '@mui/material';
import { CloudUpload } from '@mui/icons-material';
import { uploadFile, processOCR } from '../services/api';
import { FileProcessResult } from '../types';

interface FileUploadProps {
  onFileProcessed: (data: FileProcessResult) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileProcessed }) => {
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError(null);

    try {
      // Upload file
      const uploadResult = await uploadFile(file);
      
      // Process with OCR
      setProcessing(true);
      const ocrResult = await processOCR(uploadResult.filename);
      
      onFileProcessed({
        message: uploadResult.message,
        filename: uploadResult.filename,
        original_name: uploadResult.original_name,
        file_path: uploadResult.file_path,
        file_type: uploadResult.file_type,
        size_bytes: uploadResult.size_bytes,
        extracted_text: ocrResult.extracted_text,
        confidence: ocrResult.confidence,
        character_count: ocrResult.character_count
      });
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setUploading(false);
      setProcessing(false);
    }
  };

  return (
    <Box sx={{ p: 3, border: '2px dashed #ccc', borderRadius: 2, textAlign: 'center' }}>
      <input
        accept="image/*,.pdf"
        style={{ display: 'none' }}
        id="file-upload"
        type="file"
        onChange={handleFileUpload}
        disabled={uploading || processing}
      />
      <label htmlFor="file-upload">
        <Button
          variant="contained"
          component="span"
          startIcon={<CloudUpload />}
          disabled={uploading || processing}
        >
          Upload Handwritten Notes
        </Button>
      </label>
      
      {(uploading || processing) && (
        <Box sx={{ mt: 2 }}>
          <LinearProgress />
          <Typography variant="body2" sx={{ mt: 1 }}>
            {uploading ? 'Uploading...' : 'Processing with OCR...'}
          </Typography>
        </Box>
      )}
      
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};

export default FileUpload;