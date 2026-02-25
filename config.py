# config.py
from pydantic import BaseModel


class Settings(BaseModel):
    """
    Єдине місце для конфігурації проекту.

    Чому це корисно:
    - шлях до tasks.json не "розмазаний" по коду
    - пізніше можна легко додати ENV-перемінні (TASKS_PATH, DEBUG, тощо)
    """
    tasks_path: str = "tasks.json"


# Глобальний обʼєкт налаштувань.
# Його імпортують і API, і CLI, і deps.py.
settings = Settings()