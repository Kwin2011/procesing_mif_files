import re

signal_words = {
    'DANGER': {
        'AR': 'الخطر',
        'BG': 'ОПАСНОСТ',
        'MY': 'Bahaya',
        'CA': 'PERILL',
        'ZH': '危险',
        'ZF': '危险',
        'HR': 'OPASNOST',
        'DA': 'FARE',
        'NL': 'GEVAAR',
        'ET': 'OHT',
        'FI': 'VAARA',
        'FR': 'DANGER',
        'DE': 'GEFAHR',
        'EL': 'ΚΙΝΔΥΝΟΣ',
        'HE': 'סכנה',
        'HU': 'VESZÉLY',
        'ID': 'BAHAYA',
        'IT': 'PERICOLO',
        'IS': 'HÆTTA',
        'JA': '危険',
        'KO': '위험',
        'LV': 'BISTAMI',
        'LT': 'PAVOJUS',
        'MS': 'BAHAYA',
        'NO': 'FARE',
        'PL': 'NIEBEZPIECZEŃSTWO',
        'RO': 'PERICOL',
        'RU': 'ОПАСНОСТЬ',
        'PT': 'PERIGO',  # Portuguese
        'SK': 'NEBEZPEČENSTVO',  # Slovak
        'SL': 'NEVARNOST',  # Slovenian
        'SR': 'OPASNOST',  # Serbian
        'ES': 'PELIGRO',  # Spanish
        'SV': 'FARA',  # Swedish
        'TL': 'MAPANGANIB',  # Tagalog
        'TH': 'อันตราย',  # Thai
        'CS': 'NEBEZPEČÍ',  # Czech
        'TR': 'TEHLIKE',  # Turkish
        'UK': 'НЕБЕЗПЕЧНО',  # Ukrainian
        'VI': 'NGUY HIỂM'  # Vietnamese
    },
    'WARNING': {
        'AR': 'التحذير',
        'BG': 'ПРЕДУПРЕЖДЕНИЕ',
        'MY': 'Peringatan',
        'CA': 'ADVERTENCIA',
        'ZH': '警告',
        'ZF': '警告',
        'HR': 'UPOZORENJE',
        'DA': 'ADVARSEL',
        'NL': 'WAARSCHUWING',
        'ET': 'HOIATUS',
        'FI': 'VAROITUS',
        'FR': 'AVERTISSEMENT',
        'DE': 'WARNUNG',
        'EL': 'ΠΡΟΕΙΔΟΠΟΙΗΣΗ',
        'HE': 'אזהרה',
        'HU': 'FIGYELEM',
        'ID': 'PERINGATAN',
        'IT': 'AVVERTENZA',
        'IS': 'AÐVÖRUN',
        'JA': '警告',
        'KO': '경고',
        'LV': 'BRĪDINĀJUMS',
        'LT': 'ĪSPEJIMAS',
        'MS': 'AMARAN',
        'NO': 'ADVARSEL',
        'PL': 'OSTRZEŻENIE',
        'RO': 'AVERTISMENT',
        'RU': 'ПРЕДУПРЕЖДЕНИЕ',
        'PT': 'ATENÇÃO',  # Portuguese
        'SK': 'VAROVANIE',  # Slovak
        'SL': 'OPOZORILO',  # Slovenian
        'SR': 'UPOZORENJE',  # Serbian
        'ES': 'ADVERTENCIA',  # Spanish
        'SV': 'VARNING',  # Swedish
        'TL': 'BABALA',  # Tagalog
        'TH': 'คำเตือน',  # Thai
        'CS': 'VAROVÁNÍ',  # Czech
        'TR': 'UYARI',  # Turkish
        'UK': 'УВАГА',  # Ukrainian
        'VI': 'CẢNH BÁO'  # Vietnamese
    },
    'CAUTION': {
        'AR': 'الانتباه',
        'BG': 'ВНИМАНИЕ',
        'MY': 'Waspada',
        'CA': 'ATENCIO',
        'ZH': '注意',
        'ZF': '注意',
        'HR': 'OPREZ',
        'DA': 'FORSIGTIG',
        'NL': 'VOORZICHTIG',
        'ET': 'ETTEVAATUST',
        'FI': 'HUOMIO',
        'FR': 'ATTENTION',
        'DE': 'VORSICHT',
        'EL': 'ΠΡΟΣΟΧΗ',
        'HE': 'תשומת לב',
        'HU': 'VIGYÁZAT',
        'ID': 'WASPADAI',
        'IT': 'ATTENZIONE',
        'IS': 'VARÚÐ',
        'JA': '注意',
        'KO': '주의',
        'LV': 'UZMANĪBU',
        'LT': 'ATSARGIAI',
        'MS': 'AWAS',
        'NO': 'FORSIKTIG',
        'PL': 'UWAGA',
        'RO': 'ATENȚIE',
        'RU': 'ВНИМАНИЕ',
        'PT': 'CUIDADO',  # Portuguese
        'SK': 'UPOZORNENIE',  # Slovak
        'SL': 'POZOR',  # Slovenian
        'SR': 'PAŽNJA',  # Serbian
        'ES': 'ATENCIÓN',  # Spanish
        'SV': 'OBSERVERA',  # Swedish
        'TL': 'MAG-INGAT',  # Tagalog
        'TH': 'ข้อควรระวัง',  # Thai
        'CS': 'POZOR',  # Czech
        'TR': 'DIKKAT',  # Turkish
        'UK': 'ОБЕРЕЖНО',  # Ukrainian
        'VI': 'THẬN TRỌNG'  # Vietnamese
    },
    'NOTICE': {
        'AR': 'ملاحظة',
        'BG': 'Бележка',
        'MY': 'Notis',
        'CA': 'AVIS',
        'ZH': '指示',
        'ZF': '指示',
        'HR': 'NAPOMENA',
        'DA': 'BEMERK',
        'NL': 'LET OP',
        'ET': 'TEATIS',
        'FI': 'HUOMAUTUS',
        'FR': 'AVIS',
        'DE': 'HINWEIS',
        'EL': 'ΣΗΜΕΙΩΣΗ',
        'HE': 'הערה',
        'HU': 'MEGJEGYZÉS',
        'ID': 'PERHATIAN',
        'IT': 'AVVISO',
        'IS': 'ATHUGIÐ',
        'JA': '通知',
        'KO': '알림',
        'LV': 'IEVĒROT',
        'LT': 'PASTABA',
        'MS': 'NOTIS',
        'NO': 'LES DETTE',
        'PL': 'NOTYFIKACJA',
        'RO': 'NOTĂ',
        'RU': 'УВЕДОМЛЕНИЕ',
        'PT': 'AVISO',  # Portuguese
        'SK': 'OZNÁMENIE',  # Slovak
        'SL': 'OBVESTILO',  # Slovenian
        'SR': 'NAPOMENA',  # Serbian
        'ES': 'AVISO',  # Spanish
        'SV': 'OBS',  # Swedish
        'TL': 'PAUNAWA',  # Tagalog
        'TH': 'ข้อสังเกต',  # Thai
        'CS': 'OZNÁMENÍ',  # Czech
        'TR': 'DUYURU',  # Turkish
        'UK': 'ЗВЕРНІТЬ УВАГУ',  # Ukrainian
        'VI': 'LƯU Ý'  # Vietnamese
    }
}


def get_language_code():
    # Use a set to avoid duplicates
    lang_codes = set()

    for signal in signal_words.values():
        # Add all keys (language codes) to the set
        lang_codes.update(signal.keys())

    return lang_codes


def is_language_code_valid(lang_code):
    # Check if the provided language code is valid
    return lang_code in get_language_code()


def replace_signal_words(content, languageCode):
    """Replace signal words in the content based on the specified language code."""
    for signal_word, translations in signal_words.items():
        if languageCode in translations:
            # Perform replacement, considering case sensitivity
            new_content = re.sub(signal_word, translations[languageCode], content)

            # Check if a replacement occurred
            if new_content != content:
                print(
                    f"Replaced '{signal_word}' with '{translations[languageCode]}'")  # Output replacement info to console
                content = new_content  # Update content after replacement
    return content