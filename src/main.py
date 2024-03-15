import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scraping.data_fetcher import data_fetcher

if __name__ == '__main__':
  corpus = data_fetcher()
  