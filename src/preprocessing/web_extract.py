from src.preprocessing.web_parser.soup import soupify, get_sections


def extract_sections(urls):
    """ Function to extract sections from a list of webpage and save them to a file.
    """
    for index, url in enumerate(urls):
        soup = soupify(url)
        sections = get_sections(soup)

        with open(f'articles/parsed/file_{index}.txt', 'w') as file:
            for section in sections:
                section = '#element#'.join(section)
                file.write(str(section) + '\n')