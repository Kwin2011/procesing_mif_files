import os  # Додано імпорт os
import re
from replacements import replace_variables
from signalWords import replace_signal_words, is_language_code_valid


class FileProcessor:
    def __init__(self, settings, user_interaction):
        self.settings = settings
        self.user_interaction = user_interaction

    def is_file_valid(self, file_path):
        return os.path.isfile(file_path)

    def get_language_code_from_filename(self, filename):
        match = re.search(r'_(\w{2})_', filename)
        if match:
            return match.group(1).upper()  # Повернути код мови у верхньому регістрі
        return None

    def replace_variables_in_file(self, input_file, output_file):
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
            content = replace_variables(content, self.settings.variables)  # Замінити змінні
            content = replace_signal_words(content, self.settings.variables['languageCode'])  # Замінити сигнальні слова

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)

    def process_file(self, file_path):
        # Автоматично визначити мовний код
        language_code = self.get_language_code_from_filename(file_path)
        if language_code:
            print(f"Знайдено мовний код у файлі: {language_code}")
            # Запитати у користувача підтвердити або змінити мовний код
            if self.user_interaction.ask_to_change_language_code(language_code):
                new_language_code = self.user_interaction.ask_for_new_language_code()
                self.settings.update_variable('languageCode', new_language_code)
            else:
                self.settings.update_variable('languageCode', language_code)
        else:
            print("Мовний код не знайдено у файлі. Використовується стандартний код.")

        output_filename = f"_{os.path.basename(file_path)}"
        output_path = os.path.join(os.path.dirname(file_path), output_filename)

        self.replace_variables_in_file(file_path, output_path)
        print(f"Обробка завершена! Результат збережено у {output_path}")
