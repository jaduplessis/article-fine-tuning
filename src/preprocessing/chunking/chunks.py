
class Chunking:
  """
  Class to construct chunks from a doc.
  The class aims to split the doc into overlapping chunks containing full sections of the doc.
  It also aims to save the introductions, headers and conclusions of the doc.
  """
  
  def __init__(self, min_chunk_size=1250, max_chunk=2500, max_overlap=750, min_overlap=500):
    self.min_chunk_size = min_chunk_size
    self.max_chunk = max_chunk
    self.max_overlap = max_overlap
    self.min_overlap = min_overlap


  def split_sections(self, doc):
    """
    Function to iterate through doc line by line and split into sections.
    When a line starting with a # is found, it is considered a header.
    The function returns a list of sections, where each section is a string.
    """
    lines = doc.split('\n')
    sections = []

    section = ''
    for line in lines:
      if line.startswith('#'):
        sections.append(section)
        section = line
      else:
        section += '\n' + line

    return sections
  

  def calculate_overlap(self, chunk_sections):
    """
    Function to calculate the overlap between two chunks of doc. 
    The function iterates through the chunk_sections from the end,
    and compares the last min_overlap characters of the current section
    The function returns the overlap as a string.
    """
    overlap = ''
    chunk_sections = chunk_sections[::-1]
    for section in chunk_sections:
      overlap += section
      if len(overlap) >= self.min_overlap:
        break

    if len(overlap) > self.max_overlap:
      # Find the first '.' 500 characters from the end of the overlap
      # and truncate the overlap to that position
      overlap = overlap[-self.max_overlap:]
      last_dot = overlap.find('. ')
      if last_dot > 0:
        overlap = overlap[last_dot+1:]

    return overlap


  def construct_chunks(self, doc):
    """
    Function to construct chunks from a doc.
    Chunks are constructed from stitching together sections of the doc.
    The chunks should be at least min_chunk_size, but no more than max_chunk. 
    They should overlap by at least min_overlap.
    The function returns a list of chunks, where each chunk is a string.
    """
    sections = self.split_sections(doc)
    chunks = []

    chunk_sections = []
    for section in sections:
      chunk_sections.append(section)
      chunk_length = sum([len(s) for s in chunk_sections])
      
      if chunk_length > self.max_chunk:
        chunk_sections.pop()
        chunk = ''.join(chunk_sections)
        chunks.append(chunk)
        overlap = self.calculate_overlap(chunk_sections)
        chunk_sections = [overlap, section]

      elif chunk_length < self.min_chunk_size:
        continue

      elif chunk_length >= self.min_chunk_size:
        chunk = ''.join(chunk_sections)
        chunks.append(chunk)

        overlap = self.calculate_overlap(chunk_sections)
        chunk_sections = [overlap]

    return chunks
      
