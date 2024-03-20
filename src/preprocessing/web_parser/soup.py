
from bs4 import BeautifulSoup
import requests


def soupify(url):
  """ Function to get the HTML content of a webpage and parse it using BeautifulSoup.
  """
  
  response = requests.get(url)
  html_content = response.content
  soup = BeautifulSoup(html_content, "html.parser")

  return soup


def get_sections(soup):
  """ Function to extract sections from a webpage using BeautifulSoup.
  """
  
  # Extract the <article> tag from the HTML content
  article = soup.find("article")

  headers = ["header", "h1", "h2", "h3", "h4", "h5", "h6"]
  elements = article.find_all(headers + ["p"])

  sections = []
  section = []
  for element in elements:
      # Maintaining the tags
      if element.name in headers:
          if len(section) > 1:
              sections.append(section)

          bare_element = f"<{element.name}>{element.text}</{element.name}>"
          section = [bare_element]

      else:
          section.append(element)

  print(f"Extracted {len(sections)} sections from the webpage.")
  return sections
