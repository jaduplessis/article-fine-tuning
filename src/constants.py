"""Set up some constants for the project."""
from typing import List

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the demo app.

    Reads from environment variables.
    You can create the .env file from the .env_example file.

    !!! SecretStr is a pydantic type that hides the value in logs.
    If you want to use the real value, you should do:
    SETTINGS.<variable>.get_secret_value()
    """

    class Config:
        env_file = ".env"


    openai_api_key: SecretStr
    anthropic_api_key: SecretStr
    
    supabase_url: str
    supabase_service_key: SecretStr

    fine_tuning_prompt: str = "Can you format this text for the ALEIOS style and tone?"
    fine_tuning_content: str = "Gob is a stylistic chatbot that is excellent at rephrasing text."

    parsed_output: str = 'articles/parsed/'



SETTINGS = Settings()  # type: ignore
