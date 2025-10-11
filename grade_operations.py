# Над файлом працював Лях Дмитро
from ui_manager import get_valid_string #Імпортуємо фунцію для валідації данних

def top3_students_avg(journal: dict):
    """Виводить ТОП-3 студентів за загальним середнім балом."""
    if not journal:
        print("\nЖурнал порожній. Додайте студентів та оцінки.")
        return

    averages = {} #цей словник буде зберігати середні значення студентів
    for student_id, data in journal.items():
        perf = data.get("performance", {})
        grades = [grade for subj in perf.values() for grade in subj if isinstance(grade, (int, float))]
        if grades:
            avg = float(sum(grades)) / len(grades)
            averages[student_id] = avg

    if not averages:
        print("\nНемає оцінок для підрахунку.")
        return

    sorted_avg = sorted(averages.items(), key=lambda x: x[1], reverse=True) #key=lambda x: x[1] повертає значення для сортування без ключа, reverse=True робить список так що бы значення стояли від більшого до меншого
    print("\n--- ТОП-3 СТУДЕНТИ ЗА СЕРЕДНІМ БАЛОМ ---")
    for i, (student_id, avg) in enumerate(sorted_avg[:3], start=1):
        s = journal[student_id]
        print(f"{i}. {s['last_name']} {s['first_name']} ({student_id}) — AVG = {avg:.2f}")


def avg_one_student_all_subjects(journal: dict):
    """Обчислює середній бал конкретного студента за всіма дисциплінами."""
    if not journal:
        print("\nЖурнал порожній.")
        return

    student_id = get_valid_string("Введіть ID студента (наприклад, STU001): ")
    if student_id not in journal:
        print(f"Помилка: студента з ID {student_id} не знайдено.")
        return

    student = journal[student_id]
    performance = student.get("performance", {})

    if not performance:
        print(f"У студента {student['last_name']} {student['first_name']} немає жодних оцінок.")
        return

    all_grades = []
    for subject, grades in performance.items():# Беремо лише коректні числові оцінки
        valid_grades = [g for g in grades if isinstance(g, (int, float))]
        all_grades.extend(valid_grades)

    if not all_grades:
        print("Помилка: у студента немає коректних числових оцінок.")
        return

    avg = float(sum(all_grades)) / len(all_grades)
    print(f"\nAVG студента {student['last_name']} {student['first_name']} (усі дисципліни) = {avg:.2f}")


def avg_all_students_one_subject(journal: dict):
    """Обчислює середній бал усіх студентів за конкретною дисципліною."""
    if not journal:
        print("\nЖурнал порожній.")
        return

    subject = get_valid_string("Введіть назву дисципліни: ")
    all_grades = []

    for data in journal.values():
        grades = data.get("performance", {}).get(subject)
        if grades:
            valid = [g for g in grades if isinstance(g, (int, float))]
            all_grades.extend(valid)

    if not all_grades:
        print(f"Немає оцінок з дисципліни '{subject}' у журналі.")
        return

    avg = float(sum(all_grades)) / len(all_grades)
    print(f"\nСередній бал усіх студентів з дисципліни '{subject}' = {avg:.2f}")


def avg_all_students_all_subjects(journal: dict):
    """Обчислює середній бал усіх студентів за всіма дисциплінами."""
    if not journal:
        print("\nЖурнал порожній.")
        return

    all_grades = []
    for data in journal.values():
        for grades in data.get("performance", {}).values():
            valid = [g for g in grades if isinstance(g, (int, float))] #Перевірка типу данних
            all_grades.extend(valid)

    if not all_grades:
        print("Немає жодної оцінки в журналі.")
        return

    avg = float(sum(all_grades)) / len(all_grades)
    print(f"\nСередній бал усіх студентів за всіма дисциплінами = {avg:.2f}")