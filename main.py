import io
import sys

from settings import Settings
from file_processor import FileProcessor
from user_interaction import UserInteraction

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    # Ініціалізація об'єктів
    settings = Settings()
    user_interaction = UserInteraction(settings)
    file_processor = FileProcessor(settings, user_interaction)

    while True:
        # Показати поточні налаштування
        user_interaction.display_settings()

        # Запит у користувача
        file_path = user_interaction.ask_to_edit_settings()

        if file_path:
            # Перевірка існування файлу
            if not file_processor.is_file_valid(file_path):
                print("Файл не знайдено. Спробуйте ще раз.")
                continue

            # Обробка файлу
            file_processor.process_file(file_path)

        # Запит на продовження
        if not user_interaction.ask_to_continue():
            break

if __name__ == "__main__":
    main()
