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
    print("5. Видалити задачу")
    print("6. Позначити як виконану")


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


def delete_task(tasks: list[str]) -> None:
    if not tasks:
        print("Немає задач для видалення.")
        return

    list_tasks(tasks)
    raw = input("Введи номер задачі для видалення: ").strip()

    if not raw.isdigit():
        print("Треба ввести число.")
        return

    idx = int(raw) - 1  # бо людям зручно з 1, а в списку індекси з 0

    if idx < 0 or idx >= len(tasks):
        print("Немає задачі з таким номером.")
        return

    removed = tasks.pop(idx)
    save_tasks(tasks)
    print(f"Видалено: {removed}")


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
        elif choice == "5":
            delete_task(tasks)
        elif choice == "6":
            complete_task(tasks)
        else:
            print("Невірний вибір")


def complete_task(tasks: list[str]) -> None:
    if not tasks:
        print("Немає задач.")
        return

    list_tasks(tasks)

    raw = input("Введи номер виконаної задачі: ").strip()

    if not raw.isdigit():
        print("Треба число.")
        return

    idx = int(raw) - 1

    if idx < 0 or idx >= len(tasks):
        print("Невірний номер.")
        return

    tasks[idx] = "[✓] " + tasks[idx]
    save_tasks(tasks)
    print("Позначено як виконану!")


if __name__ == "__main__":
    main()
