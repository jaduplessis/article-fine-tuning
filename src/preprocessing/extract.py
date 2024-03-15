import fitz
from src.preprocessing.formatter.llm import FormatterLLM  
from src.preprocessing.pdf_parser.llm import PdfParserLLM


def extract_text(pdf_path):
    parser_llm = PdfParserLLM()
    formatter_llm = FormatterLLM()

    doc = fitz.open(pdf_path)
    parsed_text = ''

    for (index, page) in enumerate(doc):    
        print(f'Processing page {index+1}/{len(doc)}', end='\r')

        text = page.get_text()

        parsed_text += parser_llm.parse_text(text)

    formatted_text = formatter_llm.format_text(parsed_text)

    with open('output2.txt', 'w') as f:
        f.write(formatted_text)

