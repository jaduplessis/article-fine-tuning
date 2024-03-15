import json
import random
from src.constants import SETTINGS
from src.preprocessing.neutralising.system import base_message_a, base_message_b, style_variation
from langchain_core.messages import HumanMessage, SystemMessage

from langchain_openai import ChatOpenAI


class NeutraliserLLM:
  ''' Class to neutralise the chunks using the language model
  
  '''
  def __init__(self, file_path: str):
    self.model = self.start_model()
    self.corpus = self.load_corpus(file_path)
    self.neutralise_chunks = []


  def start_model(self):
    ''' Function to start the language model
  
    Returns:
      openai: The language model
    '''
    model = ChatOpenAI(
      api_key=SETTINGS.openai_api_key.get_secret_value(),
      model="gpt-4",
      temperature=1.15,
      max_tokens=1500,
    )

    return model
  

  def invoke_neutraliser(self, chunk: str) -> str:
    ''' Function to neutralise the chunk using the language model and the system message to format the prompt

    Args:
      chunk: The chunk to neutralise

    Returns:
      neutralised_chunk: The neutralised chunk
    '''
    index = random.randint(0, len(style_variation) - 1)
    style = style_variation[index]

    system_message = base_message_a + style + base_message_b
    
    messages = [
      SystemMessage(
        content=system_message
      ),
      HumanMessage(
        content=chunk
      )
    ]

    neutralised_chunk = self.model.invoke(messages).content
   
    return neutralised_chunk
  

  def neutralise_corpus(self) -> list:
    ''' Function to neutralise the chunks

    Returns:
      neutralised_chunks: The neutralised chunks
    '''
    neutralised_chunks = []

    for index, chunk in enumerate(self.corpus):
      print(f'Neutralising chunk: {index+1}/{len(self.corpus)}')
      neutralised_chunk = self.invoke_neutraliser(chunk)
      neutralised_chunks.append(neutralised_chunk)

    self.neutralise_chunks = neutralised_chunks
    return neutralised_chunks
  

  def load_corpus(self, file_path: str) -> list:
    ''' Function to load the corpus

    Args:
      file_path: The file path to the corpus text file

    Returns:
      corpus: The corpus
    '''
    with open(file_path, 'r') as file:
      doc = file.read()
    
    # Iterate through the corpus and split it into chunks.
    # Chunks are delimited by <Chunk> tags.
    chunks = doc.split('<Chunk>')[1:]
    corpus = [chunk.strip() for chunk in chunks]

    return corpus
   
