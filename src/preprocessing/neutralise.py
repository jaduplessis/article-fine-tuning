
import json
from src.preprocessing.neutralising.llm import NeutraliserLLM
from src.constants import SETTINGS

"""
Prompt dataset format:
[
  {"messages": [{"role": "system", "content": "<bot description>"}, {"role": "user", "content": "<prompt>"}, {"role": "assistant", "content": "<response>"}]},
  {"messages": [{"role": "system", "content": "<bot description>"}, {"role": "user", "content": "<prompt>"}, {"role": "assistant", "content": "<response>"}]},
  ...
]
"""


def create_neutralised_dataset(file_path: str, output_file_path: str) -> None:
    ''' Function to create the neutralised dataset and save it to a file as json

    Args:
      file_path: The file path to the corpus text file
      output_file_path: The file path to the output file
    '''
    content = SETTINGS.fine_tuning_content
    base_prompt = SETTINGS.fine_tuning_prompt


    neutraliser = NeutraliserLLM(file_path)
    neutraliser.neutralise_corpus()

    if len(neutraliser.neutralise_chunks) != len(neutraliser.corpus):
        raise ValueError("The number of neutralised chunks and the original corpus should be the same.")

    # Iterate through the neutralised chunks and original corpus to create the dataset.
    # User Prompt = base_prompt + neutralised_chunk
    # Assistant Response = original_chunk
    dataset = []
    for i, chunk in enumerate(neutraliser.neutralise_chunks):
        dataset.append({
            "messages": [
                {
                    "role": "system",
                    "content": content
                },
                {
                    "role": "user",
                    "content": base_prompt + '\n\n```' + chunk + '\n```'
                },
                {
                    "role": "assistant",
                    "content": neutraliser.corpus[i]
                }
            ]
        })

    with open(output_file_path, 'w') as f:
        f.write(json.dumps(dataset, indent=2))


    