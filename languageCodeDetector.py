import re
from typing import Optional

class LanguageCodeDetector:
    """
    Detects language codes embedded in filenames using predefined mappings and heuristic rules.
    """

    def __init__(self):
        """
        Initializes the detector with a dictionary of known language codes mapped to their full names.
        """
        self.language_codes = {
            "EN": "English", "ENUS": "English (US)", "ENUK": "English (UK)",
            "US": "English (US)", "UK": "English (UK)",
            "DE": "German", "ES": "Spanish", "FR": "French", "IT": "Italian",
            "PT": "Portuguese", "PTBR": "Portuguese (Brazil)", "BR": "Portuguese (Brazil)",
            "NL": "Dutch", "RU": "Russian", "PL": "Polish",
            "SV": "Swedish", "NO": "Norwegian", "DA": "Danish", "FI": "Finnish",
            "CZ": "Czech", "SK": "Slovak", "HU": "Hungarian",
            "AR": "Arabic", "ZH": "Chinese", "CN": "Chinese",
            "CHS": "Chinese (Simplified)", "CHT": "Chinese (Traditional)",
            "JA": "Japanese", "KO": "Korean",
            # Additional codes from signalWords
            "BG": "Bulgarian", "MY": "Malay", "CA": "Catalan", "ZF": "Chinese (Traditional)",
            "HR": "Croatian", "ET": "Estonian", "EL": "Greek", "HE": "Hebrew",
            "ID": "Indonesian", "IS": "Icelandic", "LV": "Latvian", "LT": "Lithuanian",
            "MS": "Malay", "RO": "Romanian", "SL": "Slovenian", "SR": "Serbian",
            "TL": "Tagalog", "TH": "Thai", "CS": "Czech", "TR": "Turkish",
            "UK": "Ukrainian", "VI": "Vietnamese"
        }

    def detect_languages(self, filename: str) -> Optional[str]:
        """
        Detects the first matching language code from a filename.

        Args:
            filename (str): The filename to analyze.

        Returns:
            Optional[str]: The first detected language code, or None if no match is found.
        """
        name = filename.upper()
        tokens = re.split(r'[^A-Z0-9]+', name)
        found = []

        for token in tokens:
            # Try matching 4-, 3-, and 2-character codes
            for length in [4, 3, 2]:
                if len(token) < length:
                    continue
                code = token[:length]
                if code in self.language_codes and code not in found:
                    found.append(code)
                    break

        # Special rule: prefer ENUS/ENUK over generic EN
        if 'EN' in found and any(code in found for code in ['US', 'UK']):
            found.remove('EN')

        # Special rule: prefer CHS/CHT over generic ZH
        if 'ZH' in found and any(code in found for code in ['CHS', 'CHT']):
            found.remove('ZH')

        # Return the first detected code, if any
        if found:
            return found[-1]

        # No match found
        return None