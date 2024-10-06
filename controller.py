import os
import re
from signalWords import replace_signal_words, is_language_code_valid
from settings import Settings
from views import display_settings, ask_for_variable, ask_for_file_path, ask_to_change_setting, \
    ask_show_language_code_list
from replacements import replace_variables

# Initialize settings
settings = Settings()

def get_language_code_from_filename(filename):
    # Search for a language code in the filename
    match = re.search(r'_(\w{2})_', filename)
    if match:
        return match.group(1).upper()  # Return the language code in uppercase
    return None

while True:
    # 1. Display current settings
    display_settings(settings.variables)

    # 2. Prompt to edit settings or continue with a file
    action = input("Do you want to edit settings? Enter + to edit, or the file path to continue: ").strip()

    if action == '+':
        # Allow editing settings
        for key in settings.variables.keys():
            new_value = ask_for_variable(key, settings.variables[key])
            settings.update_variable(key, new_value)
    else:
        # If not editing, assume the input is a file path
        input_mif_filename = action

    # 3. Check if the file path is entered and verify its existence
    if not os.path.isfile(input_mif_filename):
        print("File not found. Please try again.")
        continue  # Continue the loop if the file is not found

    # 4. Get language code from the filename
    language_code = get_language_code_from_filename(input_mif_filename)
    if language_code:
        print(f"Found language code: {language_code}")
        settings.variables['languageCode'] = language_code  # Save the language code in settings

    # 5. Prompt for confirmation of the language code
    if ask_to_change_setting():
        # Request to correct the language code
        while True:
            new_language_code = input("Enter a new language code: ").strip().upper()
            if is_language_code_valid(new_language_code):
                settings.variables['languageCode'] = new_language_code
                break
            else:
                print("The code does not exist.")
                ask_show_language_code_list()

    # 6. Process the file
    output_filename = f"prepred_{os.path.basename(input_mif_filename)}"
    output_mif_filename = os.path.join(os.path.dirname(input_mif_filename), output_filename)

    def replace_variable_def(input_mif_file, output_mif_file, vars):
        """Replace variables in the input file and save to the output file."""
        with open(input_mif_file, 'r', encoding='utf-8') as file:
            content = file.read()
            content = replace_variables(content, vars)  # Replace defined variables
            content = replace_signal_words(content, vars['languageCode'])  # Replace signal words based on the language code

        with open(output_mif_file, 'w', encoding='utf-8') as file:
            file.write(content)

    replace_variable_def(input_mif_filename, output_mif_filename, settings.variables)
    print(f"Replacement completed! The result is saved in {output_mif_filename}")

    # Prompt to process another file
    continue_choice = input("Process another file? (+ to continue, - to exit): ").strip().lower()
    if continue_choice != '+':
        break
