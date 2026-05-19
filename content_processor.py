from ContentReplacer import ContentReplacer
from ContentVariableReplacer import replace_variables


class ContentProcessor:
    """
    Orchestrates the full content processing workflow:
    - loads metadata variables,
    - applies variable replacements,
    - runs structured content replacements,
    - optionally applies signal-based replacements.
    """

    def __init__(self, settings_manager):
        """
        :param settings_manager: Object that provides metadata via get_meta_data().
        """
        self.settings_manager = settings_manager

    def process(self, file_path, content, signal_replacer=None):
        """
        Entry point for content processing. Returns processed content only.

        :param file_path: Path to the processed file.
        :param content: File content as string.
        :param signal_replacer: Optional replacer with replace(content) method.
        :return: Processed content string.
        """
        content, _ = self.process_with_logs(file_path, content, signal_replacer)
        return content

    def process_with_logs(self, file_path, content, signal_replacer=None):
        """
        Executes processing steps in order and returns both content and logs.

        Steps:
        1. Load variables from settings
        2. Replace variables via ContentVariableReplacer
        3. Apply ContentReplacer (structured replacements with logging)
        4. Apply optional signal replacer

        :param file_path: Path to the processed file.
        :param content: File content as string.
        :param signal_replacer: Optional replacer with replace(content) method.
        :return: Tuple (processed_content: str, logs: list[str])
        """
        vars = self.settings_manager.get_meta_data()

        content = replace_variables(content, vars)

        replacer = ContentReplacer(content, vars)
        content = replacer.process()
        logs = replacer.get_logs()

        if signal_replacer:
            content = signal_replacer.replace(content)
            logs.append("[INFO] Signal word replacement applied.")

        return content, logs
