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
    # Нове поле: Курс (ціле число > 0)
    while True:
        course_input = input("Введіть номер Курсу (число, наприклад 1, 2, 3): ").strip()
        if course_input.isdigit() and int(course_input) > 0:
            course = int(course_input)
            break
        print("Помилка: введіть позитивне число для курсу.")

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
    """Відображає відформатований список усіх студентів."""
    if not journal:
        print("\nЖурнал порожній. Немає студентів для відображення.")
        return

    print("\n----- ПОТОЧНИЙ СПИСОК СТУДЕНТІВ -----")
    print(f"{'ID':<8} | {'Прізвище':<15} | {'Ім\'я':<15} | {'Група':<10} | {'Курс':<5}")
    print("-" * 70)

    # Ітерація по ключах (ID) та значеннях (словники даних)
    for student_id, data in journal.items():
        # Показуємо дефолтну позначку, якщо поле 'course' відсутнє або пусте
        course_val = data.get('course', '')
        course_display = str(course_val) if course_val not in (None, '') else '-'
        print(f"{student_id:<8} | {data.get('last_name',''):<15} | {data.get('first_name',''):<15} | {data.get('group',''):<10} | {course_display:<6}")
    print("-" * 70)

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
    # Показуємо курс у підтвердженні, якщо він є
    course_info = f" (курс: {student.get('course','-')})" if student.get('course', '') not in (None, '') else ''
    confirm = input(f"Підтвердьте відрахування {student['first_name']} {student['last_name']}{course_info} (y/n): ").strip().lower()
    if confirm in ('y', 'yes', 'т', 'так'):
        del journal[student_id]
        print(f"\nСтудент {student['first_name']} {student['last_name']} (ID: {student_id}) відрахований.")
    else:
        print("\nВідмовлено. Студента не відраховано.")


def edit_student(journal: dict):
    """
    Редагує дані студента: прізвище, ім'я, група.
    Користувач може пропустити поле (натиснути Enter) щоб залишити поточне значення.
    """
    if not journal:
        print("\nЖурнал порожній. Немає студентів для редагування.")
        return

    # Показати поточний список для вибору
    display_all_students(journal)

    student_id = get_valid_string("Введіть ID студента для редагування (наприклад, STU001): ")
    if student_id not in journal:
        print(f"\nСтудент з ID {student_id} не знайдений.")
        return

    student = journal[student_id]
    print(f"\nПоточні дані для {student['first_name']} {student['last_name']} (ID: {student_id}):")
    print(f"  Прізвище: {student['last_name']}")
    print(f"  Ім'я: {student['first_name']}")
    print(f"  Група: {student['group']}")
    print(f"  Курс: {student.get('course', '')}")

    # Запитати нові значення (порожнє = без змін)
    new_last = input(f"Введіть нове Прізвище (залиште порожнім щоб не змінювати) [{student['last_name']}]: ").strip()
    new_first = input(f"Введіть нове Ім'я (залиште порожнім щоб не змінювати) [{student['first_name']}]: ").strip()
    new_group = input(f"Введіть нову Групу (залиште порожнім щоб не змінювати) [{student['group']}]: ").strip()
    new_course = input(f"Введіть новий Курс (число, залиште порожнім щоб не змінювати) [{student.get('course', '')}]: ").strip()

    if not new_last and not new_first and not new_group and not new_course:
        print("\nНічого не змінено.")
        return

    confirm = input("Підтвердьте внесення змін (y/n): ").strip().lower()
    if confirm not in ('y', 'yes', 'т', 'так'):
        print("\nРедагування відмінено. Дані не змінено.")
        return

    if new_last:
        student['last_name'] = new_last
    if new_first:
        student['first_name'] = new_first
    if new_group:
        student['group'] = new_group
    if new_course:
        if new_course.isdigit() and int(new_course) > 0:
            student['course'] = int(new_course)
        else:
            print("Попередження: курс не було змінено — введено некоректне значення.")

    journal[student_id] = student
    print(f"\nДані студента (ID: {student_id}) успішно оновлено.")