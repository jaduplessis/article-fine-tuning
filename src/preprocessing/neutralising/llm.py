import json
import random

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.constants import SETTINGS
from src.preprocessing.neutralising.system import base_message, style_variation


class NeutraliserLLM:
  ''' Class to neutralise the chunks using the language model
  
  '''
  def __init__(self, input_file_path: str, output_dir: str, style: str, overwrite: bool = True):
    ''' Constructor for the NeutraliserLLM class
    '''
    self.openai = self.start_openai_model()
    self.anthropic = self.start_anthropic_model()
    self.corpus = self.load_corpus(input_file_path)
    self.output_dir = output_dir
    self.neutralise_chunks = []
    self.style = style
    self.overwrite = overwrite


  def start_openai_model(self):
    ''' Function to start the language model
  
    Returns:
      openai: The language model
    '''
    model = ChatOpenAI(
      api_key=SETTINGS.openai_api_key.get_secret_value(),
      model="gpt-4",
      temperature=1,
      
      max_tokens=1500,
    )

    return model
  

  def start_anthropic_model(self):
    ''' Function to start the language model
  
    Returns:
      anthropic: The language model
    '''
    model = ChatAnthropic(
      anthropic_api_key=SETTINGS.anthropic_api_key.get_secret_value(),
      model="claude-3-sonnet-20240229",
      temperature=0.8,
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
    style = style_variation[self.style]

    system_message = base_message + style
    
    messages = [
      SystemMessage(
        content=system_message
      ),
      HumanMessage(
        content=chunk
      )
    ]
    
    # Randomly select the model to use
    if random.choice([True, False]):
      neutralised_chunk = self.openai.invoke(messages).content
    else:
      # Anthropic has rate limits so if it fails, use OpenAI
      try:
        neutralised_chunk = self.anthropic.invoke(messages).content
        print('Anthropic succeeded')
      except:
        print('Anthropic failed. Using OpenAI')
        neutralised_chunk = self.openai.invoke(messages).content

    data = {
      'chunk': chunk,
      'neutralised_chunk': neutralised_chunk,
    }
   
    return data
  

  def neutralise_corpus(self) -> list:
    ''' Function to neutralise the chunks

    Returns:
      neutralised_chunks: The neutralised chunks
    '''
    neutralised_chunks = []
    if self.overwrite:
      self.overwrite_previous_data()

    for index, styled_chunk in enumerate(self.corpus):
      print(f'Neutralising chunk: {index+1}/{len(self.corpus)}', end='\r')
      neutralise_data = self.invoke_neutraliser(styled_chunk)
      neutralised_chunk = neutralise_data['neutralised_chunk']

      neutralised_chunks.append(neutralised_chunk)

      training_response = self.format_data(styled_chunk=styled_chunk, neutralised_chunk=neutralised_chunk)

      with open(f"{self.output_dir}/neutralised_data_{self.style}.jsonl", 'a') as file:
        file.write(json.dumps(training_response) + '\n')

      with open(f"{self.output_dir}/logging_{self.style}.json", 'a') as file:
        file.write(json.dumps(neutralise_data, indent=2) + '\n')

    self.neutralise_chunks = neutralised_chunks
    return neutralised_chunks
  

  def format_data(self, styled_chunk: str, neutralised_chunk: str) -> dict:
    ''' Function to format the data

    Args:
      neutralised_chunk: The neutralised chunk
      metadata: The metadata

    Returns:
      data: The formatted data
    '''
    content = SETTINGS.fine_tuning_content
    base_prompt = SETTINGS.fine_tuning_prompt

    data = {
        "messages": [
            {
                "role": "system",
                "content": content
            },
            {
                "role": "user",
                "content": base_prompt + '\n\n```' + neutralised_chunk + '\n```'
            },
            {
                "role": "assistant",
                "content": styled_chunk
            }
        ]
    }

    return data
  

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
    # chunks = doc.split('<Chunk>')[1:]
    chunks = doc.split('\n')
    corpus = [chunk.strip() for chunk in chunks]

    return corpus
   

  def overwrite_previous_data(self):
    ''' Function to overwrite the previous data
    '''
    with open(f"{self.output_dir}/neutralised_data_{self.style}.jsonl", 'w') as file:
      file.write('')
    
    with open(f"{self.output_dir}/logging_{self.style}.json", 'w') as file:
      file.write('')
   
