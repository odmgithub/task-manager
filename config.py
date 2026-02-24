# config.py
from pydantic import BaseModel

class Settings(BaseModel):
    tasks_path: str = "tasks.json"

settings = Settings()