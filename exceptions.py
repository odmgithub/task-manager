# exceptions.py

class TaskError(Exception):
    """
    Базова помилка домену (Task Manager).

    Ідея:
    - всі "наші" помилки наслідуються від TaskError
    - API/CLI можуть ловити TaskError і робити однакову обробку
    """
    pass


class TaskNotFound(TaskError):
    """Коли задача з таким id не існує."""
    pass


class TaskTextEmpty(TaskError):
    """Коли текст задачі порожній або тільки з пробілів."""
    pass


class StorageError(TaskError):
    """
    Помилка рівня сховища (файл не читається/не пишеться).

    (Опційно для майбутнього) — корисно відрізняти від помилок домену.
    """
    pass