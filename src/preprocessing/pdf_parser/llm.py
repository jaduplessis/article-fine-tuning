import json
from src.constants import SETTINGS
from src.preprocessing.pdf_parser.system import system_message
from langchain_core.messages import HumanMessage, SystemMessage

from langchain_openai import ChatOpenAI


class PdfParserLLM():
  ''' Class to prune HTML files using OpenAI's language model
  
  '''
  def __init__(self):
    self.model = self.start_model()


  def start_model(self):
    ''' Function to start the language model
  
    Returns:
      openai: The language model
    '''
    metadata_model = ChatOpenAI(
      api_key=SETTINGS.openai_api_key.get_secret_value(),
      model="gpt-3.5-turbo",
      temperature=0.5,
      max_tokens=1500,
    )

    return metadata_model
  

  def parse_text(self, text: str) -> str:
    ''' Function to parse the text using the language model and the system message to format the prompt

    Args:
      text: The text to parse

    Returns:
      parsed_text: The parsed text
    '''
    messages = [
      SystemMessage(
        content=system_message
      ),
      HumanMessage(
        content=text
      )
    ]

    response = self.model.invoke(messages).content

    parsed_text = response.replace('```', '')
   
    return parsed_text
   
