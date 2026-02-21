"""Contains FileToolHandler class definition"""


class FileToolHandler:
    """Handles the execution of file-related system tools."""

    @staticmethod
    def read_file(file_path: str) -> str:
        """Read file and return content"""
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

    @staticmethod
    def write_file(file_path: str, content: str, mode: str):
        """Write content to a file"""
        try:
            with open(file_path, mode, encoding="utf-8") as f:
                f.write(content)
                return f"Successfully wrote to {file_path}."
        except PermissionError:
            return f"Error: Permission denied. Cannot write to {file_path}."
        except IsADirectoryError:
            return f"Error: {file_path} is a directory, not a file."
        except OSError as e:
            return f"Error: Failed to write to file due to a system error: {e}"
