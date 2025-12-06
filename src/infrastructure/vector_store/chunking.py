import re
from typing import List
from src.domain.interfaces.chunking import BaseChunker

class RecursiveChunker(BaseChunker):
    def chunk_text(self, text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
        if not text:
            return []

        text = re.sub(r'\s+', ' ', text).strip()
        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:

            end = start + chunk_size
            if end >= text_len:
                chunks.append(text[start:])
                break
            boundary = -1
            for delimiter in ['. ', '? ', '! ', '\n', ' ']:
                boundary = text.rfind(delimiter, start, end)
                if boundary != -1:
                    break
            if boundary == -1:
                boundary = end
            else:
                boundary += 1 

            chunks.append(text[start:boundary].strip())
            start = boundary - chunk_overlap
            
  
            if start < boundary - chunk_size: 
                start = boundary
        return [c for c in chunks if c]