import os
import re
from datetime import datetime
from settings.settings_manager import SettingsManager

import msvcrt
from colorama import init, Fore, Style

init()


class SettingsConsoleInterface:
    """
    Console-based editor for settings metadata.

    Allows viewing and editing specific fields such as:
    - deliveryDate
    - KaNumber
    - KaDate

    Provides validation for date fields and highlights changes.
    """

    def __init__(self, target_path):
        self.settings_manager = SettingsManager(target_path=target_path)
        self.current_selection = 3
        self.editable_fields = ["deliveryDate", "KaNumber", "KaDate"]
        self.updated_fields = set()
        self.run()

    def _validate_date(self, date_str):
        """Check if a date is valid in DD.MM.YYYY format"""
        try:
            day, month, year = map(int, date_str.split('.'))
            datetime(year=year, month=month, day=day)
            return True
        except (ValueError, AttributeError):
            return False

    def display_settings(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        meta_data = self.settings_manager.get_meta_data()

        print(f"{Fore.YELLOW}=== Settings Editor ==={Style.RESET_ALL}\n")
        print(f"KaVersion: {meta_data['KaVersion']}")
        print(f"languageCode: {meta_data['languageCode']}")

        for i, field in enumerate(self.editable_fields):
            prefix = "> " if i == self.current_selection else "  "
            color = Fore.YELLOW if field in self.updated_fields else Fore.BLUE

            # Highlight invalid dates in red
            if field in ["deliveryDate", "KaDate"] and not self._validate_date(meta_data[field]):
                color = Fore.RED

            print(f"{prefix}{color}{field}: {meta_data[field]}{Style.RESET_ALL}")

        prefix = "> " if self.current_selection == len(self.editable_fields) else "  "
        print(f"\n{prefix}{Fore.GREEN}Next{Style.RESET_ALL}")

    def get_user_input(self):
        """
        Handle user key input:
        - Arrow up/down to navigate fields
        - Enter to select
        - Esc to exit
        """
        while True:
            key = ord(msvcrt.getch())
            if key == 224:
                key = ord(msvcrt.getch())
                if key == 72:  # Up
                    self.current_selection = max(0, self.current_selection - 1)
                    return True
                elif key == 80:  # Down
                    self.current_selection = min(len(self.editable_fields), self.current_selection + 1)
                    return True
            elif key == 13:  # Enter
                return False
            elif key == 27:  # Esc
                exit()

    def edit_selected_field(self):
        """
        Edit the currently selected field with validation.

        Dates are validated for DD.MM.YYYY format. Empty input keeps the previous value.
        """
        if self.current_selection < len(self.editable_fields):
            field = self.editable_fields[self.current_selection]
            current_value = self.settings_manager.get_meta_data()[field]

            while True:
                new_value = input(f"Set new {field} (current: {current_value}) >> ")

                # Keep previous value if input is empty
                if new_value.strip() == "":
                    print(f"{Fore.WHITE}↩ Keeping previous value{Style.RESET_ALL}")
                    input("Press Enter to continue...")
                    return

                # Validate date fields
                if field in ["deliveryDate", "KaDate"]:
                    if not self._validate_date(new_value):
                        print(f"{Fore.RED}✗ Invalid date (use DD.MM.YYYY){Style.RESET_ALL}")
                        print(f"{Fore.CYAN}Please try again or press Enter to cancel{Style.RESET_ALL}")
                        continue

                # Update value if valid
                try:
                    self.settings_manager.update_setting(field, new_value)
                    self.updated_fields.add(field)
                    print(f"{Fore.GREEN}✓ Updated{Style.RESET_ALL}")
                    self.display_settings()
                    break
                except Exception as e:
                    print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
                    input("Press Enter to continue...")
                    break

    def run(self):
        """Main loop to display settings and handle user edits"""
        while True:
            self.display_settings()
            if self.get_user_input():
                continue

            if self.current_selection == len(self.editable_fields):
                break
            else:
                self.edit_selected_field()
                self.current_selection = len(self.editable_fields)


if __name__ == "__main__":
    target_path = input("Enter target file path: ")
    SettingsConsoleInterface(target_path)
