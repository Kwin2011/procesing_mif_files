from signalWords import get_language_code, is_language_code_valid
import inquirer

class UserInteraction:
    def __init__(self, settings):
        self.settings = settings

    def ask_to_edit_settings(self):
        """
        Interactively allows the user to choose and modify application settings,
        displaying current values.
        """
        # Create a list to display the current settings to the user.
        settings_display = [
            f"{key}: {value}"
            for key, value in self.settings.variables.items()
        ]

        # Add a separator for better readability.
        settings_display.append("______________________________")

        # Define the choices for the user, including options to change all,
        # continue without changes, or modify specific settings.
        choices = [
            ("Change all settings", "+"),
            ("Continue without changes", "path"),
            *[
                (f"Change {key}", key)
                for key in self.settings.variables.keys()
            ]
        ]

        # Create the inquirer prompt for user action.
        questions = [
            inquirer.List(
                "action",
                message="Current settings:\n" + "\n".join(settings_display),
                choices=choices,
                default="path",
                carousel=True  # Enable carousel mode for easier navigation.
            )
        ]

        # Get the user's answer.
        answers = inquirer.prompt(questions)

        # Handle the user's chosen action.
        if answers["action"] == "+":
            # If the user chooses to change all parameters,
            # iterate through them and prompt for new values.
            for key in self.settings.variables:
                new_value = self.ask_for_variable(key, self.settings.variables[key])
                self.settings.update_variable(key, new_value)
            return None  # No file path to return in this case.
        elif answers["action"] == "path":
            # If the user chooses to continue without changes,
            # prompt for a file path.
            path_question = [
                inquirer.Text("file_path", message="Enter file path:")
            ]
            return inquirer.prompt(path_question)["file_path"]
        else:
            # If a specific parameter is chosen for modification,
            # prompt for its new value and update it.
            key = answers["action"]
            new_value = self.ask_for_variable(key, self.settings.variables[key])
            self.settings.update_variable(key, new_value)
            # Recursively call the function to display updated settings
            # and allow further modifications or continuation.
            return self.ask_to_edit_settings()


    def ask_for_variable(self, key, current_value):
        """
        Prompts the user for a new value for a specific variable,
        displaying its current value.
        """
        question = [
            inquirer.Text(
                name="new_value",
                message=f"Current {key}: {current_value}. Enter new value (or Enter to keep current):",
                default=current_value # Set the current value as default.
            )
        ]
        answer = inquirer.prompt(question)
        return answer["new_value"]

    def ask_to_continue(self):
        """
        Asks the user whether they want to continue processing files.
        """
        question = [
            inquirer.Confirm(
                "continue",
                message="Process the next file?",
                default=True # 'Yes' is the default option.
            )
        ]
        answer = inquirer.prompt(question)
        return answer["continue"]

    def display_settings(self):
        """
        Prints the current application settings to the console.
        """
        print("\nCurrent settings:")
        for key, value in self.settings.variables.items():
            print(f"{key}: {value}")
        print("______________________________")

    def ask_to_change_language_code(self, found_code):
        """
        Confirms the detected language code with the user via a yes/no list.
        """
        questions = [
            inquirer.List(
                "confirm_lang",
                message=f"Auto-detected language: {found_code}. Confirm?",
                choices=[
                    ("Yes", True),
                    ("No", False)
                ],
                default=True # 'Yes' is selected by default.
            )
        ]
        answers = inquirer.prompt(questions)
        return answers["confirm_lang"]

    def ask_for_new_language_code(self):
        """
        Allows the user to select a new language code from a list of
        available options.
        """
        lang_codes = sorted(get_language_code()) # Get and sort all available language codes.

        questions = [
            inquirer.List(
                "selected_code",
                message="Choose a language code:",
                choices=[(code, code) for code in lang_codes], # Display codes as both label and value.
                carousel=True
            )
        ]

        answers = inquirer.prompt(questions)
        return answers["selected_code"]

    def display_language_code_list(self):
        """
        Prints a formatted list of all available language codes.
        """
        lang_codes = sorted(get_language_code())
        print("\nAvailable language codes:")
        # Print codes in rows of 10 for better readability.
        for i in range(0, len(lang_codes), 10):
            row = lang_codes[i:i + 10]
            print("  ".join(f"{code:<5}" for code in row))