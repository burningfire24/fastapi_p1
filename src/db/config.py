from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent/".env" 

class Settings(BaseSettings):

    DATABASE_URL: SecretStr
    HOST:str = "localhost"
    PORT:str = 6379
    model_config=SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore"
    )


config = Settings()    

print(config.DATABASE_URL)