import os

class Chunking:
  """
  Class to construct chunks from a doc.
  The class aims to split the doc into overlapping chunks containing full sections of the doc.
  It also aims to save the introductions, headers and conclusions of the doc.
  """
  def __init__(self, input_dir, max_chunk_size: int = 1000, min_chunk_size: int = 300):
    self.input_dir = input_dir
    self.max_chunk_size = max_chunk_size
    self.min_chunk_size = min_chunk_size


  def chunk_corpus(self):
    """
    Function to chunk the corpus.
    """
    all_chunks = []
    for file in os.listdir(self.input_dir):
        with open(f'{self.input_dir}/{file}') as f:
            doc = f.read()
        
        sections = doc.split('\n')
        for section in sections:
            chunks = self.chunk_section(section)
            all_chunks.extend(chunks)

    self.save_data(all_chunks)
    return all_chunks
        

  def chunk_section(self, section: str, max_chunk_size: int = 1000, min_chunk_size: int = 300):
    """
    Function to take sections with header tags and convert to strings.
    """
    # If conclusion, return as is
    if section.startswith('<Conclusion>'):
        return [section]

    elements = section.split('#element#')
    
    chunks = []
    chunk = ""
    for element in elements:
        if len(chunk) + len(element) < max_chunk_size:
            chunk += element
        else:
            chunks.append(chunk)
            chunk = element

    if len(chunk) > min_chunk_size:
        chunks.append(chunk)
    elif len(chunks) > 0:
        chunks[-1] += chunk

    return chunks
    


  def save_data(self, chunks):
    """
    Function that takes a dictionary containing headers, introduction and conclusion.
    The function appends the headers, introduction and conclusion to files
    in the articles/components/ folder.
    """
    with open('articles/chunks/chunks.txt', 'w') as file:
        file.write('\n'.join(chunks))
        