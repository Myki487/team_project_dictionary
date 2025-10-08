# --- Валідація для введення ---

def get_valid_string(prompt: str) -> str:
    """Запитує у користувача непорожній рядок."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Помилка: Ввід не може бути порожнім. Спробуйте ще раз.")

def get_user_choice(max_option: int) -> str:
    """Запитує коректний вибір у меню (від 0 до max_option)."""
    while True:
        choice = input("Оберіть пункт: ").strip()
        if choice.isdigit():
            num_choice = int(choice)
            if 0 <= num_choice <= max_option:
                return choice
        print(f"Помилка: Некоректний вибір. Будь ласка, введіть число від 0 до {max_option}.")

# --- Відображення меню ---

def main_menu_view() -> str:
    """Відображає головне меню."""
    print("\n----- ГОЛОВНЕ МЕНЮ ЕЛЕКТРОННОГО ЖУРНАЛУ -----")
    print("1. Дії над записами студента")
    print("2. Дії над записами оцінок (Наступний етап)")
    print("3. Сортування журналу (Наступний етап)")
    print("0. Зберегти та Вийти")
    return get_user_choice(3)

def student_menu_view() -> str:
    """Відображає меню дій над студентами."""
    print("\n--- МЕНЮ 1: ДІЇ НАД СТУДЕНТАМИ ---")
    print("1. Додати студента")
    print("2. Відрахувати студента (Наступний етап)")
    print("3. Редагувати дані студента (Наступний етап)")
    print("4. Відобразити УСІХ студентів (Повний список)")
    print("5. Відобразити успішність конкретного студента (Наступний етап)")
    print("0. У попереднє меню...") 
    return get_user_choice(5)

# --- Функції для меню (диспетчери) ---

def handle_student_actions(journal: dict):
    """Керує циклом та маршрутизацією для меню дій над студентами."""
    
    from student_data import add_student, display_all_students 
    
    while True:
        choice = student_menu_view()

        if choice == '1':
            add_student(journal)
        elif choice == '4':
            display_all_students(journal)
        elif choice == '0':
            break 
        else:
            print("\nЦя опція буде реалізована на наступному етапі.")