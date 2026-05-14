import re
import json
import os
from colorama import init, Fore, Style

init()

CUSTOM_RULES_FILE = "rules/custom_rules.json"


# ─────────────────────────── helpers ────────────────────────────

def _load_custom_rules() -> list:
    if os.path.isfile(CUSTOM_RULES_FILE):
        with open(CUSTOM_RULES_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_custom_rules(rules: list) -> None:
    os.makedirs(os.path.dirname(CUSTOM_RULES_FILE), exist_ok=True)
    with open(CUSTOM_RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False, indent=2)


def _load_file(path: str) -> str | None:
    if not os.path.isfile(path):
        print(f"{Fore.RED}✗ File not found: {path}{Style.RESET_ALL}")
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def _rule_exists(rules: list, pattern: str) -> bool:
    return any(r["pattern"] == pattern for r in rules)


def _preview(before: str, after: str, max_lines: int = 12) -> None:
    """Show changed lines side-by-side (before → after)."""
    b_lines = before.splitlines()
    a_lines = after.splitlines()

    changed = [
        (i, b, a)
        for i, (b, a) in enumerate(zip(b_lines, a_lines), 1)
        if b != a
    ]

    if not changed:
        print(f"{Fore.YELLOW}  (no line-level diff found — might be whitespace change){Style.RESET_ALL}")
        return

    shown = changed[:max_lines]
    for lineno, b, a in shown:
        print(f"  {Fore.RED}L{lineno:>4}  - {b.strip()}{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}       + {a.strip()}{Style.RESET_ALL}")
    if len(changed) > max_lines:
        print(f"  {Fore.YELLOW}  … and {len(changed) - max_lines} more changed line(s){Style.RESET_ALL}")


# ─────────────────────────── main flow ──────────────────────────

def main():
    print(f"\n{Fore.YELLOW}╔══════════════════════════════════╗")
    print(f"║   MIF Rule Admin — rule tester   ║")
    print(f"╚══════════════════════════════════╝{Style.RESET_ALL}\n")

    # 1. File path
    while True:
        path = input("Path to test MIF file: ").strip().strip('"')
        content = _load_file(path)
        if content is not None:
            break

    print(f"{Fore.GREEN}✓ File loaded ({len(content):,} chars){Style.RESET_ALL}\n")

    while True:
        print(f"{Fore.CYAN}─────────────────────────────────────{Style.RESET_ALL}")
        print("Options:  [t] test new rule   [l] list custom rules   [d] delete rule   [q] quit\n")
        choice = input("Choice: ").strip().lower()

        if choice == "q":
            print("Bye.")
            break

        elif choice == "l":
            _cmd_list()

        elif choice == "d":
            _cmd_delete()

        elif choice == "t":
            _cmd_test(content)

        else:
            print(f"{Fore.RED}Unknown option.{Style.RESET_ALL}")


def _cmd_list():
    rules = _load_custom_rules()
    if not rules:
        print(f"{Fore.YELLOW}  No custom rules yet.{Style.RESET_ALL}\n")
        return
    print(f"\n{Fore.CYAN}Custom rules ({len(rules)}):{Style.RESET_ALL}")
    for i, r in enumerate(rules, 1):
        print(f"  {i:>2}. {Fore.WHITE}{r['description']}{Style.RESET_ALL}")
        print(f"      pattern     : {r['pattern'][:80]}")
        print(f"      replacement : {r['replacement'][:80]}")
    print()


def _cmd_delete():
    rules = _load_custom_rules()
    if not rules:
        print(f"{Fore.YELLOW}  No custom rules to delete.{Style.RESET_ALL}\n")
        return
    _cmd_list()
    raw = input("Enter rule number to delete (or Enter to cancel): ").strip()
    if not raw:
        return
    try:
        idx = int(raw) - 1
        removed = rules.pop(idx)
        _save_custom_rules(rules)
        print(f"{Fore.GREEN}✓ Deleted: {removed['description']}{Style.RESET_ALL}\n")
    except (ValueError, IndexError):
        print(f"{Fore.RED}✗ Invalid number.{Style.RESET_ALL}\n")


def _cmd_test(content: str):
    print(f"\n{Fore.CYAN}Enter the regex pattern (Python re syntax).{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Tip: use raw string style — backslashes are taken literally.{Style.RESET_ALL}\n")

    # Pattern
    pattern = input("Pattern     : ").strip()
    if not pattern:
        print(f"{Fore.YELLOW}  Cancelled.{Style.RESET_ALL}\n")
        return

    # Validate regex before anything else
    try:
        compiled = re.compile(pattern)
    except re.error as e:
        print(f"{Fore.RED}✗ Invalid regex: {e}{Style.RESET_ALL}\n")
        return

    # Find matches
    matches = list(compiled.finditer(content))
    if not matches:
        print(f"\n{Fore.RED}✗ Pattern not found in file.{Style.RESET_ALL}")
        print("  No changes made.\n")
        return

    print(f"\n{Fore.GREEN}✓ Found {len(matches)} match(es).{Style.RESET_ALL}")
    print(f"  First match (chars {matches[0].start()}–{matches[0].end()}):")
    print(f"  {Fore.WHITE}{repr(matches[0].group()[:120])}{Style.RESET_ALL}\n")

    # Replacement
    replacement = input("Replacement : ").strip()

    # Dry-run
    try:
        new_content, count = re.subn(pattern, replacement, content)
    except re.error as e:
        print(f"{Fore.RED}✗ Replacement error: {e}{Style.RESET_ALL}\n")
        return

    print(f"\n{Fore.CYAN}─── Preview ({count} replacement(s)) ───{Style.RESET_ALL}")
    _preview(content, new_content)
    print()

    # Save decision
    answer = input("Apply and save to custom_rules.json? [y/n]: ").strip().lower()
    if answer != "y":
        print(f"{Fore.YELLOW}  Not saved.{Style.RESET_ALL}\n")
        return

    # Description
    description = input("Description (what does this rule do?): ").strip()
    if not description:
        description = f"Custom rule: {pattern[:60]}"

    rules = _load_custom_rules()

    if _rule_exists(rules, pattern):
        overwrite = input(f"{Fore.YELLOW}Rule with this pattern already exists. Overwrite? [y/n]: {Style.RESET_ALL}").strip().lower()
        if overwrite != "y":
            print(f"{Fore.YELLOW}  Kept existing rule.{Style.RESET_ALL}\n")
            return
        rules = [r for r in rules if r["pattern"] != pattern]

    rules.append({
        "pattern": pattern,
        "replacement": replacement,
        "description": description
    })
    _save_custom_rules(rules)
    print(f"{Fore.GREEN}✓ Saved to {CUSTOM_RULES_FILE}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
