import PyPDF2
from typing import Optional

class PDFParser:
    """Extract text from PDF files"""
    
    @staticmethod
    def extract_text(pdf_file) -> str:
        """
        Extract all text from a PDF file
        
        Args:
            pdf_file: File object or path to PDF
            
        Returns:
            Extracted text as string
        """
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 2000) -> list[str]:
        """
        Split text into chunks for processing
        
        Args:
            text: Input text
            chunk_size: Maximum characters per chunk
            
        Returns:
            List of text chunks
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            
            if current_length + word_length > chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks