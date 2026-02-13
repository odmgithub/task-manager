tasks = []

while True:
    print("\n1. Додати задачу")
    print("2. Показати задачі")
    print("3. Вийти")

    choice = input("Обери дію: ")

    if choice == "1":
        task = input("Введи задачу: ")
        tasks.append(task)
        print("Задачу додано!")
    elif choice == "2":
        if len(tasks) == 0:
            print("Список задач порожній.")
        else:
            for i, t in enumerate(tasks):
                print(f"{i + 1}. {t}")
    elif choice == "3":
        print("Вихід...")
        break
    else:
        print("Невірний вибір")
