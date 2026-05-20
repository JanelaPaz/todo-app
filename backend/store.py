"""JSON file-based persistence layer."""

import json
import os
import tempfile
from pathlib import Path


class JSONStore:
    """A file-based persistence layer that reads/writes JSON arrays.

    Uses atomic writes (temp file + os.replace) to prevent file corruption.
    Creates the file with an empty array if it does not exist.
    """

    def __init__(self, file_path: str):
        """Initialize store with path to JSON file."""
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create the JSON file with an empty array if it does not exist."""
        path = Path(self.file_path)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            self._write_atomic([])

    def _write_atomic(self, data: list[dict]) -> None:
        """Write data atomically using a temp file and os.replace.

        Writes to a temporary file in the same directory, then atomically
        replaces the target file. This prevents corruption if the process
        crashes mid-write.

        Raises:
            IOError: If the write operation fails.
        """
        dir_path = os.path.dirname(os.path.abspath(self.file_path))
        fd, tmp_path = tempfile.mkstemp(dir=dir_path, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as tmp_file:
                json.dump(data, tmp_file, indent=2, default=str)
            os.replace(tmp_path, self.file_path)
        except Exception:
            # Clean up temp file if replace failed
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

    def read_all(self) -> list[dict]:
        """Read all records from the JSON file.

        Creates the file with an empty array if it does not exist.

        Returns:
            A list of all records in the store.

        Raises:
            IOError: If the file cannot be read.
        """
        try:
            if not os.path.exists(self.file_path):
                self._write_atomic([])
                return []
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except (json.JSONDecodeError, IOError) as e:
            raise IOError(f"Failed to read store file: {self.file_path}") from e

    def write_all(self, data: list[dict]) -> None:
        """Atomically write all records to the JSON file.

        Args:
            data: The complete list of records to persist.

        Raises:
            IOError: If the write operation fails.
        """
        try:
            self._write_atomic(data)
        except Exception as e:
            raise IOError(f"Failed to write store file: {self.file_path}") from e

    def find_by_id(self, record_id: str) -> dict | None:
        """Find a single record by its id field.

        Args:
            record_id: The id value to search for.

        Returns:
            The matching record dict, or None if not found.
        """
        records = self.read_all()
        for record in records:
            if record.get("id") == record_id:
                return record
        return None

    def find_by_field(self, field: str, value: str) -> dict | None:
        """Find a single record by an arbitrary field match.

        Args:
            field: The field name to search on.
            value: The value to match.

        Returns:
            The first matching record dict, or None if not found.
        """
        records = self.read_all()
        for record in records:
            if record.get(field) == value:
                return record
        return None

    def add(self, record: dict) -> dict:
        """Append a record to the store and persist.

        Args:
            record: The record dict to add.

        Returns:
            The added record.

        Raises:
            IOError: If the write operation fails.
        """
        records = self.read_all()
        records.append(record)
        self.write_all(records)
        return record

    def update(self, record_id: str, updates: dict) -> dict | None:
        """Update fields on a record by id and persist.

        Args:
            record_id: The id of the record to update.
            updates: A dict of field names and new values to apply.

        Returns:
            The updated record dict, or None if the record was not found.

        Raises:
            IOError: If the write operation fails.
        """
        records = self.read_all()
        for i, record in enumerate(records):
            if record.get("id") == record_id:
                records[i].update(updates)
                self.write_all(records)
                return records[i]
        return None

    def delete(self, record_id: str) -> bool:
        """Remove a record by id and persist.

        Args:
            record_id: The id of the record to remove.

        Returns:
            True if the record was found and removed, False otherwise.

        Raises:
            IOError: If the write operation fails.
        """
        records = self.read_all()
        original_length = len(records)
        records = [r for r in records if r.get("id") != record_id]
        if len(records) == original_length:
            return False
        self.write_all(records)
        return True
