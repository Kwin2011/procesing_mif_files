import os
import sys
from settings.settings_manager import SettingsManager
from file_processor import FileProcessor
from file_handler import FileHandler
from user_interface import ConsoleUserInterface
from settings.settings_console_Interface import SettingsConsoleInterface


def main():
    print("MIF file processing program started")

    ui = ConsoleUserInterface()

    # --- 1. Ask for the first file ---
    target_path = ui.ask_for_file_path()

    if not os.path.isfile(target_path):
        print(f"Error: file not found → {target_path}")
        return

    # --- 2. Show/edit settings once ---
    SettingsConsoleInterface(target_path)

    while True:
        # --- 3. Initialize components ---
        settings = SettingsManager(target_path=target_path)
        processor = FileProcessor(settings)

        # --- 4. Process the file ---
        try:
            result_path = processor.process(target_path)
            print(f"✅ File successfully processed: {result_path}")
        except Exception as e:
            print(f"⛔ Critical error: {str(e)}")

        # --- 5. Ask if the user wants to continue ---
        if not ui.ask_to_continue():
            print("Processing finished")
            break

        # --- 6. Ask for the next file ---
        target_path = ui.ask_for_file_path()
        if not os.path.isfile(target_path):
            print(f"Error: file not found → {target_path}")
            break


if __name__ == "__main__":
    main()
