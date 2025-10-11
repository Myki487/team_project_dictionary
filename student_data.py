from utility import generate_next_id
from ui_manager import get_valid_string


def add_student(journal: dict):
    """Збирає дані про студента, генерує ID та додає запис до журналу."""
    new_id = generate_next_id(journal)

    print(f"\nДодавання нового студента. ID: {new_id}")

    # Введення ПІБ
    last_name = get_valid_string("Введіть Прізвище: ")
    first_name = get_valid_string("Введіть Ім'я: ")
    middle_name = get_valid_string("Введіть По-батькові: ")

    group = get_valid_string("Введіть Групу: ")

    # Введення курсу (1–6)
    while True:
        course_input = input("Введіть номер Курсу (1–6): ").strip()
        if course_input.isdigit():
            course = int(course_input)
            if 1 <= course <= 6:
                break
        print("Помилка: введіть число від 1 до 6 для курсу.")

    # Додавання у журнал
    journal[new_id] = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "group": group,
        "course": course,
        "performance": {}
    }

    print(f"\nСтудента {last_name} {first_name} {middle_name} (ID: {new_id}) успішно додано.")


def display_all_students(journal: dict):
    """Відображає відформатований список усіх студентів."""
    if not journal:
        print("\nЖурнал порожній. Немає студентів для відображення.")
        return

    print("\n----- ПОТОЧНИЙ СПИСОК СТУДЕНТІВ -----")
    print(f"{'ID':<8} | {'Прізвище':<15} | {'Ім\'я':<15} | {'По-батькові':<18} | {'Група':<10} | {'Курс':<5}")
    print("-" * 90)

    for student_id, data in journal.items():
        course_val = data.get('course', '-')
        print(f"{student_id:<8} | {data.get('last_name',''):<15} | {data.get('first_name',''):<15} | {data.get('middle_name',''):<18} | {data.get('group',''):<10} | {course_val:<5}")

    print("-" * 90)


def expel_student(journal: dict):
    """Видаляє студента з журналу за його ID після підтвердження."""
    if not journal:
        print("\nЖурнал порожній. Немає студентів для відрахування.")
        return

    display_all_students(journal)

    student_id = get_valid_string("Введіть ID студента для відрахування (наприклад, STU001): ")
    if student_id not in journal:
        print(f"\nСтудент з ID {student_id} не знайдений.")
        return

    student = journal[student_id]
    full_name = f"{student.get('last_name', '')} {student.get('first_name', '')} {student.get('middle_name', '')}".strip()
    confirm = input(f"Підтвердьте відрахування {full_name} (yes/no): ").strip().lower()

    if confirm in ('y', 'yes', 'т', 'так'):
        del journal[student_id]
        print(f"\nСтудент {full_name} (ID: {student_id}) відрахований.")
    else:
        print("\nВідмовлено. Студента не відраховано.")


def edit_student(journal: dict):
    """Редагує дані студента (ПІБ, група, курс)."""
    if not journal:
        print("\nЖурнал порожній. Немає студентів для редагування.")
        return

    display_all_students(journal)
    student_id = get_valid_string("Введіть ID студента для редагування (наприклад, STU001): ")
    if student_id not in journal:
        print(f"\nСтудент з ID {student_id} не знайдений.")
        return

    student = journal[student_id]
    print(f"\nПоточні дані для {student.get('last_name','')} {student.get('first_name','')} {student.get('middle_name','')} (ID: {student_id}):")
    print(f"  Прізвище: {student.get('last_name','')}")
    print(f"  Ім'я: {student.get('first_name','')}")
    print(f"  По-батькові: {student.get('middle_name','')}")
    print(f"  Група: {student.get('group','')}")
    print(f"  Курс: {student.get('course','')}")

    new_last = input(f"Введіть нове Прізвище (залиште порожнім щоб не змінювати) [{student.get('last_name','')}]: ").strip()
    new_first = input(f"Введіть нове Ім'я (залиште порожнім щоб не змінювати) [{student.get('first_name','')}]: ").strip()
    new_middle = input(f"Введіть нове По-батькові (залиште порожнім щоб не змінювати) [{student.get('middle_name','')}]: ").strip()
    new_group = input(f"Введіть нову Групу (залиште порожнім щоб не змінювати) [{student.get('group','')}]: ").strip()

    # Для курсу — даємо можливість перезаписати одразу, поки не введе коректно або не натисне Enter
    while True:
        tmp = input(f"Введіть новий Курс (число, залиште порожнім щоб не змінювати) [{student.get('course','')}]: ").strip()
        if tmp == "":
            new_course = ""  # залишити без змін
            break
        if tmp.isdigit():
            tmp_val = int(tmp)
            if 1 <= tmp_val <= 6:
                new_course = tmp
                break
        print("Помилка: введіть число від 1 до 6 для курсу або натисніть Enter щоб не змінювати.")

    if not any([new_last, new_first, new_middle, new_group, new_course]):
        print("\nНічого не змінено.")
        return

    # Підтвердження
    confirm = input("Підтвердити зміни? (yes/no): ").strip().lower()
    if confirm not in ('y', 'yes', 'т', 'так'):
        print("\nРедагування скасовано.")
        return

    # Оновлення даних
    if new_last:
        student['last_name'] = new_last
    if new_first:
        student['first_name'] = new_first
    if new_middle:
        student['middle_name'] = new_middle
    if new_group:
        student['group'] = new_group
    if new_course:
        # new_course гарантовано або пустий рядок або правильне число з діапазону 1-6
        student['course'] = int(new_course)

    journal[student_id] = student
    print(f"\nДані студента (ID: {student_id}) оновлено.")


def clear_all_students(journal: dict):
    """Очищує весь журнал студентів після підтвердження."""
    if not journal:
        print("\nЖурнал порожній. Немає студентів для видалення.")
        return

    confirm = input("Ви впевнені, що хочете видалити всіх студентів? (yes/no): ").strip().lower()
    if confirm in ('y', 'yes', 'т', 'так'):
        journal.clear()
        print("\nСписок студентів очищено.")
    else:
        print("\nОперацію скасовано.")
