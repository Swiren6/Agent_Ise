from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # Database
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    
    # LLM
    TOGETHER_API_KEY: str
    
    # App
    APP_NAME: str = "SQL Assistant API"
    DEBUG: bool = False
    
    # Cache
    CACHE_FILE: str = "question_cache.json"
    
    # Fichiers de configuration
    RELATIONS_FILE: str = "prompt_relations.txt"
    
    class Config:
        env_file = ".env"
        
    @property
    def database_url(self) -> str:
        return f"mysql+mysqlconnector://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

settings = Settings()