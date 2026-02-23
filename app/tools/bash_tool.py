"""Contains BashHandler class definition"""

import shlex
import subprocess

from app.errors import BashExecutionError


ALLOWED_COMMANDS = frozenset(
    {
        # File directory and navigation
        "ls",
        "pwd",
        # "cd",
        # File content and manipulation
        "cat",
        "head",
        "tail",
        "grep",
        "find",
        # "touch",
        # "mkdir",
        # File operations
        # "cp",
        # "mv",
        "rm",
        # Text processing
        # "sed",
        # "awk",
        # "sort",
        # "wc",
        # System and environment info
        "echo",
        "date",
        "whoami",
        # "env",
    }
)


class BashTool:
    """Handles the execution of shell command"""

    @staticmethod
    def run_command(command: str) -> str:
        """Run shell command"""
        try:
            args = shlex.split(command)

            if not args:
                raise BashExecutionError("Empty command")

        except Exception as e:
            raise BashExecutionError(f"Invalid command syntax: {e}") from e

        base_cmd = args[0]

        if base_cmd not in ALLOWED_COMMANDS:
            raise BashExecutionError(f"{args[0]} command not allowed.")

        try:
            result = subprocess.run(
                args=args,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                timeout=10,
            )

            return result.stdout or ""

        except subprocess.TimeoutExpired as e:
            raise BashExecutionError(f"Command '{command}' timed out after 10s") from e
        except subprocess.CalledProcessError as e:
            raise BashExecutionError(f"Command failed: {e.stderr.strip()}") from e
        except FileNotFoundError as e:
            raise BashExecutionError(f"Executable not found for: {command}") from e
        except Exception as e:
            raise BashExecutionError(f"Unexpected shell error: {e}") from e
