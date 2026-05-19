import os
import json
from datetime import datetime


class ProcessingLogger:
    """
    Manages processing history logs for MIF files.

    Each processed file gets a JSON log entry stored in the logs/ directory.
    The master index (logs/index.json) keeps a summary of all processed files.

    Log entry structure:
    {
        "file_path": str,
        "file_name": str,
        "processed_at": str (ISO 8601),
        "result_path": str,
        "status": "success" | "error",
        "error_message": str | null,
        "settings_snapshot": dict,
        "content_logs": list[str]
    }
    """

    LOGS_DIR = "logs"
    INDEX_FILE = "logs/index.json"

    def __init__(self):
        self._ensure_logs_dir()

    def _ensure_logs_dir(self):
        """Create logs directory if it does not exist."""
        os.makedirs(self.LOGS_DIR, exist_ok=True)

    def _load_index(self) -> list:
        """Load the master index of all processed files."""
        if not os.path.isfile(self.INDEX_FILE):
            return []
        try:
            with open(self.INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_index(self, index: list):
        """Persist the master index to disk."""
        with open(self.INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4, ensure_ascii=False)

    def _log_file_path(self, timestamp: str, file_name: str) -> str:
        """Build a unique log file path based on timestamp and file name."""
        safe_name = file_name.replace("/", "_").replace("\\", "_")
        safe_ts = timestamp.replace(":", "-").replace(".", "-")
        return os.path.join(self.LOGS_DIR, f"{safe_ts}__{safe_name}.json")

    def save_log(
        self,
        file_path: str,
        result_path: str | None,
        status: str,
        settings_snapshot: dict,
        content_logs: list[str],
        error_message: str | None = None,
    ) -> str:
        """
        Save a processing log entry for one file.

        :param file_path: Original input file path.
        :param result_path: Output file path (None on error).
        :param status: 'success' or 'error'.
        :param settings_snapshot: Metadata dict at the time of processing.
        :param content_logs: List of log strings from ContentReplacer.
        :param error_message: Error description if status is 'error'.
        :return: Path to the saved log file.
        """
        timestamp = datetime.now().isoformat(timespec="seconds")
        file_name = os.path.basename(file_path)

        entry = {
            "file_path": file_path,
            "file_name": file_name,
            "processed_at": timestamp,
            "result_path": result_path,
            "status": status,
            "error_message": error_message,
            "settings_snapshot": settings_snapshot,
            "content_logs": content_logs,
        }

        log_file = self._log_file_path(timestamp, file_name)
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=4, ensure_ascii=False)

        # Update master index
        index = self._load_index()
        index.append({
            "file_name": file_name,
            "file_path": file_path,
            "processed_at": timestamp,
            "status": status,
            "log_file": log_file,
        })
        self._save_index(index)

        return log_file

    def get_all_entries(self) -> list:
        """
        Return all index entries sorted by processed_at descending (newest first).
        """
        index = self._load_index()
        return sorted(index, key=lambda e: e["processed_at"], reverse=True)

    def load_log_detail(self, log_file: str) -> dict | None:
        """
        Load full log detail for a specific log file.

        :param log_file: Path returned from get_all_entries()[n]['log_file'].
        :return: Full log dict or None if file is missing/corrupt.
        """
        if not os.path.isfile(log_file):
            return None
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
