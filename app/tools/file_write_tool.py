"""Contains FileTool class definition"""

from typing import Any, Dict

from app.errors import FileWriteError
from app.tools.base_tool import BaseTool


class FileWriteTool(BaseTool):
    """Handles the execution of file-related system tools."""

    def name(self) -> str:
        return "FileWrite"

    def execute(self, arguments: Dict[str, Any]) -> str:
        file_path = arguments.get("file_path")
        content = arguments.get("content")

        if not file_path:
            raise ValueError("file_path is required")

        if content is None:
            raise ValueError("content is required")

        return self._write(file_path, content)

    def _write(self, file_path: str, content: str) -> str:
        """Write content to a file"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                return f"Successfully wrote to {file_path}."
        except (PermissionError, IsADirectoryError, OSError) as e:
            raise FileWriteError(f"Failed to write to '{file_path}': {e}") from e
