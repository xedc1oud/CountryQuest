from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    token: SecretStr
    database: SecretStr
    redis: SecretStr
    
    model_config = SettingsConfigDict(
        env_file='prod.env', 
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=False
    )
    
settings = Settings()