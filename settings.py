# settings.py
import json
import os

class Settings:
    def __init__(self, file_path='settings.json'):
        self.file_path = file_path
        self.variables = {
            "KaVersion": "00",
            "deliveryDate": "empty",
            "KaNumber": "empty",
            "KaDate": "empty",
            "languageCode": "EN",
            "KaNameReleased": "Acolad Switzerland AG"
        }
        self.load()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.variables = json.load(file)
        else:
            self.save()  # Якщо файл не існує, створити новий


    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.variables, file, ensure_ascii=False, indent=4)

    def update_variable(self, key, value):
        if key in self.variables:
            self.variables[key] = value
            self.save()
