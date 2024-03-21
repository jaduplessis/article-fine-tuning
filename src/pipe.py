import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))

from src.preprocessing.chunk import recursive_chunk_text
from src.preprocessing.neutralise import create_neutralised_dataset
from src.preprocessing.pdf_extract import recursive_extract_text

if __name__ == '__main__':
  recursive_extract_text('articles/raw/')

  # delete articles/chunks/chunks.txt
  if os.path.exists('articles/chunks/chunks.txt'):
      os.remove('articles/chunks/chunks.txt')
      
  recursive_chunk_text('articles/parsed/')

  neutraliser = create_neutralised_dataset('articles/chunks/chunks.txt', 'articles/neutralised/training_data.json')