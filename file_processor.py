import os  # Import the 'os' module for operating system-related functionalities
import re
from replacements import replace_variables
from signalWords import replace_signal_words, is_language_code_valid


class FileProcessor:
    def __init__(self, settings, user_interaction):
        """
        Initializes the FileProcessor with settings and a user interaction object.
        :param settings: An object containing application settings.
        :param user_interaction: An object to handle user interactions.
        """
        self.settings = settings
        self.user_interaction = user_interaction

    def is_file_valid(self, file_path):
        """
        Checks if the given file path points to a valid file.
        :param file_path: The path to the file.
        :return: True if the file exists and is a file, False otherwise.
        """
        return os.path.isfile(file_path)

    def get_language_code_from_filename(self, filename):
        """
        Extracts a two-letter language code from the filename,
        assuming it's in the format '_XX_'.
        :param filename: The name of the file.
        :return: The language code in uppercase if found, None otherwise.
        """
        match = re.search(r'_(\w{2})_', filename)
        if match:
            return match.group(1).upper()  # Return the language code in uppercase
        return None

    def replace_variables_in_file(self, input_file, output_file):
        """
        Reads content from an input file, replaces variables and signal words
        based on current settings, and writes the modified content to an output file.
        :param input_file: The path to the input file.
        :param output_file: The path to the output file where modified content will be saved.
        """
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
            # Replace variables in the content using the settings.
            content = replace_variables(content, self.settings.variables)
            # Replace signal words based on the language code in settings.
            content = replace_signal_words(content, self.settings.variables['languageCode'])

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)

    def process_file(self, file_path):
        """
        Processes a single file: automatically detects language code from the filename,
        prompts the user for confirmation or a new language code if needed,
        updates settings, and then performs variable and signal word replacements.
        :param file_path: The path to the file to be processed.
        """
        # Automatically detect the language code from the file name.
        language_code = self.get_language_code_from_filename(file_path)
        if language_code:
            print(f"Language code found in file: {language_code}")
            # Ask the user to confirm or change the detected language code.
            if not self.user_interaction.ask_to_change_language_code(language_code):
                # If the user doesn't confirm, prompt for a new language code.
                language_code = self.user_interaction.ask_for_new_language_code()

            self.settings.update_variable('languageCode', language_code)
        else:
            print("Language code not found in file. Using default code.")
            # If no language code is found, ask the user to provide one.
            language_code = self.user_interaction.ask_for_new_language_code()
            self.settings.update_variable('languageCode', language_code)

        # Construct the output filename and path.
        output_filename = f"_{os.path.basename(file_path)}"
        output_path = os.path.join(os.path.dirname(file_path), output_filename)

        # Perform the variable and signal word replacements and save the output.
        self.replace_variables_in_file(file_path, output_path)
        print(f"Processing complete! Result saved to {output_path}")