"""Contains FileToolHandler class definition"""

from app.errors import FileReadError, FileWriteError


class FileTool:
    """Handles the execution of file-related system tools."""

    @staticmethod
    def read_file(file_path: str) -> str:
        """Read file and return content"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as e:
            raise FileReadError(f"Failed to read file: '{file_path}': {e}") from e

    @staticmethod
    def write_file(file_path: str, content: str) -> str:
        """Write content to a file"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                return f"Successfully wrote to {file_path}."
        except (PermissionError, IsADirectoryError, OSError) as e:
            raise FileWriteError(f"Failed to write to '{file_path}': {e}") from e
