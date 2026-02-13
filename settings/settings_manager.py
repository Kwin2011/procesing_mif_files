import os
import re
import json
from file_handler import FileHandler
from languageCodeDetector import LanguageCodeDetector


class SettingsManager:
    """
    Manages application settings for MIF file processing.

    Responsibilities:
    - Load settings from a JSON file or create default settings.
    - Provide metadata including dynamic KaVersion and languageCode.
    - Update editable settings and save changes to disk.
    """

    def __init__(self, config_path="settings/settings.json", target_path=None):
        """
        Initialize SettingsManager.

        :param config_path: Path to the JSON configuration file.
        :param target_path: Path to the target MIF file (used for dynamic fields).
        """
        self.config_path = config_path
        self.target_path = target_path
        self.language_detector = LanguageCodeDetector()
        self.meta_data = self._load_or_create_settings()

    def _load_or_create_settings(self) -> dict:
        """
        Load settings from the JSON file if it exists,
        otherwise create default settings and save them.

        :return: Dictionary of settings.
        """
        defaults = {
            "deliveryDate": "empty",
            "KaNumber": "empty",
            "KaDate": "empty",
            "KaNameReleased": "Acolad Switzerland AG"
        }

        # Load existing settings
        if FileHandler.is_file_valid(self.config_path):
            content = FileHandler.read_file(self.config_path)
            try:
                loaded_data = json.loads(content)
            except Exception:
                loaded_data = defaults.copy()
            return loaded_data

        # Create and save defaults if file does not exist
        self._save_settings(defaults)
        return defaults

    def get_meta_data(self) -> dict:
        """
        Get a copy of the metadata including dynamic fields.

        :return: Dictionary of metadata.
        """
        meta_data = self.meta_data.copy()
        meta_data["KaVersion"] = self._get_dynamic_ka_version()
        meta_data["languageCode"] = self._get_dynamic_language_code()
        return meta_data

    def _get_dynamic_ka_version(self) -> str:
        """Extract KaVersion dynamically from the target file name."""
        if not self.target_path:
            return "None"
        match = re.search(r'(\d{2})\.\w+$', self.target_path)
        return match.group(1) if match else "None"

    def _get_dynamic_language_code(self) -> str:
        """Detect language code from the target file using LanguageCodeDetector."""
        if self.target_path:
            detected = self.language_detector.detect_languages(self.target_path)
            return detected if detected is not None else "None"
        return "None"

    def update_setting(self, key: str, value: str) -> None:
        """
        Update a setting and save it to disk.

        Dynamic fields 'KaVersion' and 'languageCode' cannot be modified.

        :param key: Setting key to update.
        :param value: New value.
        :raises ValueError: If attempting to modify a dynamic field.
        """
        if key in {"KaVersion", "languageCode"}:
            raise ValueError(f"Field '{key}' is dynamically determined and cannot be modified")
        self.meta_data[key] = value
        self._save_settings(self.meta_data)

    def _save_settings(self, data: dict) -> None:
        """
        Save settings dictionary to the JSON file, creating folders if needed.

        :param data: Dictionary to save.
        """
        folder = os.path.dirname(self.config_path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        FileHandler.write_file(self.config_path, json.dumps(data, indent=4))
