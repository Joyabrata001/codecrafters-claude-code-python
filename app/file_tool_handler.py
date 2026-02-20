"""Contains FileToolHandler class definition"""


class FileToolHandler:
    """Handles the execution of file-related system tools."""

    @staticmethod
    def read_file(file_path: str) -> str:
        """Reads file and returns content"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: The file at {file_path} was not found."
        except PermissionError:
            return f"Error: Permission denied to read {file_path}."
        except UnicodeDecodeError:
            return f"Error: Could not decode {file_path}. Check the encoding."
        except OSError as e:
            return f"An unexpected error occurred: {e}"
