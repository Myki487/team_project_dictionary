#Файл розроблений Годуном Миколою
import json
import os

def load_journal(filename: str) -> dict:
    """Завантажує словник журналу з JSON-файлу."""
    if not os.path.exists(filename):
        # Повертаємо порожній словник, якщо файл не існує
        return {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Помилка: Файл журналу пошкоджений. Розпочинаємо з порожнього журналу.")
        return {}

def save_journal(journal: dict, filename: str):
    """Зберігає поточний словник журналу у JSON-файл."""
    # Перевірка чи директорія 'data' існує
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        # ensure_ascii=False для коректного зберігання українських символів
        json.dump(journal, f, indent=4, ensure_ascii=False)