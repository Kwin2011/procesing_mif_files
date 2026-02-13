import re
from ContentReplacer import ContentReplacer

class VariableReplacer:
    """
    Replaces predefined variables in content based on SettingsManager.
    """

    def __init__(self, settings_manager):
        """
        Args:
            settings_manager: Instance of SettingsManager with dynamic fields.
        """
        self.settings = settings_manager

    def replace_variables(self, content):
        """
        Apply variable replacements to the given content.

        Replacements are based on the following mapping:
            - 'SCHKA1Number' -> 'KaNumber'
            - 'SCHDeliveryDate' -> 'deliveryDate'
            - 'SCHKA1Date' -> 'KaDate'
            - 'SCHVersion' -> 'KaVersion'
            - 'SCHNameReleased' -> 'KaNameReleased'

        Args:
            content (str): Original file content

        Returns:
            str: Content with variables replaced
        """
        # Динамічне додавання змінних
        variables = {
            'SCHKA1Number': 'KaNumber',
            'SCHDeliveryDate': 'deliveryDate',
            'SCHKA1Date': 'KaDate',
            'SCHVersion': 'KaVersion',
            'SCHNameReleased': 'KaNameReleased'
        }

        settings = self.settings.get_meta_data()

        # Створюємо ContentReplacer для обробки патернів
        replacer = ContentReplacer(content, {})

        for var_name, setting_key in variables.items():
            pattern = r'(<VariableFormat\s*<VariableName\s*`' + var_name + r'\'?>\s*<VariableDef\s*)(`.*?)(\'?>)'
            replacement = rf"\1`{settings.get(setting_key, '')}'>"
            replacer._perform_and_log_replacement(
                pattern, 
                replacement, 
                f"Variable replacement: {var_name}"
            )

        # Повертаємо оброблений контент
        return replacer.process()
