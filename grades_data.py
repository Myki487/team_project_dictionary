from ui_manager import get_valid_string
from utility import find_student


def add_subject(journal: dict, student_id: str = None):
    """Додає новий предмет для конкретного студента."""
    if not journal:
        print("\n⚠️ Журнал порожній.")
        return

    # Якщо ID студента не передано — запитуємо вручну
    if not student_id:
        student_id = get_valid_string("Введіть ID студента: ")

    student = find_student(journal, student_id)
    if not student:
        print(f"❌ Студента з ID '{student_id}' не знайдено.")
        return

    subject = get_valid_string("Введіть назву предмету: ")

    # Якщо предмет уже є
    if subject in student["performance"]:
        print(f"⚠️ Предмет '{subject}' вже існує у студента {student['last_name']} {student['first_name']}.")
        return subject

    # Створюємо новий предмет із порожнім списком оцінок
    student["performance"][subject] = []
    print(f"✅ Предмет '{subject}' успішно додано студенту {student['last_name']} {student['first_name']}.")
    return subject


def add_grade(journal: dict):
    """Додає оцінку студенту за предмет (по ID)."""
    if not journal:
        print("\n⚠️ У журналі немає студентів.")
        return

    student_id = get_valid_string("Введіть ID студента: ")
    student = find_student(journal, student_id)

    if not student:
        print(f"❌ Студента з ID '{student_id}' не знайдено.")
        return

    # Отримуємо або створюємо розділ "performance"
    performance = student.setdefault("performance", {})
    subject = get_valid_string("Введіть назву предмету: ")

    # Якщо предмет не знайдено — пропонуємо створити
    if subject not in performance:
        print(f"⚠️ Предмет '{subject}' не знайдено у цього студента.")
        create = input("Хочете створити цей предмет? (так/ні): ").strip().lower()
        if create in ("так", "y", "yes"):
            subject = add_subject(journal, student_id)
        else:
            print("❌ Додавання оцінки скасовано.")
            return

    # Додаємо оцінку
    while True:
        try:
            grade = int(input("Введіть оцінку (1–100): ").strip())
            if 1 <= grade <= 100:
                performance[subject].append(grade)
                print(f"✅ Оцінку {grade} додано з предмету '{subject}' студенту {student['last_name']} {student['first_name']}.")
                break
            else:
                print("Помилка: оцінка має бути від 1 до 100.")
        except ValueError:
            print("Помилка: введіть число.")


def view_student_grades(journal: dict):
    """Переглядає оцінки студента (по ID) та середнє арифметичне."""
    if not journal:
        print("\n⚠️ У журналі немає студентів.")
        return

    student_id = get_valid_string("Введіть ID студента: ")
    student = find_student(journal, student_id)

    if not student:
        print(f"❌ Студента з ID '{student_id}' не знайдено.")
        return

    performance = student.get("performance", {})
    if not performance:
        print(f"⚠️ У студента {student['last_name']} {student['first_name']} ще немає оцінок.")
        return

    print(f"\n📘 Успішність студента {student['last_name']} {student['first_name']}:")
    for subject, marks in performance.items():
        if marks:
            avg = sum(marks) / len(marks)
            print(f"  {subject}: {marks} → середнє: {avg:.2f}")
        else:
            print(f"  {subject}: (оцінок немає)")

    print("\n✅ Перегляд завершено.")


def edit_grade(journal: dict):
    """Редагує оцінку студента (по ID)."""
    student_id = get_valid_string("Введіть ID студента: ")
    student = find_student(journal, student_id)

    if not student:
        print(f"❌ Студента з ID '{student_id}' не знайдено.")
        return

    performance = student.get("performance", {})
    if not performance:
        print("⚠️ У студента немає предметів.")
        return

    print("Предмети:", ", ".join(performance.keys()))
    subject = get_valid_string("Введіть предмет: ")

    if subject not in performance:
        print(f"❌ Предмет '{subject}' не знайдено.")
        return

    if not performance[subject]:
        print("⚠️ Оцінок із цього предмету ще немає.")
        return

    print(f"Поточні оцінки: {performance[subject]}")
    try:
        index = int(input("Введіть номер оцінки для редагування (починаючи з 1): ")) - 1
        if 0 <= index < len(performance[subject]):
            new_grade = int(input("Нова оцінка (1–12): "))
            if 1 <= new_grade <= 100:
                performance[subject][index] = new_grade
                print("✅ Оцінку змінено успішно.")
            else:
                print("❌ Оцінка має бути в діапазоні 1–100.")
        else:
            print("❌ Невірний номер оцінки.")
    except ValueError:
        print("❌ Введено некоректне число.")


def delete_grade(journal: dict):
    """Видаляє оцінку студента (по ID)."""
    student_id = get_valid_string("Введіть ID студента: ")
    student = find_student(journal, student_id)

    if not student:
        print(f"❌ Студента з ID '{student_id}' не знайдено.")
        return

    performance = student.get("performance", {})
    if not performance:
        print("⚠️ У студента немає предметів.")
        return

    print("Предмети:", ", ".join(performance.keys()))
    subject = get_valid_string("Введіть предмет: ")

    if subject not in performance:
        print(f"❌ Предмет '{subject}' не знайдено.")
        return

    if not performance[subject]:
        print("⚠️ Оцінок із цього предмету немає.")
        return

    print(f"Поточні оцінки: {performance[subject]}")
    try:
        index = int(input("Введіть номер оцінки для видалення (починаючи з 1): ")) - 1
        if 0 <= index < len(performance[subject]):
            deleted = performance[subject].pop(index)
            print(f"✅ Оцінку {deleted} видалено.")
        else:
            print("❌ Невірний номер оцінки.")
    except ValueError:
        print("❌ Введено некоректне число.")
