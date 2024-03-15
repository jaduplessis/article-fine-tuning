import os

import fitz

from src.preprocessing.formatter.llm import FormatterLLM
from src.preprocessing.pdf_parser.llm import PdfParserLLM


def extract_text(pdf_path, output_path):
    """
    Function to extract and format the text from a PDF file and save it to a text file.
    """

    parser_llm = PdfParserLLM()
    formatter_llm = FormatterLLM()

    doc = fitz.open(pdf_path)
    parsed_text = ''

    for (index, page) in enumerate(doc):
        print(f'Processing page {index+1}/{len(doc)}', end='\r')

        text = page.get_text()

        parsed_text += parser_llm.parse_text(text)

    formatted_text = formatter_llm.format_text(parsed_text)

    with open('articles/parsed/' + output_path, 'w', encoding='utf-8') as f:
        f.write(formatted_text)


def recursive_extract_text(input_dir):
    """
    Function to recursively extract and format the text from all PDF files in
    a directory and its subdirectories.
    """
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.pdf'):
                output_path = file.split('/')[-1].replace('.pdf', '.txt')

                pdf_path = os.path.join(root, file)
                print(f'Processing {pdf_path}', end='\n')
                extract_text(pdf_path, output_path)