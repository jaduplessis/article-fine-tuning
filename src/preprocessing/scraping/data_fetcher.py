from src.constants import SETTINGS

import requests
from bs4 import BeautifulSoup


def data_fetcher():
  ''' Function to fetch the data from the URLs in the settings file

  Returns:
    dict: A dictionary of the URLs and their content
  '''

  docs_url = SETTINGS.docs_url
  corpus = {}

  # Fetch the URLs from the settings and recursively fetch the content
  for url in docs_url:
    doc = fetch(url)
    corpus[url] = doc

  return corpus
  

def fetch(url):
  ''' Function to fetch the content of a URL and return the body minus the script and style tags

  Args:
    url (str): The URL to fetch

  Returns:
    str: The content of the body of the URL
  '''
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
  }
  
  response = requests.get(url, headers=headers)
  response.raise_for_status()

  soup = BeautifulSoup(response.text, 'html.parser')
  
  # Strip out the script and style tags
  for script in soup(['script', 'style']):
    script.decompose()

  for tag in soup():
    # Remove all style attributes
    if tag.has_attr('style'):
        del tag['style']
    
    # Optional: Remove other common styling attributes like 'class' and 'id'
    for attribute in ['class', 'id']:
        if tag.has_attr(attribute):
            del tag[attribute]
    
    # List of attributes you consider unnecessary for your needs
    for attribute in ['class', 'id', 'data-*']:
        if tag.has_attr(attribute):
            del tag[attribute]
  
  return soup.prettify()
  
      

