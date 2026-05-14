import re
import json
from file_handler import FileHandler


class JsonRuleLoader:
    """
    Loads replacement rules from JSON files and applies them to content.

    Each rule in the JSON has:
        - "pattern":     regex pattern string
        - "replacement": replacement string (may contain {var_name} placeholders)
        - "description": human-readable label for logging
        - "uses_vars":   (optional bool) if true, {key} in replacement is filled from vars dict
    """

    def __init__(self, rules_dir="rules"):
        self.rules_dir = rules_dir
        self._cache = {}

    def load(self, filename: str) -> list:
        """Load and cache rules from a JSON file inside rules_dir."""
        path = f"{self.rules_dir}/{filename}"
        if path not in self._cache:
            content = FileHandler.read_file(path)
            self._cache[path] = json.loads(content)
        return self._cache[path]

    def apply(self, content: str, filename: str, vars: dict = None, logs: list = None) -> str:
        """
        Apply all rules from a JSON file to the given content.

        :param content:   Text to process.
        :param filename:  JSON file name inside rules_dir.
        :param vars:      Dict of variables for {key} substitution in replacements.
        :param logs:      Optional list to append log messages to.
        :return:          Processed content.
        """
        rules = self.load(filename)
        for rule in rules:
            pattern = rule["pattern"]
            replacement = rule["replacement"]
            description = rule.get("description", pattern)
            uses_vars = rule.get("uses_vars", False)

            if uses_vars and vars:
                try:
                    replacement = replacement.format(**vars)
                except KeyError as e:
                    msg = f"[WARNING] '{description}': missing variable {e} — skipped"
                    if logs is not None:
                        logs.append(msg)
                    continue

            try:
                new_content, count = re.subn(pattern, replacement, content)
                content = new_content
                if logs is not None:
                    if count > 0:
                        logs.append(f"[SUCCESS] {description}: {count} replacement(s) made.")
                    else:
                        logs.append(f"[FAILURE] {description}: no matches found.")
            except re.error as e:
                if logs is not None:
                    logs.append(f"[ERROR]   {description}: invalid regex — {e}")

        return content
