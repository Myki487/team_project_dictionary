# Над файлом працював Бондар Олександр
from ui_manager import get_valid_string
from utility import find_student


# 🟢 Додавання нової дисципліни студенту
def add_subject(journal: dict, student_id: str = None, subject_name: str = None):
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

    if not subject_name:
        subject = get_valid_string("Введіть назву дисципліни: ")
    else:
        subject = subject_name

    # Якщо дисципліна вже є
    if subject in student.get("performance", {}):
        print(f"⚠️ Дисципліна '{subject}' вже існує у студента {student.get('last_name','')} {student.get('first_name','')}.")
        return subject

    # Створюємо нову дисципліну з порожнім списком оцінок
    student.setdefault("performance", {})[subject] = []
    print(f"✅ Дисципліну '{subject}' успішно додано студенту {student.get('last_name','')} {student.get('first_name','')}.")
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
        create = input("Хочете створити цю дисципліну? (yes/no): ").strip().lower()
        if create in ("т", "так", "y", "yes"):
            # Функція add_subject поверне назву дисципліни, яку ми використаємо нижче
            subject = add_subject(journal, student_id, subject_name=subject)

            # Якщо add_subject повернула None (помилка або відміна), виходимо
            if not subject:
                print("❌ Додавання оцінки скасовано (невдале створення дисципліни).")
                return
        else:
            print("❌ Додавання оцінки скасовано.")
            return

    # Додаємо оцінку
    while True:
        try:
            grade_input = input("Введіть оцінку (1–100): ").strip()
            grade = int(grade_input)
            if 1 <= grade <= 100:
                performance[subject].append(grade)
                print(f"✅ Оцінку {grade} додано з дисципліни '{subject}' студенту {student.get('last_name','')} {student.get('first_name','')} ({student_id}).")
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
        print(f"⚠️ У студента {student.get('last_name','')} {student.get('first_name','')} ще немає оцінок.")
        return

    print(f"\n📘 Успішність студента {student.get('last_name','')} {student.get('first_name','')} ({student_id}):")
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
    # Вибір індексу (один раз)
    try:
        index_input = input("Введіть номер оцінки для редагування (починаючи з 1): ").strip()
        index = int(index_input) - 1
    except ValueError:
        print("❌ Введено некоректне число.")
        return

    if not (0 <= index < len(performance[subject])):
        print("❌ Невірний номер оцінки.")
        return

    # Цикл для введення нової оцінки — дозволяє переробити введення, поки не буде коректного значення або поки не натиснуть Enter для скасування
    while True:
        new_input = input("Нова оцінка (1–100). Натисніть Enter щоб скасувати: ").strip()
        if new_input == "":
            print("❌ Редагування оцінки скасовано.")
            return
        if not new_input.isdigit():
            print("Помилка: введіть число від 1 до 100 або натисніть Enter щоб скасувати.")
            continue
        new_grade = int(new_input)
        if 1 <= new_grade <= 100:
            performance[subject][index] = new_grade
            print("✅ Оцінку змінено успішно.")
            break
        else:
            print("Помилка: оцінка має бути від 1 до 100.")


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
        print(f"⚠️ У студента {student.get('last_name','')} {student.get('first_name','')} немає дисциплін.")
        return

    print(f"Дисципліни студента: {', '.join(performance.keys())}")
    subject = get_valid_string("Введіть назву дисципліни, яку потрібно видалити: ")

    if subject not in performance:
        print(f"❌ Дисципліну '{subject}' не знайдено.")
        return

    confirm = input(f"Ви впевнені, що хочете видалити '{subject}' разом з усіма оцінками? (yes/no): ").strip().lower()
    if confirm in ("т", "так", "y", "yes"):
        del performance[subject]
        print(f"🗑️  Дисципліну '{subject}' успішно видалено у студента {student.get('last_name','')} {student.get('first_name','')}.")
    else:
        print("❌ Видалення скасовано.")
