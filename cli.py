from services import (
    get_tasks_service as list_tasks,
    add_task_service as add_task,
    toggle_task_service as toggle_task,
    update_task_service as update_task,
    delete_task_service as delete_task,
)

def show(tasks):
    if not tasks:
        print("Немає задач.")
        return
    for t in tasks:
        mark = "✓" if t.done else " "
        print(f"{t.id:>3} [{mark}] {t.text}  ({t.created_at})")


def main():
    while True:
        print("\n1) list  2) add  3) toggle  4) edit  5) delete  0) exit")
        choice = input("> ").strip()

        try:
            if choice == "1":
                show(list_tasks())

            elif choice == "2":
                text = input("Text: ")
                t = add_task(text)
                print(f"Added: #{t.id}")

            elif choice == "3":
                task_id = int(input("ID: "))
                t = toggle_task(task_id)
                print(f"Toggled: #{t.id} -> done={t.done}")

            elif choice == "4":
                task_id = int(input("ID: "))
                text = input("New text: ")
                t = update_task(task_id, text)
                print(f"Updated: #{t.id}")

            elif choice == "5":
                task_id = int(input("ID: "))
                delete_task(task_id)
                print("Deleted.")

            elif choice == "0":
                break

            else:
                print("Невідомий вибір.")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()