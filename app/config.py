# Path: `app/env.py`
# Description: This file contains code to load `.env` file and make a pydantic `BaseSettings` class which can be used to access environment variables in the application.
 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MongoDB Configuration
    MONGO_DB_USER: str
    MONGO_DB_PASSWORD: str
    MONGO_DB_HOST: str
    MONGO_DB_PORT: str
    MONGO_DB_NAME: str
    
    @classmethod
    def get_mongodb_uri(cls) -> str:
        return f"mongodb://{settings.MONGO_DB_USER}:{settings.MONGO_DB_PASSWORD}@{settings.MONGO_DB_HOST}:{settings.MONGO_DB_PORT}"
    
    # PostgreSQL Configuration
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    
    @classmethod
    def get_postgres_uri(cls) -> str:
        return f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    
    # SRM Student Portal Credentials
    SRM_PORTAL_USERNAME: str
    SRM_PORTAL_PASSWORD: str
    
    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
settings = Settings()
