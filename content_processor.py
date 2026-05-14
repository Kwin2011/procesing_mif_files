from ContentReplacer import ContentReplacer
from ContentVariableReplacer import replace_variables


class ContentProcessor:
    """
    Orchestrates the full content processing workflow.
    After process() completes, logs are available in self.last_logs.
    """

    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.last_logs = []

    def process(self, file_path, content, signal_replacer=None):
        return self.process_content(file_path, content, signal_replacer)

    def process_content(self, file_path, content, signal_replacer=None):
        vars = self.settings_manager.get_meta_data()

        content = replace_variables(content, vars)

        replacer = ContentReplacer(content, vars)
        content = replacer.process()

        # Store logs so FileProcessor can pick them up
        self.last_logs = replacer.get_logs()

        if signal_replacer:
            content = signal_replacer.replace(content)

        return content
