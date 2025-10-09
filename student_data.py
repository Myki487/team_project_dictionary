# Імпортуємо функції-помічники та функції вводу даних
from utility import generate_next_id 
from ui_manager import get_valid_string

def add_student(journal: dict):
    """Збирає дані про студента, генерує ID та додає запис до журналу."""

    # 1. Генерація унікального ID
    new_id = generate_next_id(journal)

    print(f"\nДодавання нового студента. ID: {new_id}")

    # 2. Збір даних
    last_name = get_valid_string("Введіть Прізвище: ")
    first_name = get_valid_string("Введіть Ім'я: ")
    group = get_valid_string("Введіть Групу: ")

    # 3. Додавання нового запису у GLOBAL_JOURNAL (через аргумент journal)
    journal[new_id] = {
        "first_name": first_name,
        "last_name": last_name,
        "group": group,
        "performance": {}  # Словник для майбутніх оцінок
    }

    print(f"\nСтудента {first_name} {last_name} (ID: {new_id}) успішно додано.")

def display_all_students(journal: dict):
    """Відображає відформатований список усіх студентів."""
    if not journal:
        print("\nЖурнал порожній. Немає студентів для відображення.")
        return

    print("\n----- ПОТОЧНИЙ СПИСОК СТУДЕНТІВ -----")
    print(f"{'ID':<8} | {'Прізвище':<15} | {'Ім\'я':<15} | {'Група':<10}")
    print("-" * 55)

    # Ітерація по ключах (ID) та значеннях (словники даних)
    for student_id, data in journal.items():
        print(f"{student_id:<8} | {data['last_name']:<15} | {data['first_name']:<15} | {data['group']:<10}")
    print("-" * 55)

def expel_student(journal: dict):
    # Відрахувати (видалити) студента за ID після підтвердження.
    if not journal:
        print("\nЖурнал порожній. Немає студентів для відрахування.")
        return

    # Показати поточний список для зручності
    display_all_students(journal)

    student_id = get_valid_string("Введіть ID студента для відрахування (наприклад, STU001): ")
    if student_id not in journal:
        print(f"\nСтудент з ID {student_id} не знайдений.")
        return

    student = journal[student_id]
    confirm = input(f"Підтвердьте відрахування {student['first_name']} {student['last_name']} (y/n): ").strip().lower()
    if confirm in ('y', 'yes', 'т', 'так'):
        del journal[student_id]
        print(f"\nСтудент {student['first_name']} {student['last_name']} (ID: {student_id}) відрахований.")
    else:
        print("\nВідмовлено. Студента не відраховано.")