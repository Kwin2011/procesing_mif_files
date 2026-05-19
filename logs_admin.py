import os
import msvcrt
from colorama import init, Fore, Style
from processing_logger import ProcessingLogger

init()


class LogsAdminInterface:
    """
    Interactive console admin panel for browsing processing history.

    Features:
    - Lists all processed files sorted by date (newest first).
    - Navigate with arrow keys, open log detail with Enter.
    - Detail view shows: settings snapshot, content replacer logs, status.
    - Press Esc or Q to go back / exit.
    """

    def __init__(self):
        self.logger = ProcessingLogger()
        self.entries = []
        self.selection = 0
        self.run()

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _clear():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def _getch() -> int:
        key = ord(msvcrt.getch())
        if key == 224:
            return 1000 + ord(msvcrt.getch())   # arrows → 1072 / 1080
        return key

    @staticmethod
    def _format_ts(iso: str) -> str:
        """Convert ISO timestamp to human-friendly format."""
        try:
            date, time = iso.split("T")
            y, m, d = date.split("-")
            return f"{d}.{m}.{y}  {time}"
        except Exception:
            return iso

    @staticmethod
    def _status_color(status: str) -> str:
        return Fore.GREEN if status == "success" else Fore.RED

    @staticmethod
    def _paginate(items, page_size=20):
        """Split a list into pages."""
        for i in range(0, len(items), page_size):
            yield items[i: i + page_size]

    # ------------------------------------------------------------------ #
    #  List view                                                           #
    # ------------------------------------------------------------------ #

    def _display_list(self):
        self._clear()
        self.entries = self.logger.get_all_entries()

        print(f"{Fore.YELLOW}╔══════════════════════════════════════════════════════════════╗")
        print(f"║          MIF Processing History  —  Log Admin                ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}↑ ↓{Style.RESET_ALL} Navigate   "
              f"{Fore.CYAN}Enter{Style.RESET_ALL} Open logs   "
              f"{Fore.CYAN}R{Style.RESET_ALL} Refresh   "
              f"{Fore.CYAN}Esc{Style.RESET_ALL} Exit\n")

        if not self.entries:
            print(f"  {Fore.WHITE}No processing history found.{Style.RESET_ALL}")
            print(f"\n  Run the main program to process MIF files first.")
            return

        # Column header
        print(f"  {'#':<4} {'Date & Time':<22} {'Status':<10} {'File name'}")
        print(f"  {'─'*4} {'─'*22} {'─'*10} {'─'*40}")

        for i, entry in enumerate(self.entries):
            prefix = f"{Fore.YELLOW}▶ {Style.RESET_ALL}" if i == self.selection else "  "
            ts = self._format_ts(entry["processed_at"])
            status = entry["status"]
            sc = self._status_color(status)
            name = entry["file_name"]

            # Truncate long names
            if len(name) > 45:
                name = "…" + name[-44:]

            row_color = Fore.WHITE if i == self.selection else Fore.LIGHTBLACK_EX
            print(
                f"{prefix}{row_color}{i + 1:<4}{Style.RESET_ALL} "
                f"{row_color}{ts:<22}{Style.RESET_ALL} "
                f"{sc}{status:<10}{Style.RESET_ALL} "
                f"{row_color}{name}{Style.RESET_ALL}"
            )

        print(f"\n  {Fore.LIGHTBLACK_EX}Total: {len(self.entries)} file(s){Style.RESET_ALL}")

    # ------------------------------------------------------------------ #
    #  Detail view                                                         #
    # ------------------------------------------------------------------ #

    def _display_detail(self, entry: dict):
        detail = self.logger.load_log_detail(entry["log_file"])
        if not detail:
            print(f"{Fore.RED}  ✗ Log file not found or corrupted.{Style.RESET_ALL}")
            input("\n  Press Enter to go back...")
            return

        page = 0
        while True:
            self._clear()
            sc = self._status_color(detail["status"])

            print(f"{Fore.YELLOW}╔══════════════════════════════════════════════════════════════╗")
            print(f"║  Log Detail                                                  ║")
            print(f"╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

            # Header info
            print(f"  {Fore.CYAN}File:{Style.RESET_ALL}        {detail['file_name']}")
            print(f"  {Fore.CYAN}Full path:{Style.RESET_ALL}   {detail['file_path']}")
            print(f"  {Fore.CYAN}Processed:{Style.RESET_ALL}   {self._format_ts(detail['processed_at'])}")
            print(f"  {Fore.CYAN}Status:{Style.RESET_ALL}      {sc}{detail['status'].upper()}{Style.RESET_ALL}")

            if detail.get("result_path"):
                print(f"  {Fore.CYAN}Output:{Style.RESET_ALL}      {detail['result_path']}")

            if detail.get("error_message"):
                print(f"\n  {Fore.RED}Error:{Style.RESET_ALL} {detail['error_message']}")

            # Settings snapshot
            print(f"\n  {Fore.YELLOW}── Settings snapshot ──────────────────────────────────────{Style.RESET_ALL}")
            for k, v in detail.get("settings_snapshot", {}).items():
                print(f"    {Fore.CYAN}{k:<20}{Style.RESET_ALL} {v}")

            # Content logs (paginated, 20 per page)
            logs = detail.get("content_logs", [])
            pages = list(self._paginate(logs, 20))
            total_pages = len(pages)

            print(f"\n  {Fore.YELLOW}── Processing log  (page {page + 1}/{max(1, total_pages)}) ────────────────────────{Style.RESET_ALL}")

            if not logs:
                print(f"    {Fore.LIGHTBLACK_EX}(no log entries){Style.RESET_ALL}")
            else:
                for line in pages[page]:
                    if line.startswith("[SUCCESS]"):
                        color = Fore.GREEN
                    elif line.startswith("[FAILURE]"):
                        color = Fore.YELLOW
                    elif line.startswith("[ERROR]"):
                        color = Fore.RED
                    elif line.startswith("[INFO]"):
                        color = Fore.CYAN
                    else:
                        color = Fore.LIGHTBLACK_EX
                    print(f"    {color}{line}{Style.RESET_ALL}")

            print(f"\n  {Fore.CYAN}← →{Style.RESET_ALL} Scroll pages   {Fore.CYAN}Esc{Style.RESET_ALL} Back to list")

            # Input
            key = self._getch()
            if key == 27 or key in (ord("q"), ord("Q")):   # Esc or Q → back
                return
            elif key == 1077 and page > 0:                  # ← arrow
                page -= 1
            elif key == 1080 and page < total_pages - 1:    # → actually ↓ for next
                page += 1
            elif key == 1072 and page > 0:                  # ↑ → prev page
                page -= 1
            elif key == 1080 and page < total_pages - 1:    # ↓ → next page
                page += 1

    # ------------------------------------------------------------------ #
    #  Main loop                                                           #
    # ------------------------------------------------------------------ #

    def run(self):
        """Main event loop for the logs admin panel."""
        while True:
            self._display_list()
            self.entries = self.logger.get_all_entries()

            if not self.entries:
                input("\n  Press Enter to exit...")
                return

            key = self._getch()

            if key == 27 or key in (ord("q"), ord("Q")):   # Esc / Q → exit
                self._clear()
                return

            elif key == 1072:                               # ↑ arrow (224, 72)
                self.selection = max(0, self.selection - 1)

            elif key == 1080:                               # ↓ arrow (224, 80)
                self.selection = min(len(self.entries) - 1, self.selection + 1)

            elif key == 13:                                 # Enter → open detail
                if 0 <= self.selection < len(self.entries):
                    self._display_detail(self.entries[self.selection])

            elif key in (ord("r"), ord("R")):               # R → refresh
                self.selection = 0


# ------------------------------------------------------------------ #
#  Standalone entry point                                              #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    LogsAdminInterface()
