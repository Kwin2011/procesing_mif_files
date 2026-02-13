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
        Entry point for content processing.

        :param file_path: Path to the processed file.
        :param content: File content as string.
        :param signal_replacer: Optional replacer with replace(content) method.
        :return: Processed content.
        """
        return self.process_content(file_path, content, signal_replacer)

    def process_content(self, file_path, content, signal_replacer=None):
        """
        Executes processing steps in order:
        1. Load variables
        2. Replace variables
        3. Apply ContentReplacer
        4. Apply optional signal replacer
        """
        vars = self.settings_manager.get_meta_data()

        content = replace_variables(content, vars)

        replacer = ContentReplacer(content, vars)
        content = replacer.process()

        if signal_replacer:
            content = signal_replacer.replace(content)

        return content
