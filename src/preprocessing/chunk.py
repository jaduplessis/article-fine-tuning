from src.preprocessing.chunking.chunks import Chunking
import os

def chunk_text(file_path):
    with open(file_path) as f:
        doc = f.read()

    chunking = Chunking()
    chunking.construct_chunks(doc)
    chunking.save_data()



def recursive_chunk_text(input_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                print(f'Processing {file_path}', end='\n')
                chunk_text(file_path)