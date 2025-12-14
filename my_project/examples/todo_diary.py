import os

# работа с файлами (чтение, запись)

FILENAME = "../todo.txt"


def add_task(task: str):
    """Добавляет задачу в файл."""
    with open(FILENAME, 'a', encoding='utf-8') as f:
        f.write(task.strip() + '\n')
    print("✅ Задача добавлена!")


def show_tasks():
    """Выводит все задачи из файла."""
    if not os.path.exists(FILENAME):
        print("📝 Файл задач пуст.")
        return

    with open(FILENAME, 'r', encoding='utf-8') as f:
        tasks = f.readlines()

    if not tasks:
        print("📝 Нет задач.")
    else:
        print("\n📋 Ваши задачи:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task.strip()}")


def main():
    while True:
        print("\n" + "=" * 30)
        print("ДНЕВНИК ЗАДАЧ")
        print("=" * 30)
        print("1. Добавить задачу")
        print("2. Показать задачи")
        print("3. Выйти")
        choice = input("Выберите действие (1-3): ").strip()

        if choice == "1":
            task = input("Введите задачу: ")
            if task:
                add_task(task)
            else:
                print("⚠️  Задача не может быть пустой.")
        elif choice == "2":
            show_tasks()
        elif choice == "3":
            print("До свидания! 👋")
            break
        else:
            print("⚠️  Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
