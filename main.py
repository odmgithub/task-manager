import json
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks() -> list[str]:
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return data
        return []
    except json.JSONDecodeError:
        return []


def save_tasks(tasks: list[str]) -> None:
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def show_menu() -> None:
    print("\n1. Додати задачу")
    print("2. Показати задачі")
    print("3. Вийти")
    print("4. Очистити список")


def add_task(tasks: list[str]) -> None:
    task = input("Введи задачу: ").strip()
    if not task:
        print("Порожню задачу не додаємо 🙂")
        return
    tasks.append(task)
    save_tasks(tasks)
    print("Задачу додано!")


def list_tasks(tasks: list[str]) -> None:
    if not tasks:
        print("Список задач порожній.")
        return
    for i, t in enumerate(tasks, start=1):
        print(f"{i}. {t}")


def clear_tasks(tasks: list[str]) -> None:
    tasks.clear()
    save_tasks(tasks)
    print("Список очищено!")


def main() -> None:
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Обери дію: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            print("Вихід...")
            break
        elif choice == "4":
            clear_tasks(tasks)
        else:
            print("Невірний вибір")


if __name__ == "__main__":
    main()
