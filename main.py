# Імпортуємо функції диспетчера з модулів
from file_manager import load_journal, save_journal
from ui_manager import main_menu_view, handle_student_actions

# --- КОНФІГУРАЦІЯ ТА ДАНІ ---
JOURNAL_FILE = 'data/journal.json'
GLOBAL_JOURNAL = {} # Змінна для зберігання словника в пам'яті

def main():
    global GLOBAL_JOURNAL
    print("Запуск електронного журналу...")
    
    # 1. ЗАВАНТАЖЕННЯ ДАНИХ
    GLOBAL_JOURNAL = load_journal(JOURNAL_FILE)
    if GLOBAL_JOURNAL:
        print(f"Дані завантажено успішно. ({len(GLOBAL_JOURNAL)} студентів).")
    else:
        print("Розпочинаємо з порожнього журналу.")
        
    # 2. ГОЛОВНИЙ ЦИКЛ ПРОГРАМИ
    while True:
        choice = main_menu_view() 

        if choice == '1':
            # Передаємо управління обробнику меню 1
            handle_student_actions(GLOBAL_JOURNAL) 
        elif choice == '0':
            break # Вихід із циклу
        else:
            print("\nЦя опція буде реалізована на наступному етапі. Будь ласка, оберіть 1 або 0.")

    # 3. ЗБЕРЕЖЕННЯ ДАНИХ ТА ВИХІД
    try:
        save_journal(GLOBAL_JOURNAL, JOURNAL_FILE)
        print(f"\nДані успішно збережено у {JOURNAL_FILE}. До побачення!")
    except Exception as e:
        print(f"\nПомилка збереження даних: {e}")

if __name__ == "__main__":
    main()