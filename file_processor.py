import os
from file_handler import FileHandler
from content_processor import ContentProcessor
from signalWords import SignalWordsReplacer
from processing_logger import ProcessingLogger


class FileProcessor:
    """
    Processes MIF files and records a full processing log.

    Integrates with ProcessingLogger to persist per-file history,
    including settings snapshot, ContentReplacer logs, and outcome.
    """

    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.content_processor = ContentProcessor(settings_manager)
        self.logger = ProcessingLogger()

        lang_code = self.settings_manager.get_meta_data().get("languageCode", None)

        if SignalWordsReplacer.is_language_code_valid(lang_code):
            self.signal_replacer = SignalWordsReplacer(lang_code)
        else:
            print(f"⚠ Language code '{lang_code}' not supported — skipping signal word replacement")
            self.signal_replacer = None

    def process(self, file_path: str) -> str:
        """
        Process file and return path to processed file.

        Saves a detailed log entry regardless of success or failure.

        :param file_path: Path to the input MIF file.
        :return: Path to the output file.
        :raises Exception: Re-raises any processing exception after logging.
        """
        settings_snapshot = self.settings_manager.get_meta_data()
        content_logs: list[str] = []
        result_path = None

        try:
            # 1. Read the file
            content = FileHandler.read_file(file_path)

            # 2. Process the content (collect logs from ContentReplacer)
            content, content_logs = self.content_processor.process_with_logs(
                file_path, content, self.signal_replacer
            )

            # 3. Build the output path
            base, ext = os.path.splitext(file_path)
            result_path = f"{base}_processed{ext}"

            # 4. Write the result
            FileHandler.write_file(result_path, content)

            # 5. Save success log
            log_path = self.logger.save_log(
                file_path=file_path,
                result_path=result_path,
                status="success",
                settings_snapshot=settings_snapshot,
                content_logs=content_logs,
            )
            print(f"📋 Log saved: {log_path}")

            return result_path

        except Exception as e:
            # Save error log, then re-raise
            self.logger.save_log(
                file_path=file_path,
                result_path=None,
                status="error",
                settings_snapshot=settings_snapshot,
                content_logs=content_logs,
                error_message=str(e),
            )
            raise
