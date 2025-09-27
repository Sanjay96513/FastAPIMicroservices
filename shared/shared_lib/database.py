import motor.motor_asyncio
from beanie import init_beanie
from pydantic_settings import BaseSettings
from . import models  # Import models to be initialized

class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://admin:password@mongo:27017"
    DATABASE_NAME: str = "fastapi_microservices"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

async def init_db():
    """
    Initializes the database connection and Beanie ODM.
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
    db = client[settings.DATABASE_NAME]

    await init_beanie(
        database=db,
        document_models=[
            models.User,
            models.Transaction,
            # Add other models here as they are created
        ],
    )