from pydantic_settings import BaseSettings, SettingsConfigDict 
from pydantic import SecretStr
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent/".env" 

class Settings(BaseSettings):

    secret_key: SecretStr
    algorithm: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    model_config=SettingsConfigDict(
        env_file=ENV_FILE,
        extra='ignore'
    )

config = Settings()