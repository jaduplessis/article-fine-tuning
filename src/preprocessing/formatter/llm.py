import json
from src.constants import SETTINGS
from src.preprocessing.pdf_parser.system import system_message
from langchain_core.messages import HumanMessage, SystemMessage

from langchain_openai import ChatOpenAI


class FormatterLLM():
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
      model="gpt-4-0125-preview",
      temperature=0.7,
      max_tokens=3500,
    )

    return metadata_model
  

  def format_text(self, text: str) -> str:
    ''' Function to format the text using the language model and the system message to format the prompt

    Args:
      text: The text to format

    Returns:
      formatted_text: The formatted text
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

    formatted_text = response.replace('<<<', '').replace('>>>', '')
   
    return formatted_text
   
