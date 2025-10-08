# Імпортуємо функції-помічники та функції вводу даних
from utility import generate_next_id 
from ui_manager import get_valid_string


def _get_valid_course(prompt: str) -> int:
    # Запитує курс як число від 1 до 4 (повертає int).
    while True:
        value = input(prompt).strip()
        if not value:
            print("Помилка: Ввід не може бути порожнім. Введіть число від 1 до 4.")
            continue
        if value.isdigit():
            n = int(value)
            if 1 <= n <= 4:
                return n
        print("Помилка: некоректний курс. Введіть число від 1 до 4.")


def add_student(journal: dict):
    # Збирає дані про студента, генерує ID та додає запис до журналу.
    # 1. Генерація унікального ID
    new_id = generate_next_id(journal)

    print(f"\nДодавання нового студента. ID: {new_id}")

    # 2. Збір даних
    last_name = get_valid_string("Введіть Прізвище: ")
    first_name = get_valid_string("Введіть Ім'я: ")
    group = get_valid_string("Введіть Групу: ")
    course = _get_valid_course("Введіть Курс (1-4): ")

    # 3. Додавання нового запису у GLOBAL_JOURNAL (через аргумент journal)
    journal[new_id] = {
        "first_name": first_name,
        "last_name": last_name,
        "group": group,
        "course": course,
        "performance": {}  # Словник для майбутніх оцінок
    }

    print(f"\nСтудента {first_name} {last_name} (ID: {new_id}) успішно додано.")


def display_all_students(journal: dict):
    # Відображає відформатований список усіх студентів.
    if not journal:
        print("\nЖурнал порожній. Немає студентів для відображення.")
        return

    print("\n----- ПОТОЧНИЙ СПИСОК СТУДЕНТІВ -----")
    print(f"{'ID':<8} | {'Прізвище':<15} | {'Ім\'я':<15} | {'Група':<10} | {'Курс':<4}")
    print("-" * 70)

    # Ітерація по ключах (ID) та значеннях (словники даних)
    for student_id, data in journal.items():
        course = data.get('course', '')
        print(f"{student_id:<8} | {data['last_name']:<15} | {data['first_name']:<15} | {data['group']:<10} | {str(course):<4}")
    print("-" * 70)


def expel_student(journal: dict):
    # Видаляє студента за ID після підтвердження.
    if not journal:
        print("\nЖурнал порожній. Немає студентів для видалення.")
        return

    student_id = get_valid_string("Введіть ID студента для відрахування: ")
    if student_id not in journal:
        print(f"\nСтудент з ID {student_id} не знайдений.")
        return

    data = journal[student_id]
    confirm = get_valid_string(f"Підтвердіть відрахування {data['first_name']} {data['last_name']} (y/n): ")
    if confirm.lower() in ('y', 'так', 'yes'):
        del journal[student_id]
        print(f"\nСтудент {data['first_name']} {data['last_name']} (ID: {student_id}) відрахований.")
    else:
        print("\nВідрахування скасовано.")


def edit_student(journal: dict):
    # Редагує основні поля студента: прізвище, ім'я, група, курс.
    if not journal:
        print("\nЖурнал порожній. Немає студентів для редагування.")
        return

    student_id = get_valid_string("Введіть ID студента для редагування: ")
    if student_id not in journal:
        print(f"\nСтудент з ID {student_id} не знайдений.")
        return

    data = journal[student_id]
    print(f"\nПоточні дані: Прізвище: {data.get('last_name','')}, Ім'я: {data.get('first_name','')}, Група: {data.get('group','')}, Курс: {data.get('course','')}")
    new_last = input("Введіть нове Прізвище (залиште пустим щоб не змінювати): ").strip()
    new_first = input("Введіть нове Ім'я (залиште пустим щоб не змінювати): ").strip()
    new_group = input("Введіть нову Групу (залиште пустим щоб не змінювати): ").strip()
    new_course = input("Введіть новий Курс (1-4) (залиште пустим щоб не змінювати): ").strip()

    if new_last:
        data['last_name'] = new_last
    if new_first:
        data['first_name'] = new_first
    if new_group:
        data['group'] = new_group
    if new_course:
        if new_course.isdigit() and 1 <= int(new_course) <= 4:
            data['course'] = int(new_course)
        else:
            print("Помилка: курс не змінено. Значення має бути від 1 до 4.")

    journal[student_id] = data
    print(f"\nДані студента (ID: {student_id}) оновлено.")


def display_student_performance(journal: dict):
    # Показує словник 'performance' для конкретного студента за ID.
    if not journal:
        print("\nЖурнал порожній. Немає студентів для показу успішності.")
        return

    student_id = get_valid_string("Введіть ID студента для перегляду успішності: ")
    if student_id not in journal:
        print(f"\nСтудент з ID {student_id} не знайдений.")
        return

    performance = journal[student_id].get('performance', {})
    if not performance:
        print(f"\nУ студента (ID: {student_id}) ще немає записів з оцінками.")
        return

    print(f"\nУспішність студента {journal[student_id]['first_name']} {journal[student_id]['last_name']} (ID: {student_id}):")
    for subj, grades in performance.items():
        print(f" - {subj}: {grades}")