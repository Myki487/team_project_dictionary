from ui_manager import get_valid_string
from utility import find_student


# 🟢 Додавання нової дисципліни студенту
def add_subject(journal: dict, student_id: str = None):
    """Додає нову дисципліну для конкретного студента."""
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

    subject = get_valid_string("Введіть назву дисципліни: ")

    # Якщо дисципліна вже є
    if subject in student["performance"]:
        print(f"⚠️ Дисципліна '{subject}' вже існує у студента {student['last_name']} {student['first_name']}.")
        return subject

    # Створюємо нову дисципліну з порожнім списком оцінок
    student["performance"][subject] = []
    print(f"✅ Дисципліну '{subject}' успішно додано студенту {student['last_name']} {student['first_name']}.")
    return subject


# 🟢 Додавання оцінки студенту за певну дисципліну
def add_grade(journal: dict):
    """Додає оцінку студенту за дисципліну (по ID)."""
    if not journal:
        print("\n⚠️ У журналі немає студентів.")
        return

    student_id = get_valid_string("Введіть ID студента: ")
    student = find_student(journal, student_id)

    if not student:
        print(f"❌ Студента з ID '{student_id}' не знайдено.")
        return

    performance = student.setdefault("performance", {})
    subject = get_valid_string("Введіть назву дисципліни: ")

    # Якщо дисципліна не знайдена — пропонуємо створити
    if subject not in performance:
        print(f"⚠️ Дисципліну '{subject}' не знайдено у цього студента.")
        create = input("Хочете створити цю дисципліну? (так/ні): ").strip().lower()
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
                print(f"✅ Оцінку {grade} додано з дисципліни '{subject}' студенту {student['last_name']} {student['first_name']}.")
                break
            else:
                print("Помилка: оцінка має бути від 1 до 100.")
        except ValueError:
            print("Помилка: введіть число.")


# 🟢 Перегляд усіх оцінок студента та середнього балу
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

    print(f"\n📘 Успішність студента {student['last_name']} {student['first_name']} ({student_id}):")
    for subject, marks in performance.items():
        if marks:
            avg = sum(marks) / len(marks)
            print(f"  {subject}: {marks} → середнє: {avg:.2f}")
        else:
            print(f"  {subject}: (оцінок немає)")

    print("\n✅ Перегляд завершено.")


# 🟢 Редагування конкретної оцінки студента
def edit_grade(journal: dict):
    """Редагує оцінку студента (по ID)."""
    student_id = get_valid_string("Введіть ID студента: ")
    student = find_student(journal, student_id)

    if not student:
        print(f"❌ Студента з ID '{student_id}' не знайдено.")
        return

    performance = student.get("performance", {})
    if not performance:
        print("⚠️ У студента немає дисциплін.")
        return

    print("Дисципліни:", ", ".join(performance.keys()))
    subject = get_valid_string("Введіть назву дисципліни: ")

    if subject not in performance:
        print(f"❌ Дисципліну '{subject}' не знайдено.")
        return

    if not performance[subject]:
        print("⚠️ Оцінок із цієї дисципліни ще немає.")
        return

    print(f"Поточні оцінки: {performance[subject]}")
    try:
        index = int(input("Введіть номер оцінки для редагування (починаючи з 1): ")) - 1
        if 0 <= index < len(performance[subject]):
            new_grade = int(input("Нова оцінка (1–100): "))
            if 1 <= new_grade <= 100:
                performance[subject][index] = new_grade
                print("✅ Оцінку змінено успішно.")
            else:
                print("❌ Оцінка має бути в діапазоні 1–100.")
        else:
            print("❌ Невірний номер оцінки.")
    except ValueError:
        print("❌ Введено некоректне число.")


# 🟢 Видалення конкретної оцінки студента
def delete_grade(journal: dict):
    """Видаляє оцінку студента (по ID)."""
    student_id = get_valid_string("Введіть ID студента: ")
    student = find_student(journal, student_id)

    if not student:
        print(f"❌ Студента з ID '{student_id}' не знайдено.")
        return

    performance = student.get("performance", {})
    if not performance:
        print("⚠️ У студента немає дисциплін.")
        return

    print("Дисципліни:", ", ".join(performance.keys()))
    subject = get_valid_string("Введіть назву дисципліни: ")

    if subject not in performance:
        print(f"❌ Дисципліну '{subject}' не знайдено.")
        return

    if not performance[subject]:
        print("⚠️ Оцінок із цієї дисципліни немає.")
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


# 🟢 Видалення дисципліни з усіма оцінками
def delete_subject(journal: dict):
    """Видаляє дисципліну разом із усіма оцінками у студента."""
    if not journal:
        print("\n⚠️ Журнал порожній.")
        return

    student_id = get_valid_string("Введіть ID студента: ")
    student = find_student(journal, student_id)

    if not student:
        print(f"❌ Студента з ID '{student_id}' не знайдено.")
        return

    performance = student.get("performance", {})
    if not performance:
        print(f"⚠️ У студента {student['last_name']} {student['first_name']} немає дисциплін.")
        return

    print(f"Дисципліни студента: {', '.join(performance.keys())}")
    subject = get_valid_string("Введіть назву дисципліни, яку потрібно видалити: ")

    if subject not in performance:
        print(f"❌ Дисципліну '{subject}' не знайдено.")
        return

    confirm = input(f"Ви впевнені, що хочете видалити '{subject}' разом з усіма оцінками? (так/ні): ").strip().lower()
    if confirm in ("так", "y", "yes"):
        del performance[subject]
        print(f"🗑️ Дисципліну '{subject}' успішно видалено у студента {student['last_name']} {student['first_name']}.")
    else:
        print("❌ Видалення скасовано.")
