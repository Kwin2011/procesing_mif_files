import os
from file_handler import FileHandler
from content_processor import ContentProcessor
from signalWords import SignalWordsReplacer
from processing_logger import ProcessingLogger


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
        """Process file, write result and a log file. Returns path to processed file."""
        logger = ProcessingLogger(file_path)

        # 1. Read
        content = FileHandler.read_file(file_path)

        # 2. Process
        content = self.content_processor.process(file_path, content, self.signal_replacer)

        # 3. Collect logs from ContentReplacer (passed up via content_processor)
        if hasattr(self.content_processor, "last_logs"):
            logger.add_all(self.content_processor.last_logs)

        # 4. Write output file
        base, ext = os.path.splitext(file_path)
        result_path = f"{base}_processed{ext}"
        FileHandler.write_file(result_path, content)

        # 5. Save log
        log_path = logger.save()
        print(f"📋 Log saved: {log_path}")

        return result_path
