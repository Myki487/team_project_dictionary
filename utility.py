def generate_next_id(journal: dict) -> str:
    """Генерує наступний унікальний ID студента (наприклад, STU001, STU002)."""

    existing_ids = list(journal.keys())
    max_num = 0

    # Шукаємо найбільший числовий суфікс серед існуючих ID
    for student_id in existing_ids:
        if student_id.startswith('STU') and student_id[3:].isdigit():
            try:
                num = int(student_id[3:])
                if num > max_num:
                    max_num = num
            except ValueError:
                continue

    # Форматуємо наступний номер, забезпечуючи три розряди (наприклад, 005)
    next_num = max_num + 1
    new_id = f"STU{next_num:03d}"

    return new_id

def find_student(journal: dict, student_id: str) -> dict | None:
    """Знаходить студента за ID та повертає словник його даних."""
    return journal.get(student_id)