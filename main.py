import io
import sys
from settings import Settings
from file_processor import FileProcessor
from user_interaction import UserInteraction

# Set the standard output encoding to UTF-8 to ensure proper display of characters.
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    # Initialize objects for settings, user interaction, and file processing.
    settings = Settings()
    user_interaction = UserInteraction(settings)
    file_processor = FileProcessor(settings, user_interaction)

    # Main loop for the application.
    while True:
        # Display the current application settings to the user.
        user_interaction.display_settings()

        # Prompt the user to enter a file path or choose to edit settings.
        file_path = user_interaction.ask_to_edit_settings()

        # If a file path is provided, proceed with file processing.
        if file_path:
            # Check if the provided file path is valid and the file exists.
            if not file_processor.is_file_valid(file_path):
                print("File not found. Please try again.")
                continue  # Continue to the next iteration of the loop.

            # Process the specified file.
            file_processor.process_file(file_path)

        # Ask the user if they want to continue with another operation.
        if not user_interaction.ask_to_continue():
            break  # Exit the loop if the user chooses not to continue.

if __name__ == "__main__":
    main()