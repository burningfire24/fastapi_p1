from pydantic_settings import BaseSettings, SettingsConfigDict 
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent/".env" 

class Settings(BaseSettings):

    secret_key:str
    algorithm:str
    model_config=SettingsConfigDict(
        env_file=ENV_FILE,
        extra='ignore'
    )

    

config = Settings()

print(config.secret_key)