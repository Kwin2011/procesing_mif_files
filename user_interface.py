class ConsoleUserInterface:
    """Console-based user interface for MIF file processing."""

    def __init__(self):
        pass

    def ask_for_file_path(self) -> str:
        return input("Enter path to file: ").strip()

    def ask_for_output_path(self) -> str:
        return input("Enter output path: ").strip()

    def ask_to_continue(self) -> bool:
        answer = input("Do you want to process another file? (y/n): ").strip().lower()
        return answer == "y"

    def show_message(self, message: str):
        print(message)

    def show_settings(self, settings: dict):
        print("\n📋 Current Settings:")
        for key, value in settings.items():
            print(f"  {key}: {value}")

    def ask_to_update_settings(self) -> bool:
        answer = input("Do you want to update settings? (y/n): ").strip().lower()
        return answer == "y"

    def ask_for_setting_update(self, key: str, current_value: str) -> str:
        return input(f"Enter new value for '{key}' (current: {current_value}): ").strip()
