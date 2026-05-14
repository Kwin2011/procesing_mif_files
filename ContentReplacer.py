import re
import os
from json_rule_loader import JsonRuleLoader


class ContentReplacer:
    """
    Performs a series of replacements in MIF file content.
    Rules for tables, variables, and cleanup are loaded from JSON files in the 'rules/' folder.
    Only page-background logic (conditional branching) remains in Python.
    """

    def __init__(self, content: str, vars: dict, rules_dir: str = "rules"):
        self.content = content
        self.vars = vars
        self.logs = []
        self._loader = JsonRuleLoader(rules_dir)

    def get_logs(self) -> list:
        return self.logs

    def _perform_and_log_replacement(self, pattern, repl, description):
        """Kept for any one-off replacements not worth putting in JSON."""
        try:
            new_content, count = re.subn(pattern, repl, self.content)
            self.content = new_content
            if count > 0:
                self.logs.append(f"[SUCCESS] {description}: {count} replacement(s) made.")
            else:
                self.logs.append(f"[FAILURE] {description}: no matches found.")
        except re.error as e:
            self.logs.append(f"[ERROR]   {description}: invalid regex — {e}")

    def process(self) -> str:
        self.logs.append("--- Content processing started ---")

        # Built-in rules from JSON files
        self.content = self._loader.apply(self.content, "cleanup_rules.json",  logs=self.logs)
        self.content = self._loader.apply(self.content, "table_rules.json",    logs=self.logs)
        self.content = self._loader.apply(self.content, "variable_rules.json", vars=self.vars, logs=self.logs)

        # Custom rules added by admin (applied last, no variable substitution)
        custom_path = os.path.join(self._loader.rules_dir, "custom_rules.json")
        if os.path.isfile(custom_path):
            self.logs.append("[INFO]    Applying custom_rules.json")
            self.content = self._loader.apply(self.content, "custom_rules.json", logs=self.logs)
        else:
            self.logs.append("[INFO]    custom_rules.json not found — skipping")

        # Conditional logic that needs Python
        self._handle_page_background()

        self.logs.append("--- Content processing completed ---")
        return self.content

    def _handle_page_background(self):
        lang_code = self.vars.get("languageCode", "NA")
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
                self.logs.append("[FAILURE] <PageBackground `75'> not found. Trying alternative scenario.")
                self._perform_and_log_replacement(
                    r'(<PageNum\s*`2\'[\s\S]*?<PageBackground\s*`)(.*?)\'',
                    rf"\1Restriction_{lang_code}'>",
                    f"Replacing <PageBackground> for <PageNum `2'>"
                )
        else:
            self.logs.append(f"[INFO]    Pattern '{restriction_pattern}' not found. Skipping PageBackground.")
