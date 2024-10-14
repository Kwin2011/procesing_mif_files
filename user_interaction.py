from signalWords import get_language_code, is_language_code_valid

class UserInteraction:
    def __init__(self, settings):
        self.settings = settings

    def ask_to_edit_settings(self):
        action = input("Хочете змінити налаштування? Введіть + для змін або шлях до файлу для продовження: ").strip()
        if action == '+':
            for key in self.settings.variables.keys():
                new_value = self.ask_for_variable(key, self.settings.variables[key])
                self.settings.update_variable(key, new_value)
        else:
            return action

    def ask_for_variable(self, key, current_value):
        new_value = input(f"Введіть нове значення для {key} (поточне: {current_value}): ").strip()
        return new_value if new_value else current_value

    def ask_to_continue(self):
        return input("Обробляти інший файл? (+ для продовження, - для виходу): ").strip() == '+'

    def display_settings(self):
        print("Поточні налаштування:")
        for key, value in self.settings.variables.items():
            print(f"{key}: {value}")
        print("______________________________")

    def ask_to_change_language_code(self, found_code):
        answer = input(f"Мовний код знайдено: {found_code}. Змінити його? (+ для зміни, будь-яка інша клавіша для підтвердження): ").strip()
        return answer == '+'

    def ask_for_new_language_code(self):
        while True:
            new_language_code = input("Введіть новий мовний код: ").strip().upper()

            # Перевірити, чи введений код є валідним
            if is_language_code_valid(new_language_code):
                return new_language_code
            else:
                print("Невірний мовний код.")
                show_list = input("Показати список доступних кодів? (+ для показу, будь-яка інша клавіша для повторної спроби): ").strip()
                if show_list == '+':
                    self.display_language_code_list()

    def display_language_code_list(self):
        """Показати список доступних мовних кодів."""
        lang_codes = list(get_language_code())
        lang_codes.sort()
        print("Доступні мовні коди:")
        for i in range(0, len(lang_codes), 10):  # Виводимо по 10 кодів в рядок
            row = "{:<5}" * min(10, len(lang_codes) - i)
            print(row.format(*lang_codes[i:i + 10]))
