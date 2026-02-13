import re
# ContentReplacer.py
class ContentReplacer:
    """
    Class for performing a series of replacements in text content
    with detailed logging of each step.
    """
    def __init__(self, content, vars):
        """
        Constructor initializes the instance with content, variables,
        and creates an empty list for logs.
        """
        self.content = content
        self.vars = vars
        self.logs = []

    def get_logs(self):
        """Returns the list of logs generated during processing."""
        return self.logs

    def _perform_and_log_replacement(self, pattern, repl, description):
        """
        Performs replacement using re.subn() and logs the result.

        :param pattern: Regular expression for searching.
        :param repl: Replacement string or function.
        :param description: Description of the operation for logging.
        """
        try:
            new_content, count = re.subn(pattern, repl, self.content)
            self.content = new_content
            if count > 0:
                self.logs.append(f"[SUCCESS] {description}: {count} replacement(s) made.")
            else:
                self.logs.append(f"[FAILURE] {description}: No matches found.")
        except re.error as e:
            self.logs.append(f"[ERROR]   {description}: Invalid regular expression. {e}")


    def process(self):
        """
        Main method that sequentially performs all replacements.
        It acts as the "activator" of all other methods.
        """
        self.logs.append("--- Content processing started ---")
        self._remove_default_font()
        self._replace_table_widths()
        self._replace_variables()
        self._handle_page_background()
        self._cleanup()
        self.logs.append("--- Content processing completed ---")
        
        return self.content

    def _remove_default_font(self):
        self._perform_and_log_replacement(
            pattern=r'(<VariableDef\s*`<Default ¶ Font\\>)(.*?)\'',
            repl=r"<VariableDef `\2'",
            description="Removing '<Default ¶ Font>' tag"
        )

    def _replace_table_widths(self):
        replacements = {
            # ... (your replacements dictionary remains unchanged here)
            r'<TblColumnWidth\s*2\.89033\s*cm>.*<TblColumnWidth\s*2\.51263\s*cm>': '<TblColumnWidth 2.797 cm>...',
            r'<TblColumnWidth\s*11\.93173\s*cm>\s*<TblColumnWidth\s*2\.16131\s*cm>\s*<TblColumnWidth\s*3\.505\s*cm>': '<TblColumnWidth 10.175 cm>...',
        }
        for i, (pattern, replacement) in enumerate(replacements.items(), 1):
             self._perform_and_log_replacement(
                 pattern, 
                 replacement, 
                 f"Replacing table widths (pattern #{i})"
             )

    def _replace_variables(self):
        # Using .get() for safe dictionary access
        # to avoid KeyError if the key is missing.
        self._perform_and_log_replacement(
            r'(<VariableFormat\s*<VariableName\s*`SCHKA1Number\'?>\s*<VariableDef\s*)(`.*?)(\'?>)', 
            rf"\1`{self.vars.get('KaNumber', '')}'>",
            "Variable 'SCHKA1Number'"
        )
        self._perform_and_log_replacement(
            r'(<VariableFormat\s*<VariableName\s*`SCHKA1Date\'?>\s*<VariableDef\s*)(`.*?)(\'?>)', 
            rf"\1`{self.vars.get('KaDate', '')}'>",
            "Variable 'SCHKA1Date'"
        )
        # ... and so on for all other variables
        self._perform_and_log_replacement(
            r'(<VariableFormat\s*<VariableName\s*`TIMDocNumber\'?>\s*<VariableDef\s*`\d+)(\'?>)',
            rf"\1_{self.vars.get('languageCode', 'NA')}'>",
            "Variable 'TIMDocNumber'"
        )

        for i in range(2, 8):
            self._perform_and_log_replacement(
                fr'(<VariableFormat\s*<VariableName\s*`SCHKA{i}Number\'?>\s*<VariableDef\s*`)(.*?)(\'?>)',
                r"\1'>",
                f"Clearing variable 'SCHKA{i}Number'"
            )
            # ... and so on for Date and Version
            
    def _handle_page_background(self):
        lang_code = self.vars.get('languageCode', 'NA')
        restriction_pattern = rf"Titlepage_Translation_{lang_code}"
        
        if re.search(restriction_pattern, self.content):
            self.logs.append(f"[INFO]    Pattern '{restriction_pattern}' found. Checking PageBackground.")
            
            new_content, count = re.subn(
                r'(<PageBackground\s*`)(75)(\'?>)',
                rf"\1Restriction_{lang_code}'>",
                self.content
            )
            if count > 0:
                self.content = new_content
                self.logs.append(f"[SUCCESS] Replacing <PageBackground `75'>: {count} replacement(s) made.")
            else:
                self.logs.append(f"[FAILURE] <PageBackground `75'> not found. Checking alternative scenario.")
                self._perform_and_log_replacement(
                     r'(<PageNum\s*`2\'[\s\S]*?<PageBackground\s*`)(.*?)\'',
                     rf"\1Restriction_{lang_code}'>",
                     "Replacing <PageBackground> for <PageNum `2'>"
                )
        else:
            self.logs.append(f"[INFO]    Pattern '{restriction_pattern}' not found. Skipping PageBackground replacement.")

    def _cleanup(self):
        self._perform_and_log_replacement(
            r'(<VariableFormat\s*>\s*<VariableName\s*`TIMLeadOfficeReleasedRD\'?>\s*<VariableDef\s*`)(NE1)(\'?>\s*>)',
            r"\1'>\n>",
            "Clearing 'TIMLeadOfficeReleasedRD'"
        )
        self._perform_and_log_replacement(
            r'(<VariableName\s*`SCHLeadOffice\'?>\s*<VariableDef\s*`)(.*?)\'',
            r"\1'",
            "Clearing 'SCHLeadOffice'"
        )
        self._perform_and_log_replacement(
            r'[„“]',
            '"',
            "Replacing special quotation marks"
        )

# --- Usage example ---
if __name__ == "__main__":
    from file_handler import FileHandler  # Make sure the file with the class is named file_handler.py

    original_file = "exampleFile/EJ_41416056_DA_01.mif"
    
    # Check if the file exists
    if not FileHandler.is_file_valid(original_file):
        print(f"File '{original_file}' not found.")
        exit(1)

    # Read file content
    content = FileHandler.read_file(original_file)

    # Replacement data
    variables = {
        'KaNumber': 'NEW-KA-123',
        'KaDate': '2025-07-12',
        'KaVersion': 'v2.1',
        'deliveryDate': '2025-07-13',
        'KaNameReleased': 'John Doe',
        'languageCode': 'EN'
    }

    # Process content
    replacer = ContentReplacer(content, variables)
    processed_content = replacer.process()
    logs = replacer.get_logs()

    # Save result to a file with prefix "_"
    saved_path = FileHandler.write_file(original_file, processed_content, prefix="___")

    # Output results
    print(f"Processed file saved as: {saved_path}")
    print("\n--- OPERATION LOG ---")
    for log in logs:
        print(log)
