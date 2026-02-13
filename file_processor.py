import os
from file_handler import FileHandler
from content_processor import ContentProcessor
from signalWords import SignalWordsReplacer


class FileProcessor:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.content_processor = ContentProcessor(settings_manager)

        lang_code = self.settings_manager.get_meta_data().get("languageCode", None)

        if SignalWordsReplacer.is_language_code_valid(lang_code):
            self.signal_replacer = SignalWordsReplacer(lang_code)
        else:
            print(f"⚠ Language code '{lang_code}' not supported — skipping signal word replacement")
            self.signal_replacer = None

    def process(self, file_path: str) -> str:
        """Process file and return path to processed file"""
        # 1. Читаємо файл
        content = FileHandler.read_file(file_path)

        # 2. Обробляємо контент
        content = self.content_processor.process(file_path, content, self.signal_replacer)

        # 3. Формуємо новий шлях
        base, ext = os.path.splitext(file_path)
        result_path = f"{base}_processed{ext}"

        # 4. Записуємо новий файл
        FileHandler.write_file(result_path, content)

        return result_path
