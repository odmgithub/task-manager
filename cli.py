# cli.py
from config import settings
from storage import JsonTasksRepo
from services import TasksService


def show(tasks):
    if not tasks:
        print("Немає задач.")
        return
    for t in tasks:
        mark = "✓" if t.done else " "
        print(f"{t.id:>3} [{mark}] {t.text}  ({t.created_at})")


def main():
    svc = TasksService(JsonTasksRepo(settings.tasks_path))

    while True:
        print("\n1) list  2) add  3) toggle  4) edit  5) delete  0) exit")
        choice = input("> ").strip()

        try:
            if choice == "1":
                show(svc.list_tasks())

            elif choice == "2":
                text = input("Text: ")
                t = svc.add_task(text)
                print(f"Added: #{t.id}")

            elif choice == "3":
                task_id = int(input("ID: "))
                t = svc.toggle_task(task_id)
                print(f"Toggled: #{t.id} -> done={t.done}")

            elif choice == "4":
                task_id = int(input("ID: "))
                text = input("New text: ")
                t = svc.update_task(task_id, text)
                print(f"Updated: #{t.id}")

            elif choice == "5":
                task_id = int(input("ID: "))
                svc.delete_task(task_id)
                print("Deleted.")

            elif choice == "0":
                break

            else:
                print("Невідомий вибір.")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()