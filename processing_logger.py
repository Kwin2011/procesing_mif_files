import os
from datetime import datetime


class ProcessingLogger:
    """
    Writes a processing log file next to the output file.

    Log format:
        [SUCCESS] description: N replacement(s) made.
        [FAILURE] description: no matches found.
        [ERROR]   description: invalid regex — ...
        [INFO]    informational message
        [WARNING] non-fatal issue
    """

    def __init__(self, source_file_path: str):
        """
        :param source_file_path: Path to the MIF file being processed.
                                 The log will be written alongside it.
        """
        base, _ = os.path.splitext(source_file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = f"{base}_log_{timestamp}.txt"
        self._lines = []
        self._stats = {"SUCCESS": 0, "FAILURE": 0, "ERROR": 0}

    def add(self, message: str) -> None:
        """Append one log message and update counters."""
        self._lines.append(message)
        for level in self._stats:
            if message.startswith(f"[{level}]"):
                self._stats[level] += 1
                break

    def add_all(self, messages: list) -> None:
        """Append a list of messages (e.g. from ContentReplacer.get_logs())."""
        for msg in messages:
            self.add(msg)

    def save(self) -> str:
        """
        Write the log to disk and return the log file path.
        Includes a summary section at the top.
        """
        total = sum(self._stats.values())
        header = [
            "=" * 60,
            f"  Processing log",
            f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"  Log file:  {self.log_path}",
            "=" * 60,
            "",
            "  SUMMARY",
            f"  Rules applied (SUCCESS): {self._stats['SUCCESS']}",
            f"  No match    (FAILURE):   {self._stats['FAILURE']}",
            f"  Errors      (ERROR):     {self._stats['ERROR']}",
            f"  Total rules checked:     {total}",
            "",
            "=" * 60,
            "",
        ]

        content = "\n".join(header + self._lines)

        folder = os.path.dirname(self.log_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(content)

        return self.log_path
