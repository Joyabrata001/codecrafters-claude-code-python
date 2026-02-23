"""Contains FileTool class definition"""

from typing import Any, Dict

from app.errors import FileReadError
from app.tools.base_tool import BaseTool


class FileReadTool(BaseTool):
    """Handles file read operations."""

    def name(self) -> str:
        return "FileRead"

    def execute(self, arguments: Dict[str, Any]) -> str:
        file_path = arguments.get("file_path")

        if not file_path:
            raise ValueError("file_path is required")

        return self._read(file_path)

    def _read(self, file_path: str) -> str:
        """Read file and return content"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as e:
            raise FileReadError(f"Failed to read file: '{file_path}': {e}") from e
