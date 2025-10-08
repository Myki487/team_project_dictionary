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


def edit_student(journal: dict):
    """
    Редагує дані студента: прізвище, ім'я, група.
    Користувач може пропустити поле (натиснути Enter) щоб залишити поточне значення.
    """
    if not journal:
        print("\nЖурнал порожній. Немає студентів для редагування.")

        # Відображає повний список усіх студентів та їхні дані.
        display_all_students(journal)

        if not journal:
            print("\nЖурнал порожній. Немає студентів для відображення.")
            return

        print("\n===== ПОВНИЙ СПИСОК СТУДЕНТІВ =====")

        for student_id, data in journal.items():
            first = data.get('first_name', '')
            last = data.get('last_name', '')
            group = data.get('group', '')
            performance = data.get('performance', {}) or {}

            # Основний заголовок по студентах
            print("-" * 70)
            print(f"ID: {student_id} | {last} {first} | Група: {group}")

            # Успішність
            if not performance:
                print("  Успішність: немає записів (немає оцінок)")
                continue

            total_sum = 0
            total_count = 0
            print("  Успішність:")
            for subj, grades in performance.items():
                # Очікуємо, що grades — список чисел або порожній список
                if not grades:
                    print(f"    - {subj}: немає оцінок")
                    continue
                # Вивести оцінки через кому
                grades_str = ", ".join(str(g) for g in grades)
                # Середній по предмету
                try:
                    subj_avg = sum(grades) / len(grades)
                except Exception:
                    subj_avg = None
                if subj_avg is not None:
                    print(f"    - {subj}: [{grades_str}] (середній: {subj_avg:.2f})")
                    total_sum += sum(grades)
                    total_count += len(grades)
                else:
                    print(f"    - {subj}: [{grades_str}]")

            # Загальний середній по студенту
            if total_count:
                overall_avg = total_sum / total_count
                print(f"  Загальний середній бал: {overall_avg:.2f}")
            else:
                print("  Загальний середній бал: немає оцінок")

        print("-" * 70)

    student_id = get_valid_string("Введіть ID студента для редагування (наприклад, STU001): ")
    if student_id not in journal:
        print(f"\nСтудент з ID {student_id} не знайдений.")
        return

    student = journal[student_id]
    print(f"\nПоточні дані для {student['first_name']} {student['last_name']} (ID: {student_id}):")
    print(f"  Прізвище: {student['last_name']}")
    print(f"  Ім'я: {student['first_name']}")
    print(f"  Група: {student['group']}")

    # Запитати нові значення (порожнє = без змін)
    new_last = input(f"Введіть нове Прізвище (залиште порожнім щоб не змінювати) [{student['last_name']}]: ").strip()
    new_first = input(f"Введіть нове Ім'я (залиште порожнім щоб не змінювати) [{student['first_name']}]: ").strip()
    new_group = input(f"Введіть нову Групу (залиште порожнім щоб не змінювати) [{student['group']}]: ").strip()

    if not new_last and not new_first and not new_group:
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

    journal[student_id] = student
    print(f"\nДані студента (ID: {student_id}) успішно оновлено.")