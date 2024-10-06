import os

from signalWords import get_language_code

def ask_to_change_setting():
    prompt = input("Is it correct? Press (+/-): ").strip()
    return prompt == '-'  # Return two values: whether to edit and what the user entered

def display_settings(settings):
    print("Settings:")
    for key, value in settings.items():
        print(f"{key}: {value}")
    print("______________________________")

def ask_for_variable(key, current_value):
    new_value = input(f"Enter a new value for {key} (current: {current_value}): ").strip()
    return new_value if new_value else current_value

def ask_for_file_path(prompt="Enter the file path: "):
    while True:
        file_path = input(prompt).strip()  # Read user input and trim spaces
        if os.path.isfile(file_path):  # Check if the file exists
            return file_path  # If the file exists, return its path
        elif file_path.lower() == 'exit':
            print("Exiting the program.")
            exit()
        else:
            print("File not found. Please try again.")  # Inform the user if the file does not exist

def ask_show_language_code_list():
    while True:
        answer = input("Show available languages? (+/-): ")
        if answer == '+':
            display_language_code_list(get_language_code())
            break
        elif answer == '-':
            break

def display_language_code_list(lang_codes):
    """Display the list of language codes in a table format."""
    lang_codes = list(lang_codes)  # Convert the set to a list
    lang_codes.sort()  # Call the sort method for the list
    print("List of language codes:")

    # Format the table with 10 columns
    for i in range(0, len(lang_codes), 10):  # Iterate through the list in steps of 10
        # Format the string to output 10 elements
        row = "{:<5}" * min(10, len(lang_codes) - i)
        print(row.format(*lang_codes[i:i + 10]))  # Output 10 elements at a time
