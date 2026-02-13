import re

class SignalWordsReplacer:
    """
    Class to replace signal words in text content based on a specified language.

    Attributes:
        language_code (str): The target language code used for replacements.

    Class Attributes:
        signal_words (dict): A dictionary of signal words and their translations 
                             for multiple languages.
                             Format: {signal_word: {lang_code: translation, ...}, ...}

    Methods:
        get_all_language_codes() -> set:
            Returns a set of all valid language codes in the signal_words dictionary.

        is_language_code_valid(lang_code: str) -> bool:
            Checks whether the provided language code is valid.

        replace(content: str) -> str:
            Replaces all signal words in the given content with their translations
            according to the specified language code.
    """

    signal_words = {
        "DANGER": {
            "AR": "الخطر",
            "BG": "ОПАСНОСТ",
            "MY": "Bahaya",
            "CA": "PERILL",
            "ZH": "危险",
            "ZF": "危险",
            "HR": "OPASNOST",
            "DA": "FARE",
            "NL": "GEVAAR",
            "ET": "OHT",
            "FI": "VAARA",
            "FR": "DANGER",
            "DE": "GEFAHR",
            "EL": "ΚΙΝΔΥΝΟΣ",
            "HE": "סכנה",
            "HU": "VESZÉLY",
            "ID": "BAHAYA",
            "IT": "PERICOLO",
            "IS": "HÆTTA",
            "JA": "危険",
            "KO": "위험",
            "LV": "BĪSTAMI",
            "LT": "PAVOJUS",
            "MS": "BAHAYA",
            "NO": "FARE",
            "PL": "NIEBEZPIECZEŃSTWO",
            "RO": "PERICOL",
            "RU": "ОПАСНОСТЬ",
            "PT": "PERIGO",  # Portuguese
            "SK": "NEBEZPEČENSTVO",  # Slovak
            "SL": "NEVARNOST",  # Slovenian
            "SR": "OPASNOST",  # Serbian
            "ES": "PELIGRO",  # Spanish
            "SV": "FARA",  # Swedish
            "TL": "MAPANGANIB",  # Tagalog
            "TH": "อันตราย",  # Thai
            "CS": "NEBEZPEČÍ",  # Czech
            "TR": "TEHLIKE",  # Turkish
            "UK": "НЕБЕЗПЕЧНО",  # Ukrainian
            "VI": "NGUY HIỂM",  # Vietnamese
        },
        "WARNING": {
            "AR": "تحذير",
            "BG": "ПРЕДУПРЕЖДЕНИЕ",
            "MY": "Peringatan",
            "CA": "ADVERTENCIA",
            "ZH": "警告",
            "ZF": "警告",
            "HR": "UPOZORENJE",
            "DA": "ADVARSEL",
            "NL": "WAARSCHUWING",
            "ET": "HOIATUS",
            "FI": "VAROITUS",
            "FR": "AVERTISSEMENT",
            "DE": "WARNUNG",
            "EL": "ΠΡΟΕΙΔΟΠΟΙΗΣΗ",
            "HE": "אזהרה",
            "HU": "FIGYELEM",
            "ID": "PERINGATAN",
            "IT": "AVVERTENZA",
            "IS": "AÐVÖRUN",
            "JA": "警告",
            "KO": "경고",
            "LV": "BRĪDINĀJUMS",
            "LT": "ĪSPEJIMAS",
            "MS": "AMARAN",
            "NO": "ADVARSEL",
            "PL": "OSTRZEŻENIE",
            "RO": "AVERTISMENT",
            "RU": "ПРЕДУПРЕЖДЕНИЕ",
            "PT": "ATENÇÃO",  # Portuguese
            "SK": "VAROVANIE",  # Slovak
            "SL": "OPOZORILO",  # Slovenian
            "SR": "UPOZORENJE",  # Serbian
            "ES": "ADVERTENCIA",  # Spanish
            "SV": "VARNING",  # Swedish
            "TL": "BABALA",  # Tagalog
            "TH": "คำเตือน",  # Thai
            "CS": "VAROVÁNÍ",  # Czech
            "TR": "UYARI",  # Turkish
            "UK": "УВАГА",  # Ukrainian
            "VI": "CẢNH BÁO",  # Vietnamese
        },
        "CAUTION": {
            "AR": "تنبيه",
            "BG": "ВНИМАНИЕ",
            "MY": "Waspada",
            "CA": "ATENCIO",
            "ZH": "注意",
            "ZF": "注意",
            "HR": "OPREZ",
            "DA": "FORSIGTIG",
            "NL": "VOORZICHTIG",
            "ET": "ETTEVAATUST",
            "FI": "HUOMIO",
            "FR": "ATTENTION",
            "DE": "VORSICHT",
            "EL": "ΠΡΟΣΟΧΗ",
            "HE": "זהירות",
            "HU": "VIGYÁZAT",
            "ID": "WASPADAI",
            "IT": "ATTENZIONE",
            "IS": "VARÚÐ",
            "JA": "注意",
            "KO": "주의",
            "LV": "UZMANĪBU",
            "LT": "ATSARGIAI",
            "MS": "AWAS",
            "NO": "FORSIKTIG",
            "PL": "UWAGA",
            "RO": "ATENŢIE",
            "RU": "ВНИМАНИЕ",
            "PT": "CUIDADO",  # Portuguese
            "SK": "UPOZORNENIE",  # Slovak
            "SL": "POZOR",  # Slovenian
            "SR": "PAŽNJA",  # Serbian
            "ES": "ATENCIÓN",  # Spanish
            "SV": "OBSERVERA",  # Swedish
            "TL": "MAG-INGAT",  # Tagalog
            "TH": "ข้อควรระวัง",  # Thai
            "CS": "POZOR",  # Czech
            "TR": "DIKKAT",  # Turkish
            "UK": "ОБЕРЕЖНО",  # Ukrainian
            "VI": "THẬN TRỌNG",  # Vietnamese
        },
        "NOTICE": {
            "AR": "ملاحظة",
            "BG": "Бележка",
            "MY": "Notis",
            "CA": "AVIS",
            "ZH": "指示",
            "ZF": "指示",
            "HR": "NAPOMENA",
            "DA": "BEMÆRK",
            "NL": "LET OP",
            "ET": "TEATIS",
            "FI": "HUOMAUTUS",
            "FR": "AVIS",
            "DE": "HINWEIS",
            "EL": "ΣΗΜΕΙΩΣΗ",
            "HE": "הערה",
            "HU": "MEGJEGYZÉS",
            "ID": "PERHATIAN",
            "IT": "AVVISO",
            "IS": "ATHUGIÐ",
            "JA": "通知",
            "KO": "알림",
            "LV": "IEVĒROT",
            "LT": "PASTABA",
            "MS": "NOTIS",
            "NO": "LES DETTE",
            "PL": "NOTYFIKACJA",
            "RO": "NOTĂ",
            "RU": "УВЕДОМЛЕНИЕ",
            "PT": "AVISO",  # Portuguese
            "SK": "OZNÁMENIE",  # Slovak
            "SL": "OBVESTILO",  # Slovenian
            "SR": "NAPOMENA",  # Serbian
            "ES": "AVISO",  # Spanish
            "SV": "OBS",  # Swedish
            "TL": "PAUNAWA",  # Tagalog
            "TH": "ข้อสังเกต",  # Thai
            "CS": "OZNÁMENÍ",  # Czech
            "TR": "DUYURU",  # Turkish
            "UK": "ЗВЕРНІТЬ УВАГУ",  # Ukrainian
            "VI": "LƯU Ý",  # Vietnamese
        },
    }

    def __init__(self, language_code: str):
        """
        Initialize a SignalWordsReplacer instance with a specific language.

        Args:
            language_code (str): Target language code for replacements.

        Raises:
            ValueError: If the language_code is not valid.
        """
        if not self.is_language_code_valid(language_code):
            raise ValueError(f"Invalid language code: {language_code}")
        self.language_code = language_code

    @classmethod
    def get_all_language_codes(cls) -> set:
        """
        Retrieve all language codes available in the signal_words dictionary.

        Returns:
            set: A set of all valid language codes.
        """
        codes = set()
        for translations in cls.signal_words.values():
            codes.update(translations.keys())
        return codes

    @classmethod
    def is_language_code_valid(cls, lang_code: str) -> bool:
        """
        Check if a given language code is valid for replacements.

        Args:
            lang_code (str): Language code to check.

        Returns:
            bool: True if valid, False otherwise.
        """
        return lang_code in cls.get_all_language_codes()

    def replace(self, content: str) -> str:
        """
        Replace all signal words in the provided content with translations 
        according to the specified language.

        Args:
            content (str): The text content in which to replace signal words.

        Returns:
            str: The content with signal words replaced.

        Side Effects:
            Prints each replacement to the console for logging purposes.
        """
        for signal_word, translations in self.signal_words.items():
            if self.language_code in translations:
                new_content = re.sub(signal_word, translations[self.language_code], content)
                if new_content != content:
                    print(f"Replaced '{signal_word}' with '{translations[self.language_code]}'")
                    content = new_content
        return content
